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
- Selecting zero restores the loaded mesh, sets the applied iteration count to zero, and clears subdivision-result feedback.
- Changing the subdivision scheme at a positive selected count immediately recomputes from the loaded mesh using the new scheme.
- Decreasing the selected count recomputes from the loaded mesh so the result represents the selected total, not additional iterations.
- No separate `N` shortcut or **Subdivide mesh** action is available; positive iteration and scheme changes apply automatically.
- Reset restores the loaded mesh and sets both selected and applied iterations to zero while preserving the selected scheme.

## Manual acceptance checks

1. Launch the viewer. Confirm the iteration slider thumb is at the far-left position and the adjacent iteration count displays zero.
2. Load a valid triangular STL or OBJ mesh and note its face count.
3. Move the slider to four. Confirm the displayed mesh updates immediately to four iterations and the feedback reports the applied count and face totals.
4. Use `-` and `+` to change the selected iteration count. Confirm each positive change applies immediately and stays within zero to four.
5. Change the selected count to zero. Confirm the loaded geometry and zero applied count are restored and successful subdivision feedback is cleared.
6. Select two iterations, then switch from Loop to Butterfly. Confirm Butterfly is immediately applied to two iterations of the loaded mesh.
7. Select a positive count lower than the current applied count. Confirm the mesh is recomputed from the loaded baseline to that count.
8. Reset the mesh. Confirm the loaded geometry and zero selected and applied iteration counts are restored.
