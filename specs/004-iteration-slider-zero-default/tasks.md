# Tasks: Zero-Default Iteration Control

**Input**: Design documents from `/specs/004-iteration-slider-zero-default/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md)

**Tests**: Extend focused pytest coverage in the existing Qt viewer test module for iteration selection, application, scheme changes, and feedback.

**Organization**: Tasks are grouped by user story. US1 covers zero-default iteration selection and keyboard control; US2 clarifies selected versus applied iteration feedback; US3 ensures a changed subdivision scheme can be explicitly applied without reselecting iterations.

## Phase 1: Setup

**Purpose**: No setup changes are required; the application and Qt test infrastructure already exist.

## Phase 2: Foundational

**Purpose**: No shared blocking infrastructure is required. Existing viewer state and single-iteration subdivision functions support the feature.

---

## Phase 3: User Story 1 - Select Iterations from Zero (Priority: P1) 🎯 MVP

**Goal**: Start with zero iterations selected, use consistent iteration terminology, and adjust the selection with the slider or keyboard without changing the mesh.

**Independent Test**: Start the viewer at zero, change the selected count with the slider and `+`/`-`, verify selection changes without modifying the mesh, then press `N` to apply a positive count. Verify zero remains a no-op.

### Implementation

- [X] T001 [US1] Initialize the selected iteration count to zero and keep the slider range at 0–4 in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T002 [US1] Replace user-facing "pass" wording with "iteration" wording in the control label, status messages, and result feedback in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T003 [US1] Add `+` and `-` keyboard actions that adjust the selected iteration count by one within 0–4 without applying subdivision in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T004 [US1] Keep slider changes non-destructive, make zero-count subdivision a no-op, and apply positive selections through the explicit **Subdivide mesh** action and `N` in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T005 [US1] Add or update viewer tests for iteration terminology, keyboard increment/decrement and limits, non-destructive selection, zero-count no-op, and applying counts one through four in `tests/test_viewer.py`.

**Checkpoint**: The selected iteration count starts at zero, is adjustable by slider and keyboard, and changes the mesh only after explicit application.

---

## Phase 4: User Story 2 - Distinguish Selected and Applied Iterations (Priority: P2)

**Goal**: Make selected iteration feedback distinct from the iteration count represented by the displayed mesh and preserve the selection during reset.

**Independent Test**: Apply a positive iteration count, repeat the same operation, lower the selected count and reapply, then reset. Confirm feedback describes the applied state and reset preserves the selected count.

### Implementation

- [X] T006 [US2] Update status and result feedback to use iteration terminology and clearly describe the resulting applied count, including repeated-application and zero-selection messages, in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T007 [US2] Add or update tests for success feedback, repeated application, decreasing the selected count, zero-count no-op, and reset restoring zero applied iterations while preserving selection in `tests/test_viewer.py`.

**Checkpoint**: Users can distinguish selected from applied iterations after success, no-op, decrease, and reset.

---

## Phase 5: User Story 3 - Apply a Changed Subdivision Scheme (Priority: P1)

**Goal**: Preserve the selected iteration count when the scheme changes and let `N` apply that count with the newly selected scheme from the loaded mesh baseline.

**Independent Test**: Select and apply two Loop iterations, switch to Butterfly without moving the slider, then press `N`. Verify the displayed result reflects two Butterfly iterations from the loaded mesh.

### Implementation

- [X] T008 [US3] Preserve the selected iteration count and displayed mesh when the user changes Loop/Butterfly selection in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T009 [US3] Track which subdivision scheme produced the displayed result and, on explicit apply after a scheme change, recompute the selected iteration count from the loaded mesh using the newly selected scheme in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T010 [US3] Add viewer tests proving scheme selection preserves the iteration count and mesh, and `N` recomputes from the loaded baseline under the new scheme in `tests/test_viewer.py`.

**Checkpoint**: Switching schemes is non-destructive; explicit application uses the latest scheme and preserved iteration count.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Align user documentation with iteration terminology and validate the revised interaction.

- [X] T011 [P] Update `README.md` to describe the zero-default iteration slider, `+`/`-` selection, `N` application, and iteration terminology.
- [X] T012 [P] Update `specs/004-iteration-slider-zero-default/quickstart.md` to cover zero, keyboard selection, explicit application, scheme changes, and reset.
- [X] T013 Run `uv run python -m pytest tests/test_viewer.py` and resolve feature-related failures in `tests/test_viewer.py`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No work required; project dependencies and test infrastructure already exist.
- **Foundational (Phase 2)**: No work required; existing viewer state and subdivision operations are sufficient.
- **User Story 1 (Phase 3)**: Can begin immediately.
- **User Story 2 (Phase 4)**: Depends on the selection and application state defined in US1.
- **User Story 3 (Phase 5)**: Depends on US1's explicit apply action and US2's applied-state feedback; sequenced afterward to avoid conflicting edits to `viewer.py`.
- **Polish (Phase 6)**: Depends on all user stories so the README and test run match final behavior.

### Within Each User Story

- Implement viewer behavior before adding corresponding interaction tests.
- Keep keyboard selection and mesh application as separate transitions.
- Preserve transactional behavior: failed subdivision must not replace the displayed mesh or successful-result summary.

## Parallel Opportunities

- No implementation tasks are marked parallel because they update the same viewer module and Qt test module.
- T011 and T012 can be handled independently because they update separate documentation files.

## Implementation Strategy

### MVP First

1. Complete T001–T005.
2. Verify startup at zero and non-destructive slider/keyboard selection.
3. Verify zero is a no-op and `N` applies each supported positive iteration count.

### Incremental Delivery

1. Deliver US1's zero-default iteration selection and keyboard adjustment.
2. Deliver US2's consistent iteration feedback and reset coverage.
3. Deliver US3's scheme-aware reapplication from the loaded mesh.
4. Update the README and run the focused viewer tests.

## Notes

- Every task uses the required checkbox, sequential ID, user-story label, and exact file path format.
- The existing subdivision function remains a one-iteration operation; the viewer invokes it for each requested iteration.
- No new dependencies, APIs, or contracts are required.
- T001, T004, T008, and T012 describe behavior or guidance already present; the remaining tasks were completed for the revised specification.
- Feature-focused viewer tests passed (11 passed). The full viewer module had 22 passed and 2 unrelated display-mode expectation failures: the wireframe actor test omits its configured white color, and the keyboard-cycle test expects flat shading after two steps despite the existing three-mode cycle.
