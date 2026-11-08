# Feature Specification: Zero-Default Iteration Control

**Feature Branch**: `004-iteration-slider-zero-default`

**Created**: 2026-11-08

**Status**: Draft

**Input**: User description: "A slider a legszélén kezdődjön; iterációként legyen megfogalmazva, billentyűzettel is lehessen növelni, és sémaváltáskor maradjon meg a kiválasztott iterációszám."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start with No Subdivision Selected (Priority: P1)

When the viewer starts, the user sees the iteration slider at its minimum, zero position. Zero means that no iterations are selected; values one through four remain available for the next subdivision operation. The control and its feedback consistently use iteration terminology.

**Why this priority**: The current initial value places the slider one step away from its left edge and suggests an iteration is selected even though no subdivision has been applied.

**Independent Test**: Start the viewer and verify that the slider thumb is at the far-left position, its displayed iteration count is zero, and no subdivision is reported as applied.

**Acceptance Scenarios**:

1. **Given** the viewer has just started, **When** the user views the iteration control, **Then** the slider is at its minimum position and the displayed selected iteration count is zero.
2. **Given** the selected iteration count is below four, **When** the user invokes the keyboard increase command, **Then** the selected count increases by one and never exceeds four.
3. **Given** a mesh is loaded, **When** the user changes the selected iteration count with the slider or keyboard, **Then** the mesh geometry and applied iteration count remain unchanged until subdivision is explicitly started.

### User Story 2 - Understand Zero and Applied-Iteration Feedback (Priority: P2)

The user can distinguish the iteration count selected for a future operation from the number already applied to the displayed mesh.

**Why this priority**: Clear state feedback prevents a selected value from being mistaken for completed subdivision.

**Independent Test**: Select four iterations without applying them, inspect the status, then invoke subdivision and verify that selection and applied-result feedback describe their respective states clearly.

**Acceptance Scenarios**:

1. **Given** zero iterations are selected, **When** the user attempts subdivision, **Then** the mesh remains unchanged and the viewer explains that at least one iteration must be selected.
2. **Given** a positive iteration count is selected but not applied, **When** the user views the iteration control or status, **Then** the viewer identifies the count as selected, not applied.
3. **Given** subdivision succeeds, **When** the user views the result feedback, **Then** it reports the applied iteration count without wording that could be read as zero iterations applied out of a different selected total.
4. **Given** the user resets the mesh, **When** the reset completes, **Then** the mesh has zero applied iterations and the selected slider value is preserved.

### User Story 3 - Preserve Iterations When Changing Subdivision Scheme (Priority: P1)

The user can switch between Loop and Butterfly without losing the selected iteration count. Pressing `N` applies the selected count using the newly selected scheme, starting from the loaded mesh when a different scheme must replace the current result.

**Why this priority**: Losing or silently ignoring the count makes scheme comparison confusing and forces users to repeat slider input.

**Independent Test**: Select and apply two Loop iterations, switch to Butterfly, verify that two remains selected, then press `N` and verify the displayed mesh is recomputed from the loaded mesh using two Butterfly iterations.

**Acceptance Scenarios**:

1. **Given** a positive iteration count is selected, **When** the user changes the subdivision scheme, **Then** the selected count remains unchanged and the displayed mesh is not immediately modified.
2. **Given** a mesh has been subdivided with one scheme, **When** the user selects the other scheme and presses `N`, **Then** the same selected iteration count is applied using the new scheme from the loaded mesh baseline.
3. **Given** the user changes the scheme more than once before applying subdivision, **When** the user presses `N`, **Then** the most recently selected scheme is used and the iteration count is preserved.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The iteration control MUST provide integer values from zero through four, inclusive. Zero is the no-selection state; one through four are valid iteration counts.
- **FR-002**: On a fresh viewer start, the slider MUST be at its minimum position and its selected iteration count MUST be zero. This requirement supersedes the default-one requirements in features 002 and 003.
- **FR-003**: User-facing control labels and status messages MUST use "iteration" or "iterations" and MUST distinguish the selected iteration count from the number of iterations applied to the displayed mesh.
- **FR-004**: Changing the slider value MUST NOT modify mesh geometry or the applied iteration count.
- **FR-005**: The `+` and `-` keyboard commands MUST increase or decrease the selected iteration count by one within the zero-to-four range. Changing the count by keyboard MUST NOT apply subdivision.
- **FR-006**: An attempt to subdivide with zero selected iterations MUST leave the mesh unchanged and MUST provide clear feedback that no subdivision was performed.
- **FR-007**: Pressing `N` or invoking the explicit subdivision action with a selected value from one through four MUST apply that many complete iterations.
- **FR-008**: Subdivision feedback MUST describe the number of iterations actually applied in clear terms and MUST NOT ambiguously combine zero newly applied iterations with a positive selected or total count.
- **FR-009**: Reset MUST restore the loaded mesh, indicate zero applied iterations, and preserve the selected slider value, consistent with feature 002.
- **FR-010**: Changing the subdivision scheme MUST preserve the selected iteration count and MUST NOT immediately modify the displayed mesh.
- **FR-011**: When the selected scheme differs from the scheme used to create the displayed subdivision result, pressing `N` MUST recompute the selected iteration count from the loaded mesh using the newly selected scheme.

### Key Entities *(include if feature involves data)*

- **Selected iteration count**: Integer from zero through four that configures the next subdivision operation; zero means no operation is selected.
- **Applied iteration count**: Number of complete subdivision iterations reflected in the currently displayed mesh; it is zero for the loaded mesh before subdivision and after reset.
- **Applied subdivision scheme**: The scheme used to create the currently displayed subdivision result, used to determine whether a new selection must be recomputed from the loaded mesh.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On every fresh application start, the slider thumb is at the far-left position and displays zero iterations selected.
- **SC-002**: Selecting any value from zero through four with the slider or keyboard changes only the selected-iteration display and does not change the mesh until subdivision is explicitly invoked.
- **SC-003**: At zero, a subdivision attempt leaves the mesh unchanged and clearly reports that no iteration was applied.
- **SC-004**: Users can tell from the control and result feedback which iteration count is selected and which count has actually been applied.
- **SC-005**: Changing subdivision schemes preserves the selected iteration count; invoking `N` applies that count using the new scheme from the loaded mesh baseline.

## Assumptions

- The slider configures the next subdivision operation; changing its value is non-destructive.
- A value of zero is a valid idle state, not a subdivision iteration.
- The selected iteration count remains unchanged when the user changes the subdivision scheme.
- If a different scheme is selected after subdivision has already been applied, applying again replaces the displayed result with the selected number of iterations from the loaded mesh under the new scheme.
- Existing subdivision schemes, mesh formats, and maximum of four iterations remain unchanged.
- Reset preserves the selected iteration count as specified by feature 002, even though the restored mesh has zero applied iterations.

## Out of Scope

- Changing the subdivision algorithms themselves or increasing the maximum iteration count.
- Changing the reset behavior or clearing the selected iteration count during reset.
