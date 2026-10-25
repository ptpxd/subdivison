from mesh_subdivision_viewer.viewer import DisplayMode, actor_options


import math

import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from mesh_subdivision_viewer.subdivision import SubdivisionScheme
from mesh_subdivision_viewer.viewer import DisplayMode, MeshViewerWindow, actor_options


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def viewer(app):
    window = MeshViewerWindow()
    window.show()
    QTest.qWait(100)
    yield window
    window.close()
    window.plotter.close()


def test_flat_shaded_mode_uses_unsmoothed_surface():
    assert actor_options(DisplayMode.FLAT_SHADED) == {
        "style": "surface",
        "smooth_shading": False,
    }


def test_wireframe_mode_uses_wireframe_actor():
    assert actor_options(DisplayMode.WIREFRAME) == {
        "style": "wireframe",
        "smooth_shading": False,
    }


def test_display_mode_has_flat_shading_as_initial_mode():
    assert DisplayMode.FLAT_SHADED.value == "flat-shaded"


def test_keyboard_toggles_display_and_preserves_it_after_subdivision(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    assert viewer._display_mode is DisplayMode.FLAT_SHADED

    QTest.keyClick(viewer, Qt.Key.Key_W)
    assert viewer._display_mode is DisplayMode.WIREFRAME
    actor = viewer.plotter.renderer._actors["mesh"]
    assert actor.GetProperty().GetRepresentation() == 1

    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()
    QTest.keyClick(viewer, Qt.Key.Key_N)
    assert viewer._mesh is not None
    assert viewer._mesh.revision == 1
    assert viewer._display_mode is DisplayMode.WIREFRAME
    assert viewer.plotter.renderer._actors["mesh"].GetProperty().GetRepresentation() == 1

    QTest.keyClick(viewer, Qt.Key.Key_W)
    assert viewer._display_mode is DisplayMode.FLAT_SHADED
    assert viewer.plotter.renderer._actors["mesh"].GetProperty().GetRepresentation() == 2


def test_mouse_drag_rotates_and_wheel_zoom_changes_camera(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    interactor = viewer.plotter.iren.interactor
    viewer.plotter.ren_win.SetSize(1000, 700)
    viewer.plotter.render()
    camera = viewer.plotter.camera

    initial_position = tuple(camera.position)
    initial_focal_point = tuple(camera.focal_point)
    initial_distance = math.dist(initial_position, initial_focal_point)

    interactor.SetEventPosition(400, 300)
    interactor.LeftButtonPressEvent()
    interactor.SetEventPosition(520, 360)
    interactor.MouseMoveEvent()
    interactor.LeftButtonReleaseEvent()

    rotated_position = tuple(camera.position)
    assert all(math.isfinite(value) for value in rotated_position)
    assert rotated_position != initial_position

    interactor.SetEventPosition(520, 360)
    interactor.MouseWheelForwardEvent()
    zoomed_position = tuple(camera.position)

    assert all(math.isfinite(value) for value in zoomed_position)
    assert math.dist(zoomed_position, tuple(camera.focal_point)) < math.dist(
        rotated_position, tuple(camera.focal_point)
    )
