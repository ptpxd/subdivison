# Tasks: Subdivision Iteration Controls and Reset

**Input**: Design documents from `/specs/002-subdivision-controls/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md)

**Tests**: Add focused coverage in the existing pytest modules as part of implementation, following the project constitution and the validation scenarios in the design.

**Organization**: Tasks are grouped by user story so iteration selection and reset can be implemented and verified as separate increments.

## Phase 1: Setup

**Purpose**: No setup changes are required; the Python application, Qt UI, and pytest structure already exist.

## Phase 2: Foundational

**Purpose**: No shared blocking infrastructure is required. Existing `subdivide_mesh` performs one validated pass and the viewer already manages loaded mesh state.

---

## Phase 3: User Story 1 - Choose Subdivision Iterations (Priority: P1) 🎯 MVP

**Goal**: Let the user select one through four complete subdivision passes, default to one, and explain what an iteration does.

**Independent Test**: Load a mesh, select counts 1–4, apply subdivision, and verify that each selection performs exactly that many successive passes on the current mesh; confirm one pass remains the default and the UI explains that a pass processes the complete mesh.

### Implementation

- [X] T001 [US1] Add an exclusive 1–4 iteration-count selector defaulting to 1, clarify the subdivision action as complete passes, apply the selected number of passes successively, and report successful applied iterations in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T002 [US1] Add viewer and subdivision coverage for the default and allowed iteration counts, successive-pass results, and unchanged displayed mesh when a requested multi-pass action fails in `tests/test_viewer.py` and `tests/test_subdivision.py`.

**Checkpoint**: User Story 1 works independently with existing mesh loading and subdivision schemes.

---

## Phase 4: User Story 2 - Reset Subdivision (Priority: P2)

**Goal**: Restore the mesh state from the latest successful file load with one reset action, while retaining the selected scheme and iteration count.

**Independent Test**: Load a mesh, subdivide it, reset, and verify that the original loaded mesh and zero-applied-iteration state return without reopening the file; confirm the selected scheme and iteration count are retained.

### Implementation

- [X] T003 [US2] Retain the latest successfully loaded mesh as the reset target and add a reset action that restores it, reports zero applied iterations, preserves scheme and count selections, and handles no-mesh and already-reset cases in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T004 [US2] Add viewer coverage for reset after multiple subdivision actions, reset before subdivision, selection retention, successful-load replacement of the reset target, and no-mesh feedback in `tests/test_viewer.py`.

**Checkpoint**: User Story 2 restores the original loaded mesh without affecting iteration or scheme selections.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Align user-facing usage guidance with the new controls and run the focused validation suite.

- [X] T005 [P] Document iteration selection, the meaning of one complete subdivision pass, and reset behavior in `README.md`.
- [X] T006 [P] Update the manual acceptance steps and expected automated checks for iteration selection and reset in `specs/002-subdivision-controls/quickstart.md`.
- [X] T007 Run the focused feature validation command `uv run python -m pytest tests/test_subdivision.py tests/test_viewer.py` and resolve any failures in `tests/test_subdivision.py` or `tests/test_viewer.py`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No work required; project structure and dependencies already exist.
- **Foundational (Phase 2)**: No work required; existing mesh and viewer foundations are sufficient.
- **User Story 1 (Phase 3)**: Can begin immediately; no dependency on another feature story.
- **User Story 2 (Phase 4)**: Functionally independent of User Story 1, but scheduled after it because both stories update `src/mesh_subdivision_viewer/viewer.py`.
- **Polish (Phase 5)**: Depends on both stories so the docs and focused validation reflect the completed behavior.

### User Story Dependencies

- **User Story 1 (P1)**: No dependency on another user story.
- **User Story 2 (P2)**: No functional dependency on User Story 1; implementation is sequenced after US1 to avoid concurrent edits to the same viewer module.

### Within Each User Story

- Implement the behavior before adding its focused regression coverage.
- User Story 2 reset coverage follows the reset action implementation.

## Parallel Opportunities

- **US1**: No implementation tasks are marked parallel because behavior and coverage are coupled through the viewer.
- **US2**: No implementation tasks are marked parallel because behavior and coverage are coupled through the viewer.
- **Polish**: T005 and T006 can run in parallel because they update separate documentation files.

## Parallel Example: Polish

```text
Task: T005 Update README.md usage guidance
Task: T006 Update specs/002-subdivision-controls/quickstart.md acceptance checks
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001 and T002.
2. Verify the one-pass default and each selectable count.
3. Demonstrate that each requested pass refines the preceding result and that the UI explains the complete-pass behavior.

### Incremental Delivery

1. Deliver User Story 1 as the MVP: configurable subdivision count with clear terminology.
2. Add User Story 2: reset to the latest successfully loaded mesh.
3. Update usage guides and run the focused pytest suite.

## Notes

- Every task uses the required checkbox, sequential ID, optional parallel marker, and user-story label where applicable.
- User Story tasks identify exact implementation or test file paths.
- `subdivide_mesh` remains a one-pass operation; the viewer repeats it for the selected count.

## Phase 6: Convergence

- [X] T008 Add a viewer regression test that performs subdivision in separate user actions, then resets and verifies the loaded mesh and zero applied-iteration count in `tests/test_viewer.py` per US2/AC1 (partial)
