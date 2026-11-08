# Research: Automatically Apply Iteration Changes

## Existing Project Findings

- `MeshViewerWindow` in `src/mesh_subdivision_viewer/viewer.py` already owns
  the slider, selected count, applied count, selected scheme, applied scheme,
  loaded-mesh baseline, and success feedback.
- The slider range is 0–4 and starts at zero. `_update_iteration_count`
  currently changes only the selection label and status text.
- The `+` and `-` actions adjust the slider, so connecting automatic
  application to the slider's `valueChanged` signal will also cover keyboard
  adjustments without duplicating the behavior.
- `_select_scheme` currently changes only the selected scheme and feedback.
- `subdivide_selected` already supports positive total iteration counts:
  increases under the same scheme subdivide the current result for the
  difference; decreases and scheme changes recompute from `_loaded_mesh`.
- `subdivide_selected` computes into a local `refined` value and commits the
  mesh and applied state only after the requested subdivision calls succeed.
  Existing `ValueError` and `RuntimeError` handling reports failure and
  preserves the displayed mesh and successful summary.
- Zero currently returns without changing the displayed mesh or applied
  count. Reset is a distinct command and restores the loaded baseline while
  preserving selected controls.
- The scheme and count selection status/tooltips currently instruct users to
  press `N`; the README and existing feature quickstart similarly describe
  manual application and need to be aligned with the new behavior.
- `tests/test_viewer.py` covers slider/keyboard selection, explicit
  application, scheme comparison, reset, and failure handling. Several
  existing tests explicitly expect selection alone to leave the mesh
  unchanged and will need to be revised for automatic application.
- No dependencies or public interfaces are required.

## Decisions

### Apply through the existing subdivision path

- **Decision**: Have positive slider changes invoke the existing
  `subdivide_selected` logic. Keep keyboard actions routed through the slider.
- **Rationale**: This reuses the established baseline selection, result
  feedback, and transactional error handling, and avoids a second code path.
- **Alternatives considered**: Add a separate automatic subdivision
  implementation; rejected because it duplicates state transitions and
  risks inconsistent mesh results.

### Recompute the same total, not extra iterations

- **Decision**: Treat the selected count as the desired total relative to the
  loaded mesh. Continue incrementally for increases under the same scheme,
  and recompute from the baseline for decreases or scheme changes.
- **Rationale**: This preserves existing count semantics and ensures changing
  schemes never mixes algorithms in one displayed result.
- **Alternatives considered**: Apply the selected count as additional
  iterations to the current mesh; rejected because repeated selection
  changes would compound and produce the wrong total.

### Keep zero selection non-destructive

- **Decision**: A transition to zero does not modify the mesh, applied count,
  or last successful result summary. Reset remains an explicit separate
  operation.
- **Rationale**: This is the behavior the user selected during clarification
  and the current specification requires it to remain distinct from reset.
- **Alternatives considered**: Treat zero as reset; rejected because the user
  explicitly requested that the current mesh remain unchanged.

### Recompute on a positive scheme change

- **Decision**: When the selected count is positive, a scheme change invokes
  the same subdivision path immediately; the path recomputes from the loaded
  baseline when the scheme differs from the one that produced the display.
- **Rationale**: The selected method should be reflected immediately in the
  mesh, without an additional `N` action.
- **Alternatives considered**: Keep scheme selection non-destructive until
  `N`; rejected because it conflicts with the feature request.

### Preserve explicit application as an optional action

- **Decision**: Keep `N` and the menu action, allowing them to reapply a
  positive selection, while no longer making them necessary after an
  iteration or scheme selection.
- **Rationale**: This avoids removing an existing user affordance and limits
  compatibility changes to the requested automatic behavior.
- **Alternatives considered**: Remove `N` and the menu action; rejected as
  unnecessary scope.
