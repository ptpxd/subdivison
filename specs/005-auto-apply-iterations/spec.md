# Feature Specification: Automatically Apply Iteration Changes

**Feature Branch**: `005-auto-apply-iterations`

**Created**: 2026-11-08

**Status**: Implemented; zero-selection and manual-apply behavior superseded by
`006-zero-iterations-restore-loaded-mesh`

**Input**: User description: "When I change the iteration count, I should not have to press N; the mesh should change automatically."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Apply Iteration Changes Immediately (Priority: P1)

The user adjusts the iteration slider or uses the iteration keyboard controls
and immediately sees the mesh update to reflect the selected iteration count,
without invoking the `N` subdivision command.

**Why this priority**: Requiring a separate apply command makes the iteration
control feel disconnected from the displayed mesh and adds an unnecessary
step to the primary interaction.

**Independent Test**: Load a mesh, change the selected iteration count to a
positive value, and verify that the displayed mesh and applied-iteration
feedback update without pressing `N`.

**Acceptance Scenarios**:

1. **Given** a mesh is loaded, **When** the user changes the iteration count
   to a value from one through four using the slider, **Then** the viewer
   immediately displays the corresponding subdivision result.
2. **Given** a mesh is loaded, **When** the user increases or decreases the
   iteration count with the keyboard, **Then** the viewer immediately updates
   the displayed mesh to reflect the new positive count.
3. **Given** the user changes the iteration count, **When** the update
   succeeds, **Then** the viewer's result feedback identifies the applied
   iteration count and resulting mesh size.

### User Story 2 - Apply Scheme Changes Immediately (Priority: P1)

The user can change between Loop and Butterfly and immediately see the
currently selected positive iteration count recomputed with the newly selected
scheme.

**Why this priority**: A method selection that does not affect the displayed
result makes it difficult to compare the available subdivision schemes.

**Independent Test**: Select a positive iteration count, confirm it is
displayed, then switch schemes and verify that the result is recomputed from
the loaded mesh using the newly selected scheme without pressing `N`.

**Acceptance Scenarios**:

1. **Given** a positive iteration count is selected, **When** the user changes
   the subdivision scheme, **Then** the same iteration count is immediately
   applied using the newly selected scheme from the loaded mesh.
2. **Given** the selected iteration count is zero, **When** the user changes
   the subdivision scheme, **Then** the zero-count no-op behavior is
   preserved.
3. **Given** recomputation fails, **When** the scheme change is handled,
   **Then** the previous displayed mesh and successful-result feedback remain
   intact and the failure is reported.

### Edge Cases

- Selecting zero is a no-op: it does not change the currently displayed mesh
  or the applied iteration count.
- A positive count is the requested total iteration count relative to the
  loaded mesh, not an additional number of iterations to append to the current
  result.
- Decreasing a positive count recomputes from the loaded mesh so the displayed
  result matches the newly selected total.
- If no mesh is loaded, changing the iteration count or scheme does not
  attempt subdivision and the viewer communicates that a mesh must be loaded.
- A failed automatic update leaves the last successfully displayed mesh and
  its result feedback unchanged, while reporting the failure.
- The iteration range remains zero through four, inclusive.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Changing the iteration slider to a positive value MUST
  automatically apply that total iteration count without requiring the user
  to press `N` or invoke a separate action.
- **FR-002**: The `+` and `-` keyboard controls MUST automatically apply a
  changed positive iteration count.
- **FR-003**: Changing the subdivision scheme while a positive iteration
  count is selected MUST automatically apply that count with the newly
  selected scheme, starting from the loaded mesh.
- **FR-004**: A selected iteration count MUST represent the total number of
  iterations in the displayed result relative to the loaded mesh; changes
  MUST NOT accidentally compound the selected total onto an already
  subdivided result.
- **FR-005**: Selecting zero MUST leave the displayed mesh and applied
  iteration count unchanged and MUST NOT be treated as reset.
- **FR-006**: The supported iteration range MUST remain zero through four,
  inclusive.
- **FR-007**: After a successful automatic update, the viewer MUST report the
  applied iteration count and resulting mesh size.
- **FR-008**: A failed automatic update MUST preserve the previously
  displayed mesh and successful-result feedback and MUST report the failure.
- **FR-009**: If no mesh is loaded, automatic application MUST NOT alter mesh
  state and MUST provide clear feedback.
- **FR-010**: The `N` shortcut and explicit subdivision action MAY remain
  available for compatibility, but MUST NOT be required after changing the
  iteration count or subdivision scheme.

### Key Entities

- **Selected iteration count**: Integer from zero through four representing
  the desired total number of iterations relative to the loaded mesh.
- **Displayed subdivision result**: The last successfully computed mesh,
  including its applied iteration count and the scheme that produced it.
- **Loaded mesh**: The baseline mesh used to compute a selected positive
  iteration count and to restore the original geometry through reset.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every successful positive slider change updates the displayed
  mesh without a separate `N` action.
- **SC-002**: Every successful `+` or `-` change to a positive iteration
  count updates the displayed mesh immediately.
- **SC-003**: Switching schemes with a positive count selected updates the
  result to use the newly selected scheme without a separate `N` action.
- **SC-004**: For every successful automatic update, the result feedback
  reports the correct applied count and mesh size.
- **SC-005**: At zero, changing the iteration selection or scheme does not
  alter the displayed mesh or applied count.
- **SC-006**: A failed automatic update never replaces the last successful
  displayed result.

## Assumptions

The zero-selection and optional manual-apply behavior in this historical
feature was superseded by
[006-zero-iterations-restore-loaded-mesh](../006-zero-iterations-restore-loaded-mesh/spec.md).

- This feature supersedes the manual-apply interaction in
  `004-iteration-slider-zero-default` for positive iteration and scheme
  changes; zero remains a no-op, and reset remains separate.
- The selected count is the total result count relative to the loaded mesh.
- Scheme changes at a positive selected count recompute from the loaded mesh
  to avoid mixing subdivision algorithms in one result.
- The `N` shortcut may remain as a way to reapply the current positive
  selection, but ordinary slider and keyboard count changes apply
  automatically.
- Subdivision algorithms, mesh formats, the four-iteration maximum, and
  reset behavior are otherwise unchanged.
