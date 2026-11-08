# Data Model: Automatically Applied Iteration Changes

## Selected iteration count

The desired total number of subdivision iterations relative to the loaded
mesh.

- **value**: Integer from 0 through 4, inclusive.
- **initial state**: 0 when a viewer starts.
- **positive selection transition**: Update the selected value and
  immediately request an automatic update using the current scheme.
- **zero transition**: Update the selected value and selection feedback only;
  leave the displayed mesh, applied count, applied scheme, and successful
  result summary unchanged.
- **reset behavior**: Reset preserves this value.

## Applied iteration count

The number of complete iterations represented by the currently displayed
subdivision result relative to the loaded mesh.

- **value**: Non-negative integer.
- **initial state**: 0 before subdivision and after a successful mesh load.
- **automatic update transition**: Changes only after all requested
  subdivision operations complete successfully.
- **failure behavior**: A failed update leaves this value unchanged.
- **zero selection**: Does not change this value.
- **reset transition**: Returns to 0.

## Selected subdivision scheme

The scheme chosen for the next update.

- **value**: Loop or Butterfly.
- **scheme-change transition**: At a positive selected count, immediately
  request an update with the new scheme. At zero, preserve the displayed
  mesh.
- **failure behavior**: The newly selected scheme remains the user's
  selection, but applied scheme and displayed result remain those of the last
  successful operation.

## Applied subdivision scheme

The scheme that produced the displayed subdivision result.

- **value**: Loop, Butterfly, or none when the display is the loaded
  baseline.
- **update transition**: Changes only after all iterations succeed.
- **baseline recomputation**: If the selected scheme differs from the applied
  scheme, compute the requested total from the loaded mesh.
- **reset/load transition**: Cleared when the loaded baseline is restored or
  replaced.

## Loaded mesh state

The most recently loaded valid mesh and baseline for result calculation and
reset.

- **value**: Validated mesh immediately after a successful load.
- **lifecycle**: Replaced only on a successful load; a failed load retains
  the current baseline.
- **reset transition**: The displayed mesh returns to this state.

## Subdivision feedback

User-visible information describing the selected count or displayed result.

- **selection feedback**: Identifies the selected iteration count and does
  not imply success.
- **success feedback**: Reports the scheme, resulting applied count, and
  before-and-after face counts.
- **zero feedback**: Explains that the mesh was not changed and subdivision
  was not applied; it must not imply a reset.
- **failure feedback**: Reports the error while preserving the previous
  successful-result label and summary.
