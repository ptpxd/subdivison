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
- Moving the slider or using `+`/`-` updates selection feedback only; mesh geometry and applied iteration count remain unchanged.
- Applying with zero selected iterations leaves the mesh unchanged and reports that no subdivision was performed.
- Applying with one through four selected iterations results in the corresponding applied state.
- Applying the already-applied count does not report zero newly applied iterations against a positive total.
- Changing the subdivision scheme preserves the selected iteration count and does not immediately modify the mesh.
- Pressing `N` after changing schemes recomputes the selected count from the loaded mesh with the newly selected scheme.
- Reset restores the loaded mesh and zero applied iterations while preserving the slider selection.

## Manual acceptance checks

1. Launch the viewer. Confirm the iteration slider thumb is at the far-left position and the adjacent iteration count displays zero.
2. Load a valid triangular STL or OBJ mesh and note its face count.
3. Move the slider to four. Confirm the displayed mesh and face count do not change and the UI identifies four as selected, not applied.
4. Use `-` and `+` to change the selected iteration count. Confirm it changes by one, stays in the zero-to-four range, and does not modify the mesh.
5. Invoke the explicit subdivision action or press `N`. Confirm four iterations are applied and the resulting feedback describes the applied count clearly.
6. Invoke subdivision again without changing the selection. Confirm the mesh is not misreported as having zero iterations applied out of four.
7. Change the selected count to zero and invoke subdivision. Confirm the displayed mesh remains unchanged and feedback says no subdivision was performed.
8. Select two iterations, apply Loop subdivision, then select Butterfly. Confirm the selected count remains two and the displayed mesh does not immediately change. Press `N` and confirm Butterfly is applied to two iterations of the loaded mesh.
9. Select a positive count lower than the current applied count and invoke subdivision. Confirm the mesh is recomputed from the loaded baseline to that count.
10. Reset the mesh. Confirm the loaded geometry and zero applied iteration count are restored while the selected slider value remains unchanged.
