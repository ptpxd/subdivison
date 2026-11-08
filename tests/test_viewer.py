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


def test_iteration_slider_starts_at_zero_and_offers_zero_through_four(viewer):
    assert viewer._iteration_count == 0
    assert viewer.iteration_slider.minimum() == 0
    assert viewer.iteration_slider.maximum() == 4
    assert viewer.iteration_slider.value() == 0
    assert viewer.iteration_label.text() == "Selected iterations: 0"


def test_keyboard_adjusts_and_applies_positive_iteration_count(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    loaded_mesh = viewer._mesh

    QTest.keyClick(viewer, Qt.Key.Key_Plus)
    assert viewer._iteration_count == 1
    assert viewer.iteration_label.text() == "Selected iterations: 1"
    assert viewer._mesh is not loaded_mesh
    assert viewer._applied_iterations == 1

    QTest.keyClick(viewer, Qt.Key.Key_Minus)
    QTest.keyClick(viewer, Qt.Key.Key_Minus)
    assert viewer._iteration_count == 0
    assert viewer._applied_iterations == 1

    for _ in range(5):
        QTest.keyClick(viewer, Qt.Key.Key_Plus)

    assert viewer._iteration_count == 4
    assert viewer.iteration_slider.value() == 4
    assert viewer._mesh is not loaded_mesh
    assert viewer._applied_iterations == 4
    assert viewer._mesh.revision == 4


def test_iteration_selection_applies_mesh_and_reports_result(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    loaded_mesh = viewer._mesh

    viewer.iteration_slider.setValue(4)

    assert viewer._mesh is not loaded_mesh
    assert viewer._applied_iterations == 4
    assert viewer.iteration_label.text() == "Selected iterations: 4"
    assert "Loop subdivision: applied 4 iterations" in viewer.statusBar().currentMessage()
    assert "faces" in viewer.statusBar().currentMessage()


def test_zero_selected_iterations_do_not_change_subdivided_mesh(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    viewer.iteration_slider.setValue(2)
    current_mesh = viewer._mesh
    last_summary = viewer._last_subdivision_summary
    result_label = viewer._result_label.text()

    viewer.iteration_slider.setValue(0)
    viewer._subdivide_action.trigger()

    assert viewer._mesh is current_mesh
    assert viewer._applied_iterations == 2
    assert viewer._last_subdivision_summary == last_summary
    assert viewer._result_label.text() == result_label
    assert "No subdivision applied" in viewer.statusBar().currentMessage()


def test_scheme_change_at_zero_does_not_change_displayed_mesh(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    viewer.iteration_slider.setValue(2)
    viewer.iteration_slider.setValue(0)
    current_mesh = viewer._mesh
    result_summary = viewer._last_subdivision_summary

    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()

    assert viewer._scheme is SubdivisionScheme.BUTTERFLY
    assert viewer._mesh is current_mesh
    assert viewer._applied_iterations == 2
    assert viewer._last_subdivision_summary == result_summary


def test_reapplying_same_count_and_reducing_count_report_applied_state(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    initial_face_count = len(viewer._mesh.faces)
    viewer.iteration_slider.setValue(4)
    four_iteration_mesh = viewer._mesh
    successful_summary = viewer._last_subdivision_summary

    viewer._subdivide_action.trigger()

    assert viewer._mesh is four_iteration_mesh
    assert viewer._applied_iterations == 4
    assert viewer._last_subdivision_summary == successful_summary
    assert "4 iterations already applied" in viewer.statusBar().currentMessage()
    assert "applied 0" not in viewer.statusBar().currentMessage()

    viewer.iteration_slider.setValue(2)

    assert viewer._applied_iterations == 2
    assert viewer._mesh is not four_iteration_mesh
    assert len(viewer._mesh.faces) == initial_face_count * 4**2
    assert "applied 2 iterations" in viewer._last_subdivision_summary


def test_iteration_and_scheme_selection_apply_immediately(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    viewer.iteration_slider.setValue(1)
    loop_mesh = viewer._mesh

    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()
    butterfly_mesh = viewer._mesh
    viewer.iteration_slider.setValue(3)

    assert viewer._mesh is not loop_mesh
    assert viewer._mesh is not butterfly_mesh
    assert viewer._applied_scheme is SubdivisionScheme.BUTTERFLY
    assert viewer._applied_iterations == 3
    assert "Press N to reapply" in viewer._scheme_actions[
        SubdivisionScheme.BUTTERFLY
    ].toolTip()


@pytest.mark.parametrize("iteration_count", [1, 2, 3, 4])
def test_subdivision_applies_selected_number_of_iterations(viewer, iteration_count):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    initial_face_count = len(viewer._mesh.faces)
    viewer.iteration_slider.setValue(iteration_count)
    automatic_summary = viewer._last_subdivision_summary

    QTest.keyClick(viewer, Qt.Key.Key_N)

    assert viewer._mesh is not None
    assert viewer._mesh.revision == iteration_count
    assert len(viewer._mesh.faces) == initial_face_count * 4**iteration_count
    assert viewer._applied_iterations == iteration_count
    assert viewer.statusBar().currentMessage() == (
        f"Loop subdivision: {iteration_count} "
        f"{'iteration' if iteration_count == 1 else 'iterations'} already applied."
    )
    assert automatic_summary == (
        f"Loop subdivision: applied {iteration_count} "
        f"{'iteration' if iteration_count == 1 else 'iterations'}; faces "
        f"{initial_face_count} -> {initial_face_count * 4**iteration_count}."
    )
    assert viewer._last_subdivision_summary == (
        f"Loop subdivision: applied {iteration_count} "
        f"{'iteration' if iteration_count == 1 else 'iterations'}; faces "
        f"{initial_face_count} -> {initial_face_count * 4**iteration_count}."
    )
    assert viewer._result_label.text() == viewer._last_subdivision_summary


def test_subdivide_menu_action_applies_selected_scheme_and_iterations(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    initial_face_count = len(viewer._mesh.faces)
    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()
    viewer.iteration_slider.setValue(2)

    viewer._subdivide_action.trigger()

    assert viewer._mesh is not None
    assert viewer._mesh.revision == 2
    assert len(viewer._mesh.faces) == initial_face_count * 16
    assert viewer._last_subdivision_summary == (
        f"Butterfly subdivision: applied 2 iterations; faces "
        f"{initial_face_count} -> {initial_face_count * 16}."
    )


def test_loop_and_butterfly_can_be_compared_from_reset_baseline(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    initial_face_count = len(viewer._mesh.faces)
    viewer.iteration_slider.setValue(1)

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


def test_scheme_change_preserves_iterations_and_n_recomputes_from_loaded_mesh(
    viewer,
):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    initial_face_count = len(viewer._mesh.faces)
    viewer.iteration_slider.setValue(2)
    loop_mesh = viewer._mesh

    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()

    assert viewer._iteration_count == 2
    assert viewer.iteration_slider.value() == 2
    assert viewer._mesh is not loop_mesh
    assert viewer._applied_scheme is SubdivisionScheme.BUTTERFLY
    assert viewer._applied_iterations == 2

    butterfly_mesh = viewer._mesh
    QTest.keyClick(viewer, Qt.Key.Key_N)

    assert viewer._mesh is butterfly_mesh
    assert viewer._applied_iterations == 2
    assert viewer._applied_scheme is SubdivisionScheme.BUTTERFLY
    assert len(viewer._mesh.faces) == initial_face_count * 4**2
    assert viewer._last_subdivision_summary == (
        f"Butterfly subdivision: applied 2 iterations; faces "
        f"{initial_face_count * 4**2} -> {initial_face_count * 4**2}."
    )


def test_failed_multi_pass_subdivision_keeps_displayed_mesh_unchanged(
    viewer, monkeypatch
):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    viewer.iteration_slider.setValue(1)
    original_mesh = viewer._mesh
    last_summary = viewer._last_subdivision_summary
    result_label = viewer._result_label.text()
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
    viewer.iteration_slider.setValue(3)

    assert calls == 2
    assert viewer._mesh is original_mesh
    assert viewer._applied_iterations == 1
    assert viewer._last_subdivision_summary == last_summary
    assert viewer._result_label.text() == result_label
    assert "Subdivision failed" in viewer.statusBar().currentMessage()


def test_failed_scheme_change_keeps_displayed_mesh_unchanged(viewer, monkeypatch):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    viewer.iteration_slider.setValue(1)
    original_mesh = viewer._mesh
    last_summary = viewer._last_subdivision_summary
    result_label = viewer._result_label.text()

    def fail_subdivision(mesh, scheme):
        raise RuntimeError("test failure")

    monkeypatch.setattr(
        viewer_module,
        "subdivide_mesh",
        fail_subdivision,
    )
    monkeypatch.setattr(viewer_module.QMessageBox, "warning", lambda *args: None)

    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()

    assert viewer._scheme is SubdivisionScheme.BUTTERFLY
    assert viewer._mesh is original_mesh
    assert viewer._applied_scheme is SubdivisionScheme.LOOP
    assert viewer._applied_iterations == 1
    assert viewer._last_subdivision_summary == last_summary
    assert viewer._result_label.text() == result_label
    assert "Subdivision failed" in viewer.statusBar().currentMessage()


def test_keyboard_toggles_display_and_preserves_it_after_subdivision(viewer):
    viewer.load_mesh_path("tests/fixtures/tetrahedron_ascii.stl")
    viewer.iteration_slider.setValue(1)
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
    viewer.iteration_slider.setValue(2)
    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()
    QTest.keyClick(viewer, Qt.Key.Key_N)
    assert viewer._applied_iterations == 2
    viewer.iteration_slider.setValue(3)

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

    viewer.iteration_slider.setValue(1)
    QTest.keyClick(viewer, Qt.Key.Key_N)
    viewer.iteration_slider.setValue(2)
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
    viewer.iteration_slider.setValue(1)
    viewer.subdivide_selected()
    assert viewer._last_subdivision_summary is not None

    viewer.load_mesh_path("tests/fixtures/triangle_mesh.obj")
    loaded_mesh = viewer._mesh
    assert viewer._last_subdivision_summary is None
    assert viewer._result_label.text() == (
        f"Loaded mesh: {len(loaded_mesh.faces)} faces; no subdivision applied."
    )

    viewer.iteration_slider.setValue(2)
    viewer.subdivide_selected()

    viewer.reset_mesh()

    assert viewer._mesh is loaded_mesh
    assert viewer._applied_iterations == 0
    assert viewer._last_subdivision_summary is None


def test_subdivision_and_reset_without_mesh_report_required_action(viewer):
    viewer.subdivide_selected()
    assert "Load a valid mesh" in viewer.statusBar().currentMessage()
    assert viewer._mesh is None

    viewer.iteration_slider.setValue(2)
    assert "Load a valid mesh" in viewer.statusBar().currentMessage()
    assert viewer._mesh is None
    assert viewer._applied_iterations == 0

    viewer.iteration_slider.setValue(0)
    assert "load a valid mesh" in viewer.statusBar().currentMessage().lower()
    viewer._scheme_actions[SubdivisionScheme.BUTTERFLY].trigger()
    assert "Load a valid mesh" in viewer.statusBar().currentMessage()

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
