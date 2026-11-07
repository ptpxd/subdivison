# Quickstart: Subdivision Controls and Result Feedback

## Prerequisites

- Python 3.11 or newer
- `uv`
- A desktop environment that can display the Qt viewer
- A valid triangular STL or OBJ mesh; the repository fixtures can be used

## Install and launch

From the repository root:

```powershell
uv sync --extra dev
uv run python -m mesh_subdivision_viewer
```

## Automated validation

Run the focused viewer tests:

```powershell
uv run python -m pytest tests/test_viewer.py
```

Expected results:

- Changing iteration count or subdivision scheme does not change the mesh or
  erase the last successful-operation summary.
- Starting subdivision explicitly applies the selected scheme and number of
  complete passes.
- A persistent result summary reports the scheme, number of passes, and actual
  before/after triangular face counts for each successful operation.
- Loading a new mesh or resetting to the loaded mesh clears the previous
  operation summary but preserves scheme and iteration selections.
- Failure retains the displayed mesh and persistent successful-result summary
  while the status message reports the failure.

## Manual acceptance checks

1. Launch the viewer and open a valid triangular STL or OBJ file.
2. Select a subdivision scheme and an iteration count. Confirm the UI explains
   that these settings configure the next operation, the last result summary
   remains visible, and the mesh does not change yet.
3. Use **Mesh → Subdivide mesh** or press `N`. Confirm the mesh changes and
   the persistent result summary identifies the scheme, selected pass count,
   and actual face counts before and after.
4. Select the other scheme. Confirm the current mesh and successful-result
   summary do not change merely from selecting it.
5. Press `R` to restore the loaded mesh. Confirm the previous summary clears
   while the selected settings remain unchanged. Apply subdivision again and
   confirm the result summary identifies the newly selected scheme and the
   counts for this operation.
6. Attempt subdivision without a loaded mesh. Confirm the viewer explains
   that a mesh must be loaded and remains usable.
7. Run the focused tests to verify that a failed multi-pass operation retains
   the displayed mesh and previous successful-result summary while reporting
   the failure.
