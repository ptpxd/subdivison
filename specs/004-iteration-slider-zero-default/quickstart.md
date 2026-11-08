# Quickstart: Zero-Default Iteration Control

## Prerequisites

- Python 3.11 or newer
- `uv`
- A desktop environment that can display the Qt viewer
- A valid triangular STL or OBJ mesh; repository fixtures can be used

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

- A new viewer starts with the slider at its minimum, displaying zero selected iterations.
- Moving the slider to a positive value or using `+`/`-` immediately applies the selected total iteration count.
- Selecting zero leaves the displayed mesh, applied iteration count, and last successful result unchanged; it does not reset the mesh.
- Changing the subdivision scheme at a positive selected count immediately recomputes from the loaded mesh using the new scheme.
- Decreasing the selected count recomputes from the loaded mesh so the result represents the selected total, not additional iterations.
- Pressing `N` or invoking **Subdivide mesh** re-applies the current positive selection but is not required after changing the slider or scheme.
- Reset restores the loaded mesh and zero applied iterations while preserving the slider selection.

## Manual acceptance checks

1. Launch the viewer. Confirm the iteration slider thumb is at the far-left position and the adjacent iteration count displays zero.
2. Load a valid triangular STL or OBJ mesh and note its face count.
3. Move the slider to four. Confirm the displayed mesh updates immediately to four iterations and the feedback reports the applied count and face totals.
4. Use `-` and `+` to change the selected iteration count. Confirm each positive change applies immediately and stays within zero to four.
5. Change the selected count to zero. Confirm the displayed mesh, applied count, and successful-result feedback remain unchanged.
6. Select two iterations, then switch from Loop to Butterfly. Confirm Butterfly is immediately applied to two iterations of the loaded mesh.
7. Select a positive count lower than the current applied count. Confirm the mesh is recomputed from the loaded baseline to that count.
8. Use `N` or the explicit subdivision action to reapply the current positive selection if desired.
9. Reset the mesh. Confirm the loaded geometry and zero applied iteration count are restored while the selected slider value remains unchanged.
