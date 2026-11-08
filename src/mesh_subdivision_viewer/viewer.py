from __future__ import annotations

from enum import Enum
from pathlib import Path

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QSlider
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
)
from pyvistaqt import QtInteractor

from .mesh import HalfEdgeMesh, MeshLoadError, load_mesh
from .subdivision import SubdivisionScheme, subdivide_mesh


class DisplayMode(str, Enum):
    FLAT_SHADED = "flat-shaded"
    WIREFRAME = "wireframe"


def actor_options(mode: DisplayMode) -> dict[str, object]:
    if mode is DisplayMode.WIREFRAME:
        return {"style": "wireframe", "smooth_shading": False}
    return {"style": "surface", "smooth_shading": False}


class MeshViewerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Mesh Subdivision Viewer")
        self.resize(1000, 700)

        self._mesh: HalfEdgeMesh | None = None
        self._loaded_mesh: HalfEdgeMesh | None = None
        self._iteration_count = 1
        self._applied_iterations = 0
        self._scheme = SubdivisionScheme.LOOP
        self._display_mode = DisplayMode.FLAT_SHADED

        self.plotter = QtInteractor(self)

        # Create the right panel for mesh data
        self.info_panel = QWidget(self)
        self.info_layout = QVBoxLayout(self.info_panel)
        self.vertex_label = QLabel("Vertices: 0", self.info_panel)
        self.face_label = QLabel("Triangles: 0", self.info_panel)
        self.iteration_label = QLabel("Iteration: 0", self.info_panel)  # Label for applied iterations
        self.iteration_slider = QSlider(Qt.Orientation.Horizontal, self.info_panel)  # Add slider
        self.iteration_slider.setRange(0, 4)  # Limit to 1-5 iterations
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
        self.statusBar().showMessage(
            "Open an STL or OBJ file. N: subdivide; W: change display mode. "
            "Each iteration is one complete pass over the mesh."
        )

    def _update_info_panel(self) -> None:
        """Update the vertex, triangle counts, and iteration count in the info panel."""
        if self._mesh is None:
            self.vertex_label.setText("Vertices: 0")
            self.face_label.setText("Triangles: 0")
            self.iteration_label.setText("Iteration: 0")  # Reset iteration count
        else:
            self.vertex_label.setText(f"Vertices: {len(self._mesh.vertices)}")
            self.face_label.setText(f"Triangles: {len(self._mesh.faces)}")
            self.iteration_label.setText(f"Iteration: {self._applied_iterations}")  # Update applied iterations

    def _update_iteration_count(self, value: int) -> None:
        """Update the iteration count based on the slider value and apply subdivision."""
        self._iteration_count = value
        self.iteration_label.setText(f"Iteration: {value}")  # Update the label dynamically
        self.statusBar().showMessage(f"Next subdivision applies {value} iteration(s).")

        # Apply subdivision to update the mesh
        self.subdivide_selected()

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
        scheme_group = QActionGroup(self)
        scheme_group.setExclusive(True)
        self._scheme_actions: dict[SubdivisionScheme, QAction] = {}
        for scheme, label in (
                (SubdivisionScheme.LOOP, "&Loop"),
                (SubdivisionScheme.BUTTERFLY, "&Butterfly"),
        ):
            action = QAction(label, self, checkable=True)
            action.setChecked(scheme is self._scheme)
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
        self._display_mode = DisplayMode.FLAT_SHADED
        self._show_mesh(reset_camera=True)
        self._update_info_panel()  # Update the info panel with the new mesh data
        self.statusBar().showMessage(
            f"Loaded {Path(filename).name}. N: subdivide; R: reset; "
            "W: change display mode. Each iteration is one complete pass."
        )

    def _select_scheme(self, scheme: SubdivisionScheme) -> None:
        self._scheme = scheme
        self._scheme_actions[scheme].setChecked(True)
        self.statusBar().showMessage(f"Subdivision scheme: {scheme.value.title()}")

    def _select_iteration_count(self, count: int) -> None:
        self._iteration_count = count
        self._iteration_actions[count].setChecked(True)
        self.statusBar().showMessage(
            f"Next subdivision applies {count} complete "
            f"{'iteration' if count == 1 else 'iterations'}."
        )

    def subdivide_selected(self) -> None:
        if self._mesh is None:
            self.statusBar().showMessage("Load a valid mesh before subdividing.")
            return

        # Ensure the applied iterations do not exceed the maximum
        if self._applied_iterations >= 4 and self._iteration_count > self._applied_iterations:
            self.statusBar().showMessage("Maximum iterations (4) already applied.")
            return

        # Handle reverse iterations
        if self._iteration_count < self._applied_iterations:
            self._mesh = self._loaded_mesh

            try:
                for _ in range(self._iteration_count):
                    self._mesh = subdivide_mesh(
                        self._mesh,
                        self._scheme
                    )

            except (ValueError, RuntimeError) as exc:
                self.statusBar().showMessage(
                    f"Subdivision failed: {exc}"
                )
                QMessageBox.warning(
                    self,
                    "Subdivision failed",
                    str(exc)
                )
                return

            self._applied_iterations = self._iteration_count

            self._show_mesh(reset_camera=False)
            self._update_info_panel()

            return

        # Handle forward iterations
        remaining_iterations = self._iteration_count - self._applied_iterations
        try:
            refined = self._mesh
            for _ in range(remaining_iterations):
                refined = subdivide_mesh(refined, self._scheme)
        except (ValueError, RuntimeError) as exc:
            self.statusBar().showMessage(f"Subdivision failed: {exc}")
            QMessageBox.warning(self, "Subdivision failed", str(exc))
            return

        self._mesh = refined
        self._applied_iterations = self._iteration_count
        self._show_mesh(reset_camera=False)
        self._update_info_panel()
        self.statusBar().showMessage(
            f"{self._scheme.value.title()} subdivision: applied "
            f"{remaining_iterations} "
            f"{'iteration' if remaining_iterations == 1 else 'iterations'} "
            f"({self._applied_iterations} total)."
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
        self._show_mesh(reset_camera=False)
        self.statusBar().showMessage(
            "Mesh reset to loaded state; 0 subdivision iterations applied."
        )

    def toggle_display_mode(self) -> None:
        if self._display_mode is DisplayMode.FLAT_SHADED:
            self._display_mode = DisplayMode.WIREFRAME
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