# Data Model: Subdivision Iteration Controls and Reset

## Current mesh

The mesh currently shown by the viewer.

- **value**: Validated half-edge mesh, or absent when no mesh is loaded.
- **initial state**: The mesh produced by loading a supported source file.
- **subdivision transition**: A successful subdivision action replaces the
  current mesh with the result of the requested number of sequential passes.
- **reset transition**: Replaces the current mesh with the loaded mesh state.
- **validation**: Every successful pass uses the existing mesh validation and
  topology guarantees. If a requested action fails, the current displayed mesh
  remains unchanged.

## Loaded mesh state

The successfully loaded mesh to which reset returns.

- **value**: The validated mesh state immediately after a successful load.
- **lifecycle**: Replaced when another mesh is successfully loaded; retained
  when a file load fails.
- **relationship**: Reset restores the current mesh from this state.

## Selected iteration count

The number of complete subdivision passes requested by the next subdivision
action.

- **value**: An integer from 1 through 4, inclusive.
- **default**: 1.
- **transition**: Changing the selection affects the next action only.
- **validation**: Values outside the supported range are not selectable.
- **reset behavior**: Reset does not change this selection.

## Applied iteration count

The total number of successful subdivision passes applied since the currently
loaded mesh was opened.

- **value**: A non-negative integer.
- **initial state**: 0 after a successful load.
- **subdivision transition**: Increases by the selected iteration count only
  after all requested passes complete successfully.
- **reset transition**: Returns to 0.
- **new load transition**: A successful load resets it to 0.

## Subdivision scheme

The selected algorithm for every pass in the next subdivision action.

- **value**: Loop or Butterfly.
- **transition**: The existing scheme selection changes the scheme for future
  operations.
- **reset behavior**: Reset retains the selected scheme.
