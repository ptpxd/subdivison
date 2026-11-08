# Tasks: Automatically Apply Iteration Changes

**Input**: Design documents from
`/specs/005-auto-apply-iterations/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md),
[research.md](research.md), [data-model.md](data-model.md),
[quickstart.md](quickstart.md)

**Tests**: Extend focused pytest coverage in `tests/test_viewer.py` for
automatic iteration and scheme changes, zero-selection behavior, feedback,
and transactional failures.

**Organization**: Tasks are grouped by user story. US1 covers automatic
application on positive iteration changes; US2 covers automatic
scheme-driven recomputation. Shared viewer state and documentation are
handled in the cross-cutting phase.

## Phase 1: Setup

**Purpose**: No setup changes are required; the application and Qt test
infrastructure already exist.

## Phase 2: Foundational

**Purpose**: No shared blocking infrastructure is required. Existing viewer
state and subdivision operations support the requested transitions.

---

## Phase 3: User Story 1 - Apply Iteration Changes Immediately (Priority: P1)

**Goal**: Automatically apply a positive selected iteration total when it is
changed by slider or keyboard, without requiring `N`.

**Independent Test**: Load a mesh, change the slider and keyboard-selected
count to positive values, and verify that the displayed mesh, applied count,
and result feedback update immediately. Verify that selecting zero preserves
the current displayed mesh and applied state.

### Implementation

- [X] T001 [US1] Connect positive iteration selection changes to the existing
  subdivision operation in `src/mesh_subdivision_viewer/viewer.py`; preserve
  zero as a no-op and keep `N` as an optional reapply action.
- [X] T002 [US1] Ensure changed positive counts represent the desired total
  relative to the loaded mesh, recomputing from baseline when decreasing and
  preserving transactional mesh and result state on failure in
  `src/mesh_subdivision_viewer/viewer.py`.
- [X] T003 [US1] Update selection and status feedback to describe automatic
  application rather than requiring `N` in
  `src/mesh_subdivision_viewer/viewer.py`.
- [X] T004 [US1] Add or update tests proving slider and `+`/`-` changes apply
  positive counts immediately, maintain the 0–4 range, preserve mesh and
  applied state at zero, and retain the prior result after failure in
  `tests/test_viewer.py`.

**Checkpoint**: A positive slider or keyboard selection updates the mesh
immediately; zero does not reset or otherwise change the displayed result.

---

## Phase 4: User Story 2 - Apply Scheme Changes Immediately (Priority: P1)

**Goal**: Immediately recompute the selected positive iteration total from
the loaded mesh when the selected scheme changes.

**Independent Test**: Apply a positive Loop result, switch to Butterfly
without changing the iteration count, and verify that the same total is
displayed using Butterfly from the loaded baseline. Verify switching at zero
does not modify the current mesh.

### Implementation

- [X] T005 [US2] Make a scheme change automatically apply the current positive
  iteration count using the newly selected scheme, while preserving zero
  no-op behavior, in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T006 [US2] Update scheme menu tooltips and status feedback to explain
  that a positive selection is applied immediately in
  `src/mesh_subdivision_viewer/viewer.py`.
- [X] T007 [US2] Add or update tests for immediate scheme recomputation from
  the loaded baseline, preserved iteration selection, zero-count scheme
  changes, and failure-state preservation in `tests/test_viewer.py`.

**Checkpoint**: Changing schemes at a positive selection updates the
displayed result immediately without requiring `N`.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Align user documentation with automatic application and verify
the feature.

- [X] T008 [P] Update `README.md` to document automatic positive iteration
  and scheme application, zero as a no-op, reset as a separate action, and
  optional `N` reapplication.
- [X] T009 [P] Update `specs/004-iteration-slider-zero-default/quickstart.md`
  to reflect automatic application and the zero-selection behavior.
- [X] T010 Run `uv run python -m pytest tests/test_viewer.py` and resolve
  feature-related failures in `src/mesh_subdivision_viewer/viewer.py` and
  `tests/test_viewer.py`.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No work required; project dependencies and test
  infrastructure already exist.
- **Foundational (Phase 2)**: No work required; existing viewer state and
  subdivision operations are sufficient.
- **User Story 1 (Phase 3)**: Can begin immediately.
- **User Story 2 (Phase 4)**: Depends on the shared automatic application
  path from US1.
- **Polish (Phase 5)**: Documentation follows the finalized interaction;
  focused tests validate the completed behavior.

### Within Each User Story

- Implement viewer behavior before adding corresponding interaction tests.
- Keep selected and applied iteration state distinct.
- Preserve transactional behavior: failed subdivision must not replace the
  displayed mesh or successful-result summary.

## Parallel Opportunities

- T008 and T009 can be handled independently because they update separate
  documentation files.
- The US2 implementation depends on the US1 application path and should
  follow it; tests for either story should validate the corresponding
  behavior after the implementation.

## Implementation Strategy

### MVP First

1. Complete T001–T004.
2. Verify slider and keyboard changes update positive counts immediately and
   zero leaves the current result unchanged.
3. Verify totals do not compound and failed updates preserve the last
   successful display.

### Incremental Delivery

1. Deliver US1 automatic iteration application.
2. Deliver US2 automatic scheme recomputation from the loaded baseline.
3. Update user documentation and run the focused viewer tests.

## Notes

- The existing subdivision function remains a one-iteration operation; the
  viewer invokes it for each requested iteration.
- No dependencies, APIs, or new test modules are required.
- `N` and the explicit subdivision action remain available, but are no
  longer required after changing the iteration count or scheme.
- Feature-focused validation passed: 24 tests passed. The full viewer module
  still has two unrelated failures in the wireframe actor options and
  three-mode display-cycle expectations.
