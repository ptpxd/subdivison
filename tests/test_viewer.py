import math

import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from mesh_subdivision_viewer.subdivision import SubdivisionScheme
from mesh_subdivision_viewer import viewer as viewer_module
from mesh_subdivision_viewer.viewer import (
    DisplayMode,
    MeshViewerWindow,
    actor_options,
)


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


def test_iteration_count_selector_defaults_to_one_and_offers_one_through_four(
    viewer,
):
    assert viewer._iteration_count == 1
    assert set(viewer._iteration_actions) == {1, 2, 3, 4}
    assert viewer._iteration_actions[1].isChecked()
    assert all(
        viewer._iteration_actions[count].isCheckable()
        for count in range(1, 5)
    )

    viewer._iteration_actions[4].trigger()

    assert viewer._iteration_count == 4
    assert viewer._iteration_actions[4].isChecked()
    assert "4 complete iterations" in viewer.statusBar().currentMessage()


def test_setting_selection_preserves_mesh_and_last_result_feedback(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    viewer.subdivide_selected()
    current_mesh = viewer._mesh
    result_summary = viewer._last_subdivision_summary
    result_label = viewer._result_label.text()

    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()
    viewer._iteration_actions[3].trigger()

    assert viewer._mesh is current_mesh
    assert viewer._last_subdivision_summary == result_summary
    assert viewer._result_label.text() == result_label
    assert "Subdivide mesh" in viewer._scheme_actions[
        SubdivisionScheme.BUTTERFLY
    ].toolTip()
    assert "press N" in viewer._iteration_actions[3].toolTip()
    assert "press N" in viewer.statusBar().currentMessage()


@pytest.mark.parametrize("iteration_count", [1, 2, 3, 4])
def test_subdivision_applies_selected_number_of_passes(viewer, iteration_count):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    initial_face_count = len(viewer._mesh.faces)
    viewer._iteration_actions[iteration_count].trigger()

    QTest.keyClick(viewer, Qt.Key.Key_N)

    assert viewer._mesh is not None
    assert viewer._mesh.revision == iteration_count
    assert len(viewer._mesh.faces) == initial_face_count * 4**iteration_count
    assert viewer._applied_iterations == iteration_count
    assert f"applied {iteration_count}" in viewer.statusBar().currentMessage()
    assert viewer._last_subdivision_summary == (
        f"Loop subdivision: applied {iteration_count} "
        f"{'pass' if iteration_count == 1 else 'passes'}; faces "
        f"{initial_face_count} -> {initial_face_count * 4**iteration_count}."
    )
    assert viewer._result_label.text() == viewer._last_subdivision_summary


def test_subdivide_menu_action_applies_selected_scheme_and_iterations(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    initial_face_count = len(viewer._mesh.faces)
    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()
    viewer._iteration_actions[2].trigger()

    viewer._subdivide_action.trigger()

    assert viewer._mesh is not None
    assert viewer._mesh.revision == 2
    assert len(viewer._mesh.faces) == initial_face_count * 16
    assert viewer._last_subdivision_summary == (
        f"Butterfly subdivision: applied 2 passes; faces "
        f"{initial_face_count} -> {initial_face_count * 16}."
    )


def test_loop_and_butterfly_can_be_compared_from_reset_baseline(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    initial_face_count = len(viewer._mesh.faces)

    viewer._scheme_actions[SubdivisionScheme.LOOP].trigger()
    viewer.subdivide_selected()
    loop_summary = viewer._last_subdivision_summary
    assert loop_summary.startswith("Loop subdivision:")
    assert f"faces {initial_face_count} -> {initial_face_count * 4}." in loop_summary

    viewer.reset_mesh()
    assert viewer._last_subdivision_summary is None

    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()
    viewer.subdivide_selected()
    butterfly_summary = viewer._last_subdivision_summary

    assert butterfly_summary.startswith("Butterfly subdivision:")
    assert (
        f"faces {initial_face_count} -> {initial_face_count * 4}."
        in butterfly_summary
    )


def test_failed_multi_pass_subdivision_keeps_displayed_mesh_unchanged(
    viewer, monkeypatch
):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    viewer.subdivide_selected()
    original_mesh = viewer._mesh
    last_summary = viewer._last_subdivision_summary
    result_label = viewer._result_label.text()
    viewer._iteration_actions[2].trigger()
    subdivide = viewer_module.subdivide_mesh
    calls = 0

    def fail_on_second_pass(mesh, scheme):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise RuntimeError("test failure")
        return subdivide(mesh, scheme)

    monkeypatch.setattr(viewer_module, "subdivide_mesh", fail_on_second_pass)
    monkeypatch.setattr(
        viewer_module.QMessageBox,
        "warning",
        lambda *args: None,
    )
    QTest.keyClick(viewer, Qt.Key.Key_N)

    assert calls == 2
    assert viewer._mesh is original_mesh
    assert viewer._applied_iterations == 1
    assert viewer._last_subdivision_summary == last_summary
    assert viewer._result_label.text() == result_label
    assert "Subdivision failed" in viewer.statusBar().currentMessage()


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


def test_reset_restores_loaded_mesh_and_preserves_selections(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    loaded_mesh = viewer._mesh
    viewer._iteration_actions[2].trigger()
    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()
    QTest.keyClick(viewer, Qt.Key.Key_N)
    assert viewer._applied_iterations == 2
    viewer._iteration_actions[3].trigger()

    QTest.keyClick(viewer, Qt.Key.Key_R)

    assert viewer._mesh is loaded_mesh
    assert viewer._applied_iterations == 0
    assert viewer._last_subdivision_summary is None
    assert "no subdivision applied" in viewer._result_label.text()
    assert viewer._iteration_count == 3
    assert viewer._scheme is SubdivisionScheme.BUTTERFLY
    assert "0 subdivision iterations" in viewer.statusBar().currentMessage()


def test_reset_after_separate_subdivision_actions_restores_loaded_mesh(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    loaded_mesh = viewer._mesh

    QTest.keyClick(viewer, Qt.Key.Key_N)
    QTest.keyClick(viewer, Qt.Key.Key_N)

    assert viewer._mesh is not loaded_mesh
    assert viewer._applied_iterations == 2

    QTest.keyClick(viewer, Qt.Key.Key_R)

    assert viewer._mesh is loaded_mesh
    assert viewer._applied_iterations == 0


def test_reset_when_already_loaded_is_a_no_op(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    loaded_mesh = viewer._mesh

    viewer._reset_action.trigger()

    assert viewer._mesh is loaded_mesh
    assert viewer._applied_iterations == 0
    assert "already at its loaded state" in viewer.statusBar().currentMessage()


def test_successful_load_replaces_reset_target(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    viewer.subdivide_selected()
    assert viewer._last_subdivision_summary is not None

    viewer.load_mesh_path("tests/fixtures/triangle_mesh.obj")
    loaded_mesh = viewer._mesh
    assert viewer._last_subdivision_summary is None
    assert viewer._result_label.text() == (
        f"Loaded mesh: {len(loaded_mesh.faces)} faces; no subdivision applied."
    )

    viewer._iteration_actions[2].trigger()
    viewer.subdivide_selected()

    viewer.reset_mesh()

    assert viewer._mesh is loaded_mesh
    assert viewer._applied_iterations == 0
    assert viewer._last_subdivision_summary is None


def test_subdivision_and_reset_without_mesh_report_required_action(viewer):
    viewer.subdivide_selected()
    assert "Load a valid mesh" in viewer.statusBar().currentMessage()
    assert viewer._mesh is None

    viewer.reset_mesh()
    assert "Load a valid mesh" in viewer.statusBar().currentMessage()
    assert viewer._mesh is None


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
