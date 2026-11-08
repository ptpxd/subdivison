# Feature Specification: Restore Loaded Mesh at Zero Iterations

**Feature Branch**: `006-zero-iterations-restore-loaded-mesh`

**Created**: 2026-11-08

**Status**: Implemented

**Input**: User description: "When reducing the iteration count from two to one and then zero, the viewer stops at one iteration even though it says zero, and does not restore the original shape. If the Subdivide mesh (N) feature is no longer needed, it can be removed."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Restore the Loaded Mesh at Zero (Priority: P1)

The user decreases the selected total iteration count to zero and immediately
sees the exact mesh that was originally loaded.

**Why this priority**: The selected iteration count must match the geometry
shown. Leaving a subdivided mesh on screen after selecting zero is misleading
and prevents users from returning to the original shape through the primary
iteration control.

**Independent Test**: Load a mesh, select two iterations, decrease to one, then
zero. Verify that the displayed geometry at zero matches the loaded mesh, the
applied iteration count is zero, and the result feedback indicates that no
subdivision is applied.

**Acceptance Scenarios**:

1. **Given** a loaded mesh with two iterations displayed, **When** the user
   selects one iteration, **Then** the viewer displays one iteration computed
   relative to the loaded mesh.
2. **Given** one iteration is displayed, **When** the user selects zero,
   **Then** the viewer restores the loaded mesh and reports zero applied
   iterations.
3. **Given** a positive iteration count is displayed, **When** the user uses
   the keyboard to decrease the count to zero, **Then** the same restoration
   occurs immediately.

### User Story 2 - Keep Iteration and Display State Consistent (Priority: P1)

The user can reset the mesh without leaving a positive iteration count selected
for an unsubdivided mesh.

**Why this priority**: Iteration selection, applied state, and displayed
geometry must not contradict each other.

**Independent Test**: Load a mesh, select a positive count, invoke reset, and
verify that the loaded geometry is displayed and both the selected and applied
iteration counts are zero.

**Acceptance Scenarios**:

1. **Given** a subdivided mesh, **When** the user invokes reset, **Then** the
   loaded mesh is restored and the selected and applied counts become zero.
2. **Given** a subdivision scheme is selected, **When** the user invokes reset
   or selects zero, **Then** the selected scheme remains unchanged.

### User Story 3 - Use Automatic Iteration Application (Priority: P2)

The user adjusts the iteration count or subdivision scheme and the viewer
updates immediately, without a separate manual subdivision command.

**Why this priority**: A separate apply command is redundant when controls
already apply changes automatically and can leave users unsure whether the
display reflects their current selection.

**Independent Test**: Change the count and scheme and verify that each valid
positive selection updates immediately. Verify that the `N` shortcut and
**Subdivide mesh** action are no longer presented.

**Acceptance Scenarios**:

1. **Given** a mesh is loaded, **When** the user selects a positive iteration
   count, **Then** the viewer immediately applies that total count relative to
   the loaded mesh.
2. **Given** a positive count is selected, **When** the user changes scheme,
   **Then** the viewer immediately recomputes that count from the loaded mesh
   using the selected scheme.
3. **Given** the user changes count or scheme, **When** the operation succeeds,
   **Then** the result feedback reports the applied count and resulting face
   count.
4. **Given** an automatic subdivision fails, **When** the failure is reported,
   **Then** the last successfully displayed mesh and its successful result
   feedback remain intact.

## Edge Cases

- Selecting zero when a mesh is loaded restores the loaded mesh even if a
  positive iteration result is currently displayed.
- Selecting zero with no mesh loaded changes no mesh state and does not raise
  an error.
- Reset with no mesh loaded continues to provide clear feedback.
- The iteration range remains zero through four, inclusive.
- Selecting a lower positive count recomputes from the loaded mesh; it does not
  try to reverse subdivision or compound additional iterations.
- Removing the manual subdivision action must not remove iteration selection,
  scheme selection, or the reset command.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A selected iteration count MUST represent the desired total
  number of subdivision iterations relative to the loaded mesh.
- **FR-002**: Selecting a lower positive count MUST display the result
  recomputed from the loaded mesh at that total count.
- **FR-003**: Selecting zero MUST restore the loaded mesh, set the applied
  iteration count to zero, and clear subdivision-result feedback.
- **FR-004**: The zero-selection transition MUST apply immediately through both
  the slider and keyboard iteration controls.
- **FR-005**: Reset MUST restore the loaded mesh and set the selected and
  applied iteration counts to zero while preserving the selected subdivision
  scheme.
- **FR-006**: Positive iteration-count and scheme changes MUST continue to
  apply automatically, without requiring a separate command.
- **FR-007**: The `N` shortcut and **Subdivide mesh** menu action MUST be
  removed because they do not provide a necessary operation beyond automatic
  application.
- **FR-008**: A failed automatic subdivision MUST preserve the last
  successfully displayed mesh and successful-result feedback, and MUST report
  the failure.
- **FR-009**: If no mesh is loaded, iteration and scheme selection MUST NOT
  alter mesh state and MUST provide clear feedback.
- **FR-010**: The supported iteration range MUST remain zero through four,
  inclusive.

### Key Entities

- **Loaded mesh**: The original mesh loaded from an STL or OBJ file and the
  baseline for all iteration counts.
- **Selected iteration count**: Integer from zero through four representing
  the desired total iteration count relative to the loaded mesh.
- **Applied iteration count**: The count represented by the currently
  displayed mesh; zero means the loaded mesh is displayed.
- **Selected scheme**: The subdivision algorithm used for positive iteration
  counts; reset and zero selection do not change it.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After a positive count is reduced to zero, the displayed mesh
  matches the loaded mesh and the applied count is zero.
- **SC-002**: For any positive decrease, the displayed result matches the
  selected total count computed from the loaded mesh.
- **SC-003**: After reset, selected count, applied count, and displayed mesh
  consistently represent the loaded zero-iteration state.
- **SC-004**: Positive count and scheme changes continue to update the mesh
  without a separate apply action.
- **SC-005**: The `N` shortcut and **Subdivide mesh** action are absent from
  the viewer's available controls and user documentation.
- **SC-006**: Failed automatic updates preserve the last successful result.
