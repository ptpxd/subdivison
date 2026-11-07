# Feature Specification: Subdivision Controls and Result Feedback

**Feature Branch**: `003-subdivision-feedback`

**Created**: 2026-11-07

**Status**: Draft

**Input**: User description: "A subdivision iterations és a subdivide mesh N között mi a különbség? Subdivison iterations -nál állítom a számokat, de változás nem történik, nem lesz több háló meg ilyenek. A Loop -ról Butterfly -ra váltok, akkor sem látok változást."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Understand and Apply Subdivision Settings (Priority: P1)

The user selects an iteration count and a subdivision method, understands that
these choices only configure the next operation, and explicitly starts
subdivision to update the displayed mesh.

**Why this priority**: Users currently mistake choosing settings for applying
them and cannot tell why changing methods alone leaves the mesh unchanged.
Explaining the two-step interaction is necessary to use subdivision correctly.

**Independent Test**: Load a mesh, change its iteration count and method, and
confirm the current mesh does not change until the user starts subdivision.
Then start subdivision and verify that the displayed mesh updates using the
selected settings.

**Acceptance Scenarios**:

1. **Given** a mesh is loaded, **When** the user selects an iteration count or
   subdivision method, **Then** the selected values are apparent and the UI
   explains that a separate subdivision action is required to apply them.
2. **Given** the user has selected an iteration count and method, **When** the
   user starts subdivision with the action or its shortcut, **Then** the
   selected number of complete passes is applied to the current mesh using the
   selected method.
3. **Given** subdivision has completed successfully, **When** the user views
   the operation feedback, **Then** it identifies the method, number of passes
   applied, and the mesh-size change.

### User Story 2 - Verify and Compare Subdivision Results (Priority: P2)

The user can tell that subdivision changed the mesh and can compare the
results of Loop and Butterfly by applying each method to the same original
mesh.

**Why this priority**: Clear result feedback makes the operation verifiable;
returning to the loaded mesh gives users a reliable way to compare methods
without relying on visual guesswork.

**Independent Test**: Apply each subdivision method to the same loaded mesh
after restoring the original, and verify that feedback identifies the chosen
method and reports the resulting mesh size.

**Acceptance Scenarios**:

1. **Given** a subdivision operation succeeds, **When** the result is shown,
   **Then** the viewer reports the selected method, the number of passes, and
   the before-and-after face counts.
2. **Given** the user wants to compare methods, **When** they restore the
   loaded mesh, select the other method, and subdivide, **Then** the new
   operation uses the newly selected method and the feedback identifies it.
3. **Given** an operation fails, **When** the viewer reports the failure,
   **Then** the previous mesh remains displayed and no successful-operation
   feedback is shown for the failed attempt.

### Edge Cases

- Selecting a count or method without starting subdivision changes settings
  only and must not alter mesh geometry or displayed mesh statistics.
- If no mesh is loaded, starting subdivision does not change mesh state and
  the viewer explains that a mesh must be loaded first.
- The displayed before-and-after counts accurately describe the mesh for the
  whole requested operation, not an intermediate pass.
- Switching the selected method does not retroactively alter an already
  displayed mesh.
- Resetting before comparing methods returns to the most recently loaded mesh.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The viewer MUST distinguish the iteration-count and
  subdivision-method controls from the action that applies subdivision.
- **FR-002**: The viewer MUST explain that selecting an iteration count or
  method configures a future operation and does not immediately modify the
  displayed mesh.
- **FR-003**: The viewer MUST identify the action and shortcut that apply the
  selected subdivision settings.
- **FR-004**: A successful subdivision MUST apply the selected method and
  number of complete passes to the currently displayed mesh.
- **FR-005**: After a successful operation, the viewer MUST report the
  selected method and the number of passes applied.
- **FR-006**: After a successful operation, the viewer MUST report the mesh
  face count before and after the operation.
- **FR-007**: Selecting a different subdivision method MUST affect future
  operations only; it MUST NOT silently alter the currently displayed mesh.
- **FR-008**: A failed subdivision MUST leave the previously displayed mesh
  and its successful-operation statistics unchanged and MUST report the
  failure.
- **FR-009**: The viewer MUST provide a clear explanation if the user attempts
  subdivision before loading a valid mesh.

### Key Entities *(include if feature involves data)*

- **Subdivision settings**: The selected method and number of passes for the
  next subdivision action; changing settings does not itself change the mesh.
- **Subdivision result feedback**: A user-visible summary of the successfully
  applied method, number of passes, and before-and-after face counts.
- **Displayed mesh**: The currently loaded or subdivided mesh; it changes only
  after a successful subdivision or an explicit reset/load action.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least four out of five first-time users correctly identify
  that selecting a method or iteration count only configures the next
  operation, and that the subdivision action applies it.
- **SC-002**: For every successful subdivision action, the viewer displays the
  correct selected method, applied pass count, and before-and-after face
  counts.
- **SC-003**: In a user check, all successful subdivision actions on the test
  meshes visibly update the mesh and provide feedback that lets the user
  confirm the operation completed.
- **SC-004**: Users can compare Loop and Butterfly results on the same loaded
  mesh by resetting and completing one subdivision action per method, without
  uncertainty about which method produced the displayed result.

## Assumptions

- The existing iteration-count range, default, subdivision schemes, and reset
  behavior remain unchanged.
- Selecting an iteration count or scheme is intentionally non-destructive;
  the user must invoke the subdivision action to change geometry.
- Mesh-size feedback uses face counts, which directly indicate the increase
  in triangular mesh detail; visual appearance can also depend on the input
  shape and display mode.
- Comparing schemes means applying each to the same loaded mesh state; scheme
  selection does not reprocess an existing result.
- Saving meshes and changing subdivision algorithms are out of scope.
