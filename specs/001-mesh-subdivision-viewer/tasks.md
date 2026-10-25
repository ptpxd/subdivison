# Tasks: Mesh Subdivision Viewer

**Input**: Design documents from `/specs/001-mesh-subdivision-viewer/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to support incremental implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Tasks operate on separate files and can be performed in parallel.
- **[Story]**: Maps a task to its user story; setup, foundational, and polish tasks
  have no story label.
- Every task includes the exact file path or paths to change.

## Phase 1: Setup

**Purpose**: Create the minimal Python application package and its dependencies.

- [X] T001 Create `pyproject.toml` with Python 3.11+, runtime dependencies `pyvista`, `pyvistaqt`, and `PySide6`, and the development dependency `pytest`.
- [X] T002 [P] Create `src/mesh_subdivision_viewer/__init__.py` and `src/mesh_subdivision_viewer/__main__.py` as the package and application entry point.

## Phase 2: Foundational

**Purpose**: Implement and verify the half-edge data model required by loading and subdivision.

- [X] T003 Implement `HalfEdge`, `Face`, and `HalfEdgeMesh` plus construction and connectivity validation in `src/mesh_subdivision_viewer/mesh.py`; require three valid vertices per face, one or two incident faces per undirected edge, reversed direction for twins, and reject non-finite vertices, invalid indices, duplicate directed edges, and non-manifold edges.
- [X] T004 Add `tests/test_mesh.py` coverage for triangular face loops, valid twin and boundary links, disconnected components, and every invalid-connectivity rejection defined in `specs/001-mesh-subdivision-viewer/data-model.md`.

**Checkpoint**: Half-edge connectivity can be constructed and validated independently of the GUI.

## Phase 3: User Story 1 - Load and Inspect a Mesh (Priority: P1) 🎯 MVP

**Goal**: Load STL and OBJ meshes into the half-edge representation and inspect them in an interactive fitted view.

**Independent Test**: Open valid STL and OBJ files, verify each is fitted in the viewer and can be rotated and zoomed; attempt an invalid file and verify the viewer stays usable.

### Implementation

- [X] T005 [P] [US1] Create four small test fixtures at `tests/fixtures/tetrahedron_ascii.stl`, `tests/fixtures/tetrahedron_binary.stl`, `tests/fixtures/triangle_mesh.obj`, and `tests/fixtures/polygon_mesh.obj`; include an OBJ face with more than three vertices to verify triangulation.
- [X] T006 [US1] Implement STL/OBJ loading, polygon triangulation, conversion to `HalfEdgeMesh`, and clear invalid-file/topology errors in `src/mesh_subdivision_viewer/mesh.py`.
- [X] T007 [US1] Add `tests/test_io.py` cases for all four fixtures, triangle output after OBJ triangulation, and graceful errors for empty, malformed, unreadable, and unsupported-topology inputs.
- [X] T008 [US1] Implement the PySide6 main window, file-open menu, PyVistaQt `QtInteractor`, fitted mesh display, and standard mouse rotation/zoom in `src/mesh_subdivision_viewer/viewer.py`.

**Checkpoint**: User Story 1 is usable without subdivision; invalid opens do not terminate the viewer.

## Phase 4: User Story 2 - Refine a Mesh (Priority: P2)

**Goal**: Select Loop or Butterfly and apply exactly one subdivision iteration to the current mesh per key press.

**Independent Test**: Load a valid mesh, select each scheme, press the iteration key once, and verify that the current mesh is refined and remains valid in the half-edge representation.

### Implementation

- [X] T009 [P] [US2] Add `tests/test_subdivision.py` cases verifying one Loop and one Butterfly iteration, one further iteration on the current result, component preservation, and no state change after a failed refinement.
- [X] T010 [US2] Implement the subdivision service in `src/mesh_subdivision_viewer/subdivision.py`; apply the selected PyVista Loop or Butterfly filter to each connected component, recombine results, rebuild and validate `HalfEdgeMesh`, and return one new mesh revision per call.
- [X] T011 [US2] Add a subdivision menu in `src/mesh_subdivision_viewer/viewer.py` with Loop and Butterfly choices and a visible checked current selection; default to Loop.
- [X] T012 [US2] Bind the documented iteration key in `src/mesh_subdivision_viewer/viewer.py` to exactly one call to the subdivision service; redraw the result while preserving the previous mesh if refinement fails.

**Checkpoint**: Both schemes are selectable and a single key press advances the current mesh by one validated iteration.

## Phase 5: User Story 3 - Switch Mesh Display (Priority: P3)

**Goal**: Switch between wireframe and flat-shaded display with a key while preserving the chosen mode after refinement.

**Independent Test**: Load a mesh, toggle display modes repeatedly, refine it, and verify that the selected mode remains active.

### Implementation

- [X] T013 [P] [US3] Add `tests/test_viewer.py` checks for the default flat-shaded mode, mode alternation, and display-mode preservation when a mesh is redrawn.
- [X] T014 [US3] Implement wireframe and flat-shaded rendering states in `src/mesh_subdivision_viewer/viewer.py`; start each newly loaded mesh in flat-shaded mode.
- [X] T015 [US3] Bind the display-mode key and show both keyboard shortcuts in the viewer UI in `src/mesh_subdivision_viewer/viewer.py`; ensure changing or refining the mesh does not reset the selected display mode.

**Checkpoint**: The display key alternates the two required modes and the mode survives mesh updates.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify the integrated application against the acceptance workflow and document how to run it.

- [X] T016 Update `specs/001-mesh-subdivision-viewer/quickstart.md` with the implemented install, launch, keyboard controls, and expected error behavior.
- [X] T017 Run `uv run python -m pytest` and complete every manual acceptance check in `specs/001-mesh-subdivision-viewer/quickstart.md`; fix failures in the corresponding implementation or test files.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on package setup; blocks all stories because each story depends on validated mesh representation.
- **User Story 1 (Phase 3)**: Depends on the foundational half-edge mesh; delivers the first usable viewer.
- **User Story 2 (Phase 4)**: Depends on User Story 1's loadable, displayed mesh and the foundational half-edge representation.
- **User Story 3 (Phase 5)**: Depends on User Story 1's viewer; verify after User Story 2 integration so the display mode can be checked through refinement.
- **Polish (Phase 6)**: Depends on all three user stories.

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2; no dependency on other stories.
- **US2 (P2)**: Follows US1 to refine a mesh loaded and displayed by the application.
- **US3 (P3)**: Follows US1 to display a loaded mesh; its preservation acceptance check also uses US2 refinement.

### Parallel Opportunities

- T002 can run alongside T001 because package entry files and dependency metadata are separate.
- T005 test fixtures and the T006 loader implementation can be developed independently after the half-edge model is defined.
- T009 subdivision tests can be authored in `tests/test_subdivision.py` separately from T010's implementation in `subdivision.py`.
- T013 display-mode tests can be authored separately from T014's viewer rendering changes.
- Story phases are sequenced for a complete runnable desktop application; do not parallelize tasks that edit the same `viewer.py` file.

## Parallel Example: User Story 2

```text
Task: T009 Add subdivision behavior cases in tests/test_subdivision.py
Task: T010 Implement subdivision in src/mesh_subdivision_viewer/subdivision.py
```

These tasks use separate files and can proceed in parallel once the half-edge
conversion and expected subdivision behavior are agreed.

## Implementation Strategy

### MVP First (User Story 1)

1. Complete setup and foundational half-edge representation.
2. Complete User Story 1 file loading, conversion, and interactive display.
3. Validate STL/OBJ loading, rotation, zoom, and error handling independently.
4. Stop for a usable viewer before adding subdivision.

### Incremental Delivery

1. Add User Story 2 to refine the currently loaded mesh with either scheme.
2. Add User Story 3 to switch display mode and retain it through refinement.
3. Run the complete quickstart acceptance workflow.

## Notes

- Each task is written as `- [ ] T###`, with `[P]` only for separate-file work
  and `[US1]`/`[US2]`/`[US3]` only in user-story phases.
- Tests are included because the implementation plan explicitly selects pytest
  and the half-edge/subdivision requirements need repeatable verification.
- The implementation uses VTK subdivision filters rather than custom
  subdivision algorithms; the application's mesh connectivity is still
  represented and validated with half-edges.

## Phase 7: Convergence

- [X] T018 Verify mouse drag rotation and wheel zoom in the running desktop viewer, and document the observed result in `specs/001-mesh-subdivision-viewer/quickstart.md` per plan: manual GUI validation and US1/AC2 (partial).
- [X] T019 Add window-level tests in `tests/test_viewer.py` that toggle display mode and confirm it remains selected after subdivision per T013 and US3/AC1-2 (partial).
