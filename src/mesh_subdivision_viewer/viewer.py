from __future__ import annotations

from enum import Enum
from pathlib import Path

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
        self.setCentralWidget(self.plotter)
        self._create_menus()
        self.statusBar().showMessage(
            "Open an STL or OBJ file. N: subdivide; W: change display mode. "
            "Each iteration is one complete pass over the mesh."
        )

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

        iteration_menu = mesh_menu.addMenu("&Subdivision iterations")
        iteration_group = QActionGroup(self)
        iteration_group.setExclusive(True)
        self._iteration_actions: dict[int, QAction] = {}
        for count in range(1, 5):
            unit = "iteration" if count == 1 else "iterations"
            action = QAction(f"{count} {unit}", self, checkable=True)
            action.setChecked(count == self._iteration_count)
            action.triggered.connect(
                lambda checked=False, selected=count: self._select_iteration_count(
                    selected
                )
            )
            iteration_group.addAction(action)
            iteration_menu.addAction(action)
            self._iteration_actions[count] = action

        iterate_action = QAction("&Subdivide mesh", self)
        iterate_action.setShortcut(QKeySequence("N"))
        iterate_action.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        iterate_action.setToolTip(
            "Apply the selected number of complete subdivision passes to the current mesh."
        )
        iterate_action.setStatusTip(iterate_action.toolTip())
        iterate_action.triggered.connect(self.subdivide_selected)
        mesh_menu.addAction(iterate_action)

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
        try:
            refined = self._mesh
            for _ in range(self._iteration_count):
                refined = subdivide_mesh(refined, self._scheme)
        except (ValueError, RuntimeError) as exc:
            self.statusBar().showMessage(f"Subdivision failed: {exc}")
            QMessageBox.warning(self, "Subdivision failed", str(exc))
            return

        self._mesh = refined
        self._applied_iterations += self._iteration_count
        self._show_mesh(reset_camera=False)
        self.statusBar().showMessage(
            f"{self._scheme.value.title()} subdivision: applied "
            f"{self._iteration_count} "
            f"{'iteration' if self._iteration_count == 1 else 'iterations'} "
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
