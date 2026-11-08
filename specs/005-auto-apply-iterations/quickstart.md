# Quickstart: Automatically Applied Iteration Changes

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
- Moving the slider to a positive count immediately updates the mesh and
  reports the resulting applied count and face totals.
- The `+` and `-` keyboard controls immediately apply each changed positive
  count; they do not require a separate `N` action.
- Changing Loop/Butterfly with a positive count selected immediately
  recomputes that total from the loaded mesh using the newly selected scheme.
- Selecting zero restores the loaded mesh, sets applied iterations to zero,
  and clears the subdivision-result summary.
- Failed automatic computation preserves the last successful displayed mesh
  and result summary while reporting the failure.
- There is no separate `N` or **Subdivide mesh** action; positive iteration
  and scheme changes apply automatically.
- Reset restores the loaded mesh and sets selected and applied iterations to
  zero while preserving the selected scheme.

## Manual acceptance checks

1. Launch the viewer and confirm the slider starts at zero.
2. Load `tests/fixtures/tetrahedron_ascii.stl` and note its face count.
3. Move the slider to one. Confirm the mesh updates immediately, the applied
   count becomes one, and result feedback reports the face-count change.
4. Move the slider to three. Confirm the result represents three total
   iterations from the loaded mesh rather than three additional iterations
   applied to the one-iteration result.
5. Use `-` and `+` to change the selected count. Confirm each positive
   selection updates immediately and the range remains zero through four.
6. With a positive count selected, switch from Loop to Butterfly. Confirm the
   displayed result immediately changes to the selected count computed from
   the loaded mesh with Butterfly.
7. While displaying a subdivided mesh, set the slider to zero. Confirm the
   loaded geometry and zero applied count are restored and subdivision-result
   feedback is cleared.
8. Use **Mesh → Reset to loaded mesh** or press `R`. Confirm the loaded
   geometry and both selected and applied counts are zero, with the selected
   scheme preserved.
9. Confirm there is no `N` or **Subdivide mesh** action and that subdivision
   failures leave the last successful displayed result intact.
