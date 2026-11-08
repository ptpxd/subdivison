from __future__ import annotations

from enum import Enum
from pathlib import Path

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QSlider
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
)
from pyvistaqt import QtInteractor

from .mesh import HalfEdgeMesh, MeshLoadError, load_mesh
from .subdivision import SubdivisionScheme, subdivide_mesh


class DisplayMode(str, Enum):
    FLAT_SHADED = "flat-shaded"
    WIREFRAME = "wireframe"
    WIREFRAME_NO_BACK = "wireframe-no-back"


def actor_options(mode: DisplayMode) -> dict[str, object]:
    if mode is DisplayMode.WIREFRAME:
        return {
            "style": "wireframe",
            "color": "white",
            "smooth_shading": False,
        }

    elif mode is DisplayMode.WIREFRAME_NO_BACK:
        return {
            "style": "surface",
            "color": "white",
            "show_edges": True,
            "edge_color": "#1E1F22",
            "lighting": False,
            "smooth_shading": False,
        }

    return {
        "style": "surface",
        "smooth_shading": False,
    }


class MeshViewerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Mesh Subdivision Viewer")
        self.resize(1000, 700)

        self._mesh: HalfEdgeMesh | None = None
        self._loaded_mesh: HalfEdgeMesh | None = None
        self._iteration_count = 0
        self._applied_iterations = 0
        self._scheme = SubdivisionScheme.LOOP
        self._applied_scheme: SubdivisionScheme | None = None
        self._last_subdivision_summary: str | None = None
        self._display_mode = DisplayMode.FLAT_SHADED

        self.plotter = QtInteractor(self)

        # Create the right panel for mesh data
        self.info_panel = QWidget(self)
        self.info_layout = QVBoxLayout(self.info_panel)
        self.vertex_label = QLabel("Vertices: 0", self.info_panel)
        self.face_label = QLabel("Triangles: 0", self.info_panel)
        self.iteration_label = QLabel("Selected iterations: 0", self.info_panel)
        self.iteration_slider = QSlider(Qt.Orientation.Horizontal, self.info_panel)  # Add slider
        self.iteration_slider.setRange(0, 4)
        self.iteration_slider.setValue(self._iteration_count)
        self.iteration_slider.valueChanged.connect(self._update_iteration_count)  # Connect slider to update method

        self.info_layout.addWidget(self.vertex_label)
        self.info_layout.addWidget(self.face_label)
        self.info_layout.addWidget(self.iteration_label)
        self.info_layout.addWidget(self.iteration_slider)  # Add slider to layout
        self.info_panel.setLayout(self.info_layout)

        # Use a splitter to place the plotter and info panel side by side
        splitter = QSplitter(self)
        splitter.addWidget(self.plotter)
        splitter.addWidget(self.info_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)

        self._create_menus()
        self._result_label = QLabel("No subdivision applied.")
        self._result_label.setObjectName("subdivisionResult")
        self.statusBar().addPermanentWidget(self._result_label)
        self.statusBar().showMessage(
            "Open an STL or OBJ file. +/-: change iterations; N: subdivide; "
            "W: change display mode. Each iteration refines the entire mesh once."
        )

    def _update_info_panel(self) -> None:
        """Update mesh statistics while keeping the selected iteration count visible."""
        if self._mesh is None:
            self.vertex_label.setText("Vertices: 0")
            self.face_label.setText("Triangles: 0")
        else:
            self.vertex_label.setText(f"Vertices: {len(self._mesh.vertices)}")
            self.face_label.setText(f"Triangles: {len(self._mesh.faces)}")
        self.iteration_label.setText(f"Selected iterations: {self._iteration_count}")

    def _update_iteration_count(self, value: int) -> None:
        """Update the selected iteration count without modifying the mesh."""
        self._iteration_count = value
        self.iteration_label.setText(f"Selected iterations: {value}")
        if value == 0:
            message = "Select 1 to 4 iterations, then press N to subdivide."
        else:
            message = (
                f"Selected {value} subdivision "
                f"{'iteration' if value == 1 else 'iterations'}; press N to apply."
            )
        self.statusBar().showMessage(message)

    def _create_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        open_action = QAction("&Open mesh...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_mesh)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        mesh_menu = self.menuBar().addMenu("&Mesh")
        scheme_menu = mesh_menu.addMenu("&Subdivision scheme")
        scheme_menu.setToolTipsVisible(True)
        scheme_group = QActionGroup(self)
        scheme_group.setExclusive(True)
        self._scheme_actions: dict[SubdivisionScheme, QAction] = {}
        for scheme, label in (
                (SubdivisionScheme.LOOP, "&Loop"),
                (SubdivisionScheme.BUTTERFLY, "&Butterfly"),
        ):
            action = QAction(label, self, checkable=True)
            action.setChecked(scheme is self._scheme)
            action.setToolTip(
                "Selects the method for the next operation; choose "
                "Subdivide mesh or press N to apply it."
            )
            action.setStatusTip(action.toolTip())
            action.triggered.connect(
                lambda checked=False, selected=scheme: self._select_scheme(selected)
            )
            scheme_group.addAction(action)
            scheme_menu.addAction(action)
            self._scheme_actions[scheme] = action

        reset_action = QAction("&Reset to loaded mesh", self)
        reset_action.setShortcut(QKeySequence("R"))
        reset_action.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        reset_action.triggered.connect(self.reset_mesh)
        mesh_menu.addAction(reset_action)
        self._reset_action = reset_action

        display_menu = self.menuBar().addMenu("&Display")
        self._display_action = QAction("&Toggle wireframe / flat shading", self)
        self._display_action.setShortcut(QKeySequence("W"))
        self._display_action.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        self._display_action.triggered.connect(self.toggle_display_mode)
        display_menu.addAction(self._display_action)

        self._subdivide_action = QAction("&Subdivide mesh", self)
        self._subdivide_action.setShortcut(QKeySequence("N"))
        self._subdivide_action.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        self._subdivide_action.triggered.connect(self.subdivide_selected)
        mesh_menu.addAction(self._subdivide_action)

        increase_iteration_action = QAction("Increase iterations (+)", self)
        increase_iteration_action.setShortcut(QKeySequence("+"))
        increase_iteration_action.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        increase_iteration_action.triggered.connect(self._increment_iteration)
        mesh_menu.addAction(increase_iteration_action)

        decrease_iteration_action = QAction("Decrease iterations (-)", self)
        decrease_iteration_action.setShortcut(QKeySequence("-"))
        decrease_iteration_action.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        decrease_iteration_action.triggered.connect(self._decrement_iteration)
        mesh_menu.addAction(decrease_iteration_action)

    def _increment_iteration(self) -> None:
        """Increase the selected iteration count without subdividing."""
        if self._iteration_count < 4:
            self.iteration_slider.setValue(self._iteration_count + 1)

    def _decrement_iteration(self) -> None:
        """Decrease the selected iteration count without subdividing."""
        if self._iteration_count > 0:
            self.iteration_slider.setValue(self._iteration_count - 1)

    def open_mesh(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open triangular mesh",
            "",
            "Mesh files (*.stl *.obj)",
        )
        if not filename:
            return
        self.load_mesh_path(filename)

    def load_mesh_path(self, filename: str | Path) -> None:
        try:
            mesh = load_mesh(filename)
        except MeshLoadError as exc:
            self.statusBar().showMessage(str(exc))
            QMessageBox.warning(self, "Could not open mesh", str(exc))
            return

        self._mesh = mesh
        self._loaded_mesh = mesh
        self._applied_iterations = 0
        self._applied_scheme = None
        self._last_subdivision_summary = None
        self._result_label.setText(
            f"Loaded mesh: {len(mesh.faces)} faces; no subdivision applied."
        )
        self._display_mode = DisplayMode.FLAT_SHADED
        self._show_mesh(reset_camera=True)
        self._update_info_panel()  # Update the info panel with the new mesh data
        self.statusBar().showMessage(
            f"Loaded {Path(filename).name}. +/-: change iterations; "
            "N: subdivide; R: reset; W: change display mode. "
            "Each iteration refines the entire mesh once."
        )

    def _select_scheme(self, scheme: SubdivisionScheme) -> None:
        self._scheme = scheme
        self._scheme_actions[scheme].setChecked(True)
        self.statusBar().showMessage(
            f"Selected {scheme.value.title()}; {self._iteration_count} "
            f"{'iteration' if self._iteration_count == 1 else 'iterations'} "
            "remain selected. Press N to apply."
        )

    def subdivide_selected(self) -> None:
        if self._mesh is None or self._loaded_mesh is None:
            self.statusBar().showMessage("Load a valid mesh before subdividing.")
            return

        if self._iteration_count == 0:
            self.statusBar().showMessage(
                "No subdivision applied: select 1 to 4 iterations first."
            )
            return

        scheme_changed = (
            self._applied_iterations > 0 and self._applied_scheme is not self._scheme
        )
        if (
            self._iteration_count == self._applied_iterations
            and not scheme_changed
        ):
            self.statusBar().showMessage(
                f"{self._scheme.value.title()} subdivision: "
                f"{self._applied_iterations} "
                f"{'iteration' if self._applied_iterations == 1 else 'iterations'} "
                "already applied."
            )
            return

        face_count_before = len(self._mesh.faces)
        if scheme_changed or self._iteration_count < self._applied_iterations:
            refined = self._loaded_mesh
            iterations_to_apply = self._iteration_count
        else:
            refined = self._mesh
            iterations_to_apply = self._iteration_count - self._applied_iterations

        try:
            for _ in range(iterations_to_apply):
                refined = subdivide_mesh(refined, self._scheme)
        except (ValueError, RuntimeError) as exc:
            self.statusBar().showMessage(f"Subdivision failed: {exc}")
            QMessageBox.warning(self, "Subdivision failed", str(exc))
            return

        self._mesh = refined
        self._applied_iterations = self._iteration_count
        self._applied_scheme = self._scheme
        self._show_mesh(reset_camera=False)
        self._update_info_panel()
        face_count_after = len(self._mesh.faces)
        self._last_subdivision_summary = (
            f"{self._scheme.value.title()} subdivision: applied "
            f"{self._applied_iterations} "
            f"{'iteration' if self._applied_iterations == 1 else 'iterations'}; faces "
            f"{face_count_before} -> {face_count_after}."
        )
        self._result_label.setText(self._last_subdivision_summary)
        self.statusBar().showMessage(
            self._last_subdivision_summary
        )
    def reset_mesh(self) -> None:
        if self._loaded_mesh is None:
            self.statusBar().showMessage("Load a valid mesh before resetting.")
            return
        if self._applied_iterations == 0:
            self.statusBar().showMessage("Mesh is already at its loaded state.")
            return

        self._mesh = self._loaded_mesh
        self._applied_iterations = 0
        self._applied_scheme = None
        self._last_subdivision_summary = None
        self._result_label.setText(
            f"Loaded mesh: {len(self._loaded_mesh.faces)} faces; "
            "no subdivision applied."
        )
        self._show_mesh(reset_camera=False)
        self._update_info_panel()
        self.statusBar().showMessage(
            "Mesh reset to loaded state; 0 subdivision iterations applied."
        )

    def toggle_display_mode(self) -> None:
        if self._display_mode is DisplayMode.FLAT_SHADED:
            self._display_mode = DisplayMode.WIREFRAME
        elif self._display_mode is DisplayMode.WIREFRAME:
            self._display_mode = DisplayMode.WIREFRAME_NO_BACK
        else:
            self._display_mode = DisplayMode.FLAT_SHADED
        if self._mesh is not None:
            self._show_mesh(reset_camera=False)
        self.statusBar().showMessage(f"Display mode: {self._display_mode.value}.")

    def _show_mesh(self, *, reset_camera: bool) -> None:
        if self._mesh is None:
            return
        self.plotter.add_mesh(
            self._mesh.to_polydata(),
            name="mesh",
            reset_camera=reset_camera,
            **actor_options(self._display_mode),
        )
        if reset_camera:
            self.plotter.reset_camera()

def main() -> int:
    application = QApplication.instance() or QApplication([])
    window = MeshViewerWindow()
    window.show()
    return application.exec()