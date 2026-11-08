# Tasks: Restore Loaded Mesh at Zero Iterations

**Input**: Feature specification from
`/specs/006-zero-iterations-restore-loaded-mesh/spec.md`

**Tests**: Update the focused Qt interaction tests in `tests/test_viewer.py`
for zero selection, reset, automatic positive iteration changes, removal of
the manual subdivision action, and failure-state preservation.

**Organization**: Tasks are grouped by user story. Shared viewer behavior,
menu cleanup, documentation, and validation are included where they support
the user stories.

## Phase 1: Setup

**Purpose**: No setup changes are required; the application and Qt test
infrastructure already exist.

## Phase 2: Foundational

**Purpose**: No shared blocking infrastructure is required. The loaded mesh,
selected count, applied count, and automatic subdivision path already exist.

---

## Phase 3: User Story 1 - Restore the Loaded Mesh at Zero (Priority: P1)

**Goal**: Make zero the total-count state that restores the loaded mesh, and
ensure decreases to positive totals continue to display the correct result.

**Independent Test**: Load a mesh, select two iterations, reduce to one and
then zero. Verify the one-iteration result is computed from the loaded mesh
and zero restores the loaded mesh with an applied count of zero.

### Implementation

- [X] T001 [US1] Change zero-selection handling in
  `src/mesh_subdivision_viewer/viewer.py` to restore `_loaded_mesh`, set the
  applied count to zero, clear the applied scheme and successful subdivision
  summary, refresh the displayed mesh and statistics, and report that the
  loaded mesh is displayed; preserve the selected scheme.
- [X] T002 [US1] Ensure reset in
  `src/mesh_subdivision_viewer/viewer.py` sets the selected count to zero and
  synchronizes the slider and label, as well as restoring the loaded mesh and
  clearing applied subdivision state; preserve the selected scheme.
- [X] T003 [US1] Update `tests/test_viewer.py` to verify slider and keyboard
  changes from two to one to zero restore the loaded mesh, clear subdivision
  feedback, set applied iterations to zero, and retain the selected scheme.
- [X] T004 [US1] Update reset tests in `tests/test_viewer.py` to verify the
  selected count and slider are zero after reset, and that no-mesh reset
  behavior remains safe.

**Checkpoint**: Selecting zero and invoking reset both display the original
loaded geometry with selected and applied counts at zero.

---

## Phase 4: User Story 2 - Keep Iteration and Display State Consistent (Priority: P1)

**Goal**: Keep selected count, applied count, geometry, and result feedback
consistent across zero selection, reset, mesh loading, and failed updates.

**Independent Test**: Exercise reset after a positive selection, then select a
positive count again; verify the slider and displayed result remain
synchronized. Confirm a failed positive update preserves the last successful
display and result summary.

### Implementation

- [X] T005 [US2] Update or add viewer tests in `tests/test_viewer.py` for
  reapplying a positive count after zero/reset and for preserving the last
  successful result on subdivision failure.
- [X] T006 [US2] Verify mesh-load transitions in
  `src/mesh_subdivision_viewer/viewer.py` keep the selected count, slider, and
  displayed baseline consistent with the chosen specification behavior; make
  a code change only if loading exposes a mismatch.

**Checkpoint**: Loaded, zero-iteration, reset, successful subdivision, and
failed subdivision states have consistent selected/applied/displayed values.

---

## Phase 5: User Story 3 - Use Automatic Iteration Application (Priority: P2)

**Goal**: Remove the redundant manual `N`/menu subdivision command while
retaining automatic iteration and scheme changes.

**Independent Test**: Change a positive count and scheme and verify the
display updates immediately. Confirm the Mesh menu has no **Subdivide mesh**
action, and the `N` shortcut no longer invokes subdivision.

### Implementation

- [X] T007 [US3] Remove the **Subdivide mesh** action and `N` shortcut from
  `src/mesh_subdivision_viewer/viewer.py`, and remove status/tool-tip text
  suggesting that pressing `N` reapplies the selected count.
- [X] T008 [US3] Update `tests/test_viewer.py` to remove tests that invoke the
  removed action and instead verify menu/shortcut removal and automatic
  positive-count and scheme application.

**Checkpoint**: Positive count and scheme changes still apply automatically;
no separate subdivision command is exposed.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Align user guidance with the behavior and validate the feature.

- [X] T009 [P] Update `README.md` to document that selecting zero restores the
  loaded mesh, reset clears selected and applied iterations, and subdivision
  changes apply automatically without an `N` command.
- [X] T010 [P] Add `specs/006-zero-iterations-restore-loaded-mesh/quickstart.md`
  with focused automated and manual acceptance checks for zero restoration,
  lower positive totals, reset, scheme changes, and failure handling.
- [X] T011 Run `uv run python -m pytest tests/test_viewer.py` and resolve
  feature-related failures in `src/mesh_subdivision_viewer/viewer.py` and
  `tests/test_viewer.py`.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No work required; project dependencies and test
  infrastructure already exist.
- **Foundational (Phase 2)**: No work required; existing viewer state is
  sufficient.
- **User Story 1 (Phase 3)**: Can begin immediately.
- **User Story 2 (Phase 4)**: Depends on the zero/reset state transitions in
  US1.
- **User Story 3 (Phase 5)**: Can proceed independently of zero/reset after
  confirming automatic positive application remains in place.
- **Polish (Phase 6)**: Documentation follows the finalized behavior;
  focused tests validate the completed implementation.

### Within Each User Story

- Implement the viewer state transitions before updating the corresponding
  behavior tests.
- Preserve transactional updates: a failed positive subdivision must not
  replace the last successful mesh or result summary.
- Keep the selected subdivision scheme when zero or reset restores the loaded
  mesh.

## Parallel Opportunities

- T009 and T010 update separate documentation files and can be completed in
  parallel after the behavior is settled.
- US3 menu cleanup can be implemented independently from the zero/reset
  transition, but tests and docs should reflect both changes.

## Implementation Strategy

### MVP First

1. Complete T001–T004.
2. Verify that reducing from two to one to zero displays the correct total
   and restores the loaded mesh at zero.
3. Verify reset synchronizes the slider, selected count, applied count, and
   displayed geometry.

### Incremental Delivery

1. Deliver zero-selection restoration and reset consistency.
2. Remove the redundant manual subdivision action and update interaction
   tests.
3. Update user documentation and run the focused viewer tests.

## Notes

- `subdivide_mesh` remains a one-iteration operation; the viewer's selected
  total continues to determine how many times it is called.
- No dependencies, algorithms, mesh formats, or public APIs need to change.
- Tests that expected zero to be a no-op or used `_subdivide_action` have been
  updated to match this specification.
- Validation: 52 tests pass. Two unrelated pre-existing viewer assertions
  still fail for wireframe actor color and the three-mode display cycle.
