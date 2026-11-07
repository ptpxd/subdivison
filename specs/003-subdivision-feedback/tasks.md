# Tasks: Subdivision Controls and Result Feedback

**Input**: Design documents from `/specs/003-subdivision-feedback/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md)

**Tests**: Add focused pytest coverage for user-observable behavior as required by the project constitution and implementation plan.

**Organization**: Tasks are grouped by user story so users can understand and apply subdivision first, then verify and compare its results.

## Phase 1: Setup

**Purpose**: No setup changes are required; the application and Qt test infrastructure already exist.

## Phase 2: Foundational

**Purpose**: No shared blocking infrastructure is required. Existing viewer state and single-pass subdivision functions support the feature.

---

## Phase 3: User Story 1 - Understand and Apply Subdivision Settings (Priority: P1) 🎯 MVP

**Goal**: Make it clear that scheme and iteration choices configure the next operation, and that the user must explicitly invoke subdivision to change the mesh.

**Independent Test**: Load a mesh, change scheme and iteration count, verify neither selection changes the mesh, then invoke **Subdivide mesh** or press `N` and verify the selected settings are applied.

### Implementation

- [X] T001 [US1] Add concise status/tool-tip guidance to the scheme and iteration controls explaining that selections configure the next operation and require **Subdivide mesh** or `N` to apply, while keeping selection non-destructive in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T002 [US1] Add viewer tests proving scheme and iteration selection leave mesh geometry and successful-operation feedback unchanged until the subdivision action is invoked in `tests/test_viewer.py`.
- [X] T003 [US1] Verify the explicit menu action and `N` shortcut apply the selected method and the selected 1–4 complete passes to the currently displayed mesh in `tests/test_viewer.py`.

**Checkpoint**: Users can distinguish configuration from execution and explicitly apply their selected subdivision settings.

---

## Phase 4: User Story 2 - Verify and Compare Subdivision Results (Priority: P2)

**Goal**: Show the selected method, pass count, and before-and-after face counts after success, and make method comparison from the same loaded baseline verifiable.

**Independent Test**: Apply one scheme to a loaded mesh, inspect its result feedback, reset to the loaded mesh, select the other scheme, apply subdivision, and verify new feedback reflects the second operation and its actual face counts.

### Implementation

- [X] T004 [US2] Capture the current face count before subdivision and update successful status feedback only after every requested pass completes, reporting the scheme, number of passes, and before-and-after face counts in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T005 [US2] Ensure successful-operation feedback is cleared or no longer presented as describing the current mesh after a successful load or reset, without changing scheme or iteration selections in `src/mesh_subdivision_viewer/viewer.py`.
- [X] T006 [US2] Add viewer tests for exact before-and-after face-count feedback for one and multiple passes, and for comparing Loop and Butterfly from the same reset baseline in `tests/test_viewer.py`.
- [X] T007 [US2] Add a failure regression test proving a failed pass sequence retains the displayed mesh and last successful-operation feedback while reporting the failure in `tests/test_viewer.py`.

**Checkpoint**: Each successful operation is measurable and attributable to its selected method; failed operations do not masquerade as success.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Make the two-step workflow and measurable feedback discoverable in user documentation, then validate the focused behavior.

- [X] T008 [P] Explain that scheme and iteration selection are settings, that **Subdivide mesh** or `N` applies them, and how to read the result summary in `README.md`.
- [X] T009 [P] Update the manual and automated acceptance guidance for selection, operation feedback, failure retention, and comparing methods in `specs/003-subdivision-feedback/quickstart.md`.
- [X] T010 Run `uv run python -m pytest tests/test_viewer.py` and resolve any feature-related failures in `tests/test_viewer.py`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No work required; project dependencies and test infrastructure already exist.
- **Foundational (Phase 2)**: No work required; existing viewer state and subdivision operations are sufficient.
- **User Story 1 (Phase 3)**: Can begin immediately; no dependency on another story.
- **User Story 2 (Phase 4)**: Can begin after Phase 2; sequenced after US1 because both stories update the viewer and build on understanding the explicit subdivision action.
- **Polish (Phase 5)**: Depends on the user stories so documentation and focused verification cover the final behavior.

### User Story Dependencies

- **User Story 1 (P1)**: No dependency on another user story.
- **User Story 2 (P2)**: No functional dependency on US1; ordered after it to avoid overlapping changes to `src/mesh_subdivision_viewer/viewer.py`.

### Within Each User Story

- Implement behavior in `viewer.py` before adding or adjusting its focused viewer tests.
- Keep failure-state tests with the result-feedback behavior they validate.

## Parallel Opportunities

- **US1**: No parallel tasks are marked; implementation and behavior tests touch the same viewer interactions.
- **US2**: No parallel tasks are marked; result feedback and its tests are closely coupled.
- **Polish**: T008 and T009 can run in parallel because they update separate documentation files.

## Parallel Example: Polish

```text
Task: T008 Update README.md usage guidance
Task: T009 Update specs/003-subdivision-feedback/quickstart.md validation guide
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001–T003.
2. Verify setting changes do not alter the mesh or successful-result summary.
3. Verify the explicit action and `N` shortcut apply the chosen method and pass count.

### Incremental Delivery

1. Deliver US1 so the two-step selection/application workflow is understandable and usable.
2. Deliver US2 with face-count feedback, failure-state correctness, and same-baseline method comparison.
3. Update documentation and run the focused viewer tests.

## Notes

- Every task follows the required checkbox, sequential ID, optional parallel marker, user-story label where applicable, and exact file path format.
- `subdivide_mesh` remains a one-pass operation; the viewer invokes it for each selected pass.
- No new dependencies, APIs, or contracts are required.
