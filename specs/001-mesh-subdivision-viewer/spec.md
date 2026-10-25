# Feature Specification: Mesh Subdivision Viewer

**Feature Branch**: `001-mesh-subdivision-viewer`

**Created**: 2026-10-25

**Status**: Draft

**Input**: User description: "Create software that loads a triangulated shape from an STL or OBJ file, lets the user rotate and zoom it, refine it using Loop or Butterfly subdivision selected from a menu, start each new iteration with a key press, switch between wireframe and flat-shaded display with a key, and use an edge-based data structure (half-edge or winged-edge, whichever is simpler)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Load and Inspect a Mesh (Priority: P1)

The user opens a supported STL or OBJ file and inspects the resulting triangular
shape by rotating and zooming the view.

**Why this priority**: Loading and inspecting a shape is the foundation for all
subdivision and display workflows.

**Independent Test**: Open one valid STL and one valid OBJ model, and verify that
each is displayed and can be rotated and zoomed.

**Acceptance Scenarios**:

1. **Given** the viewer is open, **When** the user opens a valid STL or OBJ mesh,
   **Then** the mesh is displayed in a view fitted to the model.
2. **Given** a mesh is displayed, **When** the user rotates or zooms the view,
   **Then** the displayed viewpoint changes while the mesh remains available.
3. **Given** an unsupported, unreadable, or invalid file, **When** the user tries
   to open it, **Then** the viewer reports that it cannot load the file and keeps
   the application usable.

---

### User Story 2 - Refine a Mesh (Priority: P2)

The user chooses Loop or Butterfly from a menu and presses the iteration key to
refine the displayed mesh one iteration at a time.

**Why this priority**: Subdivision is the primary purpose of the viewer.

**Independent Test**: Load a valid triangular mesh, select each scheme in turn,
and verify that each key press visibly refines the mesh by one iteration.

**Acceptance Scenarios**:

1. **Given** a mesh is displayed, **When** the user opens the subdivision menu,
   **Then** Loop and Butterfly are available and the selected scheme is apparent.
2. **Given** Loop is selected and a mesh is displayed, **When** the user presses
   the iteration key once, **Then** one Loop subdivision iteration is applied to
   the current mesh.
3. **Given** Butterfly is selected and a mesh is displayed, **When** the user
   presses the iteration key once, **Then** one Butterfly subdivision iteration
   is applied to the current mesh.
4. **Given** the mesh has already been refined, **When** the user presses the
   iteration key again, **Then** one further iteration of the currently selected
   scheme is applied to the refined mesh.
5. **Given** no mesh is loaded, **When** the user requests an iteration,
   **Then** no mesh is changed and the viewer explains that a mesh must be loaded
   first.

---

### User Story 3 - Switch Mesh Display (Priority: P3)

The user switches between wireframe and flat-shaded display with a keyboard key
to inspect the mesh structure and its surface.

**Why this priority**: Both display styles are required to inspect the loaded and
refined shape, but do not replace the core load and subdivision workflows.

**Independent Test**: Load a mesh, press the display-mode key repeatedly, and
verify that the view alternates between wireframe and flat shading.

**Acceptance Scenarios**:

1. **Given** a mesh is displayed, **When** the user presses the display-mode
   key, **Then** the view switches between wireframe and flat-shaded display.
2. **Given** either display mode is active, **When** the user refines the mesh,
   **Then** the selected display mode remains active.

### Edge Cases

- Opening an empty, malformed, unreadable, or unsupported file produces a clear
  error and does not terminate the viewer.
- A mesh with invalid or unsupported topology is rejected with an explanation
  rather than partially displayed or refined.
- Subdivision and view controls are unavailable until a valid mesh is loaded;
  attempting to use them gives clear feedback without changing state.
- Repeated iteration requests apply one iteration per key press to the current
  mesh.
- Changing the subdivision scheme affects subsequent iterations; it does not
  silently reprocess earlier iterations.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The viewer MUST allow the user to open a triangular mesh from an
  STL or OBJ file.
- **FR-002**: The viewer MUST display a successfully opened mesh fitted within
  the view.
- **FR-003**: The user MUST be able to rotate and zoom the displayed mesh.
- **FR-004**: A menu MUST allow the user to select Loop or Butterfly subdivision,
  and the current selection MUST be apparent.
- **FR-005**: The user MUST be able to start a single subdivision iteration
  through a keyboard key press.
- **FR-006**: Each iteration MUST refine the currently displayed mesh using the
  currently selected subdivision scheme.
- **FR-007**: The viewer MUST support wireframe and flat-shaded mesh display.
- **FR-008**: The user MUST be able to switch between those display modes using
  a keyboard key press.
- **FR-009**: The viewer MUST report file loading and unsupported-topology errors
  clearly, without terminating the application.
- **FR-010**: The viewer MUST prevent subdivision requests when no valid mesh is
  loaded and explain what action is required.
- **FR-011**: The viewer MUST represent mesh connectivity with a half-edge
  data structure, selected as the simpler of the requested edge-based options.

### Key Entities *(include if feature involves data)*

- **Mesh**: A triangular shape loaded from a supported file, including its
  vertices, faces, edge-based connectivity, and current refined result.
- **Half-edge**: A directed edge record linking mesh connectivity and adjacent
  faces; paired half-edges describe a shared edge.
- **Subdivision scheme**: The selected refinement method, either Loop or
  Butterfly.
- **Iteration**: One application of the selected scheme to the current mesh.
- **Display mode**: The selected way to view the mesh, either wireframe or
  flat-shaded.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All four valid sample files in the acceptance set (two STL and two
  OBJ triangular meshes) open and display successfully.
- **SC-002**: Both Loop and Butterfly each complete one visible refinement after
  a single iteration-key press on a valid sample mesh.
- **SC-003**: Users can switch between the two supported display modes with the
  assigned key, and each mode remains active after a refinement.
- **SC-004**: At least 4 out of 5 first-time test users can load a sample,
  rotate or zoom it, select a subdivision method, refine once, and switch
  display modes without assistance.
- **SC-005**: Every supported loaded or subdivided mesh passes checks that its
  edge-based connectivity references valid vertices, faces, and neighboring
  half-edges.

## Assumptions

- The supported input files contain valid triangular meshes; files with
  unsupported or invalid topology are reported and rejected.
- A newly opened mesh is shown in flat-shaded mode, with the view fitted to it.
- Each iteration-key press refines the current result exactly once. Changing the
  selected scheme does not undo or recalculate completed iterations.
- Keyboard shortcuts are indicated in the viewer so users can discover the
  iteration and display-mode controls.
- The acceptance set contains four representative valid sample meshes: two in
  STL format and two in OBJ format.
- This feature is limited to opening, viewing, and subdividing a single mesh at
  a time; editing, saving, and other subdivision schemes are out of scope.
- Use a half-edge representation as the simplest edge-based choice; reject
  unsupported topology rather than adding specialized representations.
