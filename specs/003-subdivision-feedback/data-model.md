# Data Model: Subdivision Controls and Result Feedback

## Subdivision settings

Settings used by the next explicit subdivision action.

- **scheme**: Loop or Butterfly.
- **iteration count**: Integer from 1 through 4, default 1.
- **selection transition**: Updates the selected value only; does not modify
  the displayed mesh or successful-operation result.
- **application transition**: The explicit subdivision action applies the
  selected scheme for the selected number of complete passes.

## Displayed mesh

The currently loaded or refined mesh.

- **face count**: Number of triangular faces in the current mesh.
- **subdivision transition**: Replaced only after every requested pass
  succeeds.
- **reset transition**: Restored to the most recently successfully loaded
  mesh.
- **failure behavior**: A failed pass sequence leaves the displayed mesh
  unchanged.

## Successful subdivision result

The most recent successful operation summary shown to the user.

- **scheme**: Method used for the completed operation.
- **passes applied**: The iteration count chosen for that action.
- **face count before**: Current mesh face count immediately before the action.
- **face count after**: Result mesh face count after every requested pass
  completes.
- **update rule**: Replace the summary only after successful completion.
- **failure behavior**: Retain the previous successful summary; show the
  failure separately.
- **reset/load behavior**: A reset or new load changes the mesh baseline; any
  displayed operation summary must not be presented as a result for the new
  baseline.
