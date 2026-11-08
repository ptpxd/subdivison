# Data Model: Zero-Default Iteration Control

## Selected iteration count

The number of complete subdivision iterations requested for the next explicit subdivision operation.

- **value**: Integer from 0 through 4, inclusive.
- **initial state**: 0 when the viewer starts.
- **selection transition**: Slider or `+`/`-` keyboard input updates this value and its label only; it does not change the displayed mesh or applied iteration count.
- **application transition**: A positive value requests that many total iterations relative to the loaded mesh.
- **zero behavior**: An explicit subdivision attempt at zero leaves the current mesh and applied count unchanged and reports that no subdivision was performed.
- **reset behavior**: Reset preserves this value.

## Applied iteration count

The number of successful complete subdivision iterations represented by the displayed mesh relative to the loaded mesh.

- **value**: Non-negative integer.
- **initial state**: 0 before subdivision and after a successful mesh load.
- **subdivision transition**: Changes only after all requested passes succeed.
- **decrease transition**: For a positive selected count below the applied count, recompute from the loaded mesh to the selected count only after explicit subdivision.
- **reset transition**: Returns to 0.
- **failure behavior**: A failed operation does not replace the displayed mesh or update the applied count.

## Applied subdivision scheme

The scheme that produced the displayed subdivision result.

- **value**: Loop, Butterfly, or none when the displayed mesh is the loaded baseline.
- **update transition**: Set only after all requested iterations complete successfully.
- **scheme-change transition**: Selecting a different scheme does not change the displayed value or selected iteration count. On the next explicit apply, recompute from the loaded mesh under the newly selected scheme.
- **reset/load transition**: Clear the applied scheme when restoring or loading the base mesh.

## Loaded mesh state

The most recently loaded valid mesh, used as the baseline for reset and for recomputing a lower positive pass count.

- **value**: Validated mesh immediately after a successful load.
- **lifecycle**: Replaced only by a successful load; a failed load retains the existing baseline.
- **reset transition**: The displayed mesh returns to this state.

## Subdivision feedback

User-visible status describing selection or the result of an explicit operation.

- **selection feedback**: Identifies the selected iteration count, including zero, and does not imply that iterations were applied.
- **success feedback**: Identifies the resulting applied count clearly.
- **zero-attempt feedback**: States that no subdivision was performed.
- **already-applied feedback**: Does not describe the operation as zero new iterations out of a positive selected total.
- **failure feedback**: Reports the failure without presenting a failed operation as a successful result.
