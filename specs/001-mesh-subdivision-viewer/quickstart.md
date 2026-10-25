# Quickstart: Mesh Subdivision Viewer

## Prerequisites

- Python 3.11 or newer
- uv
- A desktop environment with a supported Qt display
- One valid triangular STL file and one valid OBJ file for manual checks

## Install and launch

From the repository root:

```powershell
uv sync --extra dev
uv run python -m mesh_subdivision_viewer
```

The viewer opens with no mesh loaded. Use its file menu to open an STL or OBJ
file. The Mesh menu selects the Loop or Butterfly scheme.

- Press `N` to apply exactly one iteration of the selected scheme.
- Press `W` to switch between flat-shaded and wireframe display.
- Drag with the mouse to rotate and use the mouse wheel to zoom.

## Automated checks

```powershell
uv run python -m pytest
```

Expected result: mesh construction and validation, file loading, and both
subdivision schemes pass their focused tests. The viewer tests also send
mouse-drag and wheel events through the VTK camera interactor and verify that
rotation changes the camera position and zoom reduces its distance from the
focal point.

## Manual acceptance checks

1. Open a valid STL file. Confirm that it is fitted in the view and that
   dragging and zooming change the camera view.
2. Open a valid OBJ file containing polygon faces. Confirm it loads as a
   triangle mesh.
3. Select Loop in the Mesh menu and press `N` once.
   Confirm one refinement is displayed. Press it again and confirm a second
   iteration acts on the current result.
4. Select Butterfly and press `N`. Confirm the selected scheme
   is used for the next iteration.
5. Press `W` repeatedly. Confirm the view alternates between
   wireframe and flat shading, including after refinement.
6. Try an unreadable or invalid mesh. Confirm a clear error appears and the
   application remains usable.

See [data-model.md](data-model.md) for topology invariants.
