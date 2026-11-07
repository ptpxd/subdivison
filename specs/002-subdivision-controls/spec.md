# Feature Specification: Subdivision Iteration Controls and Reset

**Feature Branch**: `002-subdivision-controls`

**Created**: 2026-11-07

**Status**: Draft

**Input**: User description: "oké a meglévő jó, viszont lehessen állítani iteráció mennyiséget is egytől négyig. ezt kis featuret add hozzá, valamint lehessen resetelni. mert jelenleg a subdivide once feature nem tudom, hogy mit takar?"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Choose Subdivision Iterations (Priority: P1)

The user chooses how many subdivision iterations to apply, from one to four,
then starts subdivision. The viewer makes clear that an iteration is one full
subdivision pass over the current mesh, so the existing "subdivide once"
behavior is understandable and the user knows what the selected count means.

**Why this priority**: Controlling the amount of refinement is the requested
core improvement, and clear wording makes the existing action understandable.

**Independent Test**: Load a mesh, apply subdivision with each available count,
and verify that the chosen number of successive passes is applied to the
displayed mesh.

**Acceptance Scenarios**:

1. **Given** a valid mesh is loaded, **When** the user views the subdivision
   controls, **Then** the iteration count can be set to each integer from one
   through four and the default is one.
2. **Given** an iteration count is selected, **When** the user starts
   subdivision, **Then** that number of full passes is applied successively to
   the currently displayed mesh using the selected subdivision scheme.
3. **Given** the subdivision action is available, **When** the user reads its
   label or accompanying help, **Then** it is clear that one iteration means
   one complete pass over the mesh, not one face or one individual action on a
   part of the mesh.

### User Story 2 - Reset Subdivision (Priority: P2)

The user restores the displayed mesh to the state it had immediately after
loading the source file, without having to reload the file.

**Why this priority**: Reset lets users recover quickly from excessive
refinement and compare their work with the original mesh.

**Independent Test**: Load a mesh, subdivide it, reset, and verify that the
original loaded shape is displayed again.

**Acceptance Scenarios**:

1. **Given** a loaded mesh has been subdivided, **When** the user selects reset,
   **Then** the viewer restores the mesh to its original loaded state and shows
   that no iterations are currently applied.
2. **Given** the loaded mesh is already in its original state, **When** the
   user selects reset, **Then** the mesh remains unchanged and the viewer
   remains usable.

### Edge Cases

- The iteration count cannot be set below one or above four.
- If no valid mesh is loaded, subdivision and reset do not change mesh state
  and the viewer explains that a mesh must be loaded first.
- Reset after several subdivision operations restores the original loaded mesh,
  not merely the state before the most recent operation.
- Reset does not discard the loaded mesh or change the selected subdivision
  scheme.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The viewer MUST let the user select an iteration count from one
  through four, inclusive.
- **FR-002**: The initial iteration count MUST be one to preserve the existing
  single-iteration behavior by default.
- **FR-003**: The viewer MUST explain in the subdivision control that one
  iteration is one complete subdivision pass over the current mesh.
- **FR-004**: When subdivision is started, the viewer MUST apply the selected
  number of iterations successively to the currently displayed mesh using the
  selected subdivision scheme.
- **FR-005**: The viewer MUST provide a reset action that restores the mesh to
  its state immediately after the source file was loaded.
- **FR-006**: After reset, the viewer MUST indicate that zero subdivision
  iterations are applied to the restored mesh.
- **FR-007**: If no valid mesh is loaded, subdivision and reset MUST leave mesh
  state unchanged and clearly explain that a mesh must be loaded first.
- **FR-008**: Reset MUST retain the loaded source mesh and the currently
  selected subdivision scheme.

### Key Entities *(include if feature involves data)*

- **Iteration count**: The number of complete subdivision passes requested for
  one subdivision action; its allowed values are one through four.
- **Loaded mesh state**: The mesh as it appeared immediately after loading the
  source file, used as the target state for reset.
- **Applied iteration count**: The number of subdivision passes currently
  reflected in the displayed mesh; reset returns it to zero.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can select and apply each supported iteration count
  (one through four), and the displayed mesh reflects exactly that many
  successive subdivision passes.
- **SC-002**: After any number of subdivision actions, one reset restores the
  same mesh shape as immediately after loading the source file.
- **SC-003**: At least four out of five first-time users can identify what one
  iteration means and complete a subdivision with a chosen count without
  assistance.
- **SC-004**: Users can return to the original loaded mesh with one reset
  action, without reopening the source file.

## Assumptions

- The selected iteration count applies to the next subdivision action; each
  pass refines the result of the preceding pass.
- The default count remains one so existing single-iteration usage is
  preserved.
- Reset returns to the mesh as first loaded, shows zero applied iterations,
  and retains the chosen iteration count and subdivision scheme.
- Existing subdivision schemes, file formats, and mesh viewing behavior remain
  unchanged.
- Saving meshes and undoing individual subdivision actions are out of scope.
