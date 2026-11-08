# Quickstart: Restore Loaded Mesh at Zero Iterations

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

- The viewer starts with zero selected iterations and a slider range of 0–4.
- Positive slider and keyboard count changes apply immediately.
- Decreasing a positive total recomputes from the loaded mesh.
- Selecting zero restores the loaded mesh, sets the applied count to zero, and
  clears subdivision-result feedback.
- Changing Loop/Butterfly at a positive selected count immediately recomputes
  that total from the loaded mesh.
- Reset restores the loaded mesh and sets selected and applied iteration
  counts to zero while preserving the selected scheme.
- A failed automatic update preserves the last successful displayed mesh and
  result summary.
- The `N` shortcut and **Subdivide mesh** menu action are absent.

## Manual acceptance checks

1. Launch the viewer and confirm the slider starts at zero.
2. Load `tests/fixtures/tetrahedron_ascii.stl` and note its face count.
3. Select two iterations, then one. Confirm the displayed result has four
   times the loaded face count and the applied count is one.
4. Select zero. Confirm the original loaded geometry and face count return,
   the applied count reads zero, and subdivision-result feedback is cleared.
5. Use `+` and `-` to change the count and confirm each positive total is
   applied immediately.
6. With a positive count selected, switch from Loop to Butterfly. Confirm the
   same total is recomputed from the loaded mesh.
7. Press `R`. Confirm the loaded geometry is restored and both selected and
   applied iteration counts are zero; the selected scheme remains unchanged.
8. Confirm no **Subdivide mesh** action or `N` shortcut is available.
