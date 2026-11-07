# Quickstart: Subdivision Iteration Controls and Reset

## Prerequisites

- Python 3.11 or newer
- `uv`
- A desktop environment that can display the Qt viewer
- A valid triangular STL or OBJ mesh; the repository's tetrahedron fixture can
  be used for manual checks

## Install and launch

From the repository root:

```powershell
uv sync --extra dev
uv run python -m mesh_subdivision_viewer
```

## Automated validation

Run the focused tests:

```powershell
uv run python -m pytest tests/test_subdivision.py tests/test_viewer.py
```

Expected results:

- The one-pass subdivision behavior remains unchanged.
- Applying multiple selected passes produces the same result as applying the
  single-pass operation repeatedly to its preceding result.
- Reset returns the current mesh and applied-iteration count to the loaded
  state.
- The UI defaults to one iteration, permits only values 1–4, and preserves the
  selected scheme and iteration count when reset is used.

## Manual acceptance checks

1. Launch the viewer and open a valid triangular STL or OBJ file.
2. In **Mesh → Subdivision iterations**, choose each count from 1 through 4.
   Confirm that the default is 1 and the selected value is apparent.
3. Use **Mesh → Subdivide mesh** or press `N`. Confirm the UI explains that an
   iteration is one complete pass over the current mesh.
4. Apply two passes at once. Confirm the result is equivalent to two
   successive single passes using the same scheme.
5. Apply another subdivision action, then choose **Mesh → Reset to loaded
   mesh** or press `R`. Confirm the mesh returns to its just-loaded shape and
   the applied iteration count is zero.
6. Confirm reset retains the selected subdivision scheme and iteration count.
7. Reset before any subdivision and confirm the mesh remains unchanged and
   the viewer remains usable.
8. With no mesh loaded, attempt subdivision and reset; confirm the viewer
   reports that a mesh must be loaded and no mesh state changes.
