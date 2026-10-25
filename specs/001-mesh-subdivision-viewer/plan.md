# Implementation Plan: Mesh Subdivision Viewer

**Branch**: `001-mesh-subdivision-viewer` | **Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-mesh-subdivision-viewer/spec.md`

## Summary

Build a small Python desktop viewer that loads STL and OBJ triangle meshes,
represents mesh connectivity as a half-edge structure, and renders the model
with interactive rotation and zoom. Use PyVista/VTK for mesh import, rendering,
and its Loop and Butterfly subdivision filters; use PyVistaQt and PySide6 for
the desktop window and menu. This avoids implementing complex subdivision
algorithms while satisfying the required edge-based representation.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: PyVista (VTK-backed mesh I/O and subdivision),
PyVistaQt, PySide6

**Storage**: Local STL and OBJ files; no application data persistence

**Testing**: pytest for mesh topology, loading, and subdivision behavior;
manual GUI checks for interaction and display modes

**Target Platform**: Desktop; Windows as the initial development platform

**Project Type**: Single Python desktop application

**Performance Goals**: Keep interaction responsive for small demonstration
meshes; no explicit large-mesh performance target

**Constraints**: Input components must be manifold; triangularize polygonal OBJ
faces during loading; show clear errors for unreadable or unsupported topology.
VTK subdivision filters are applied to connected components individually and
the results are combined.

**Scale/Scope**: One mesh open at a time, two subdivision schemes, two display
modes, and one iteration per key press

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Task-focused simplicity**: Pass. Use existing Python libraries for I/O,
  rendering, UI embedding, and subdivision instead of custom implementations.
- **Clean, readable code**: Pass. Keep the application in a small package with
  separate mesh, subdivision, and viewer responsibilities.
- **Requirements-driven scope**: Pass. No editing, saving, extra schemes, or
  unrelated UI features are included.
- **Preserve behavior**: Pass. This is a new application; invalid input must
  produce a user-visible error without closing the viewer.
- **Proportionate verification**: Pass. Use focused pytest coverage for mesh
  invariants and subdivision, plus manual end-to-end GUI checks.
- **Implementation constraints**: Pass. Python and the half-edge structure are
  user requirements; dependencies are limited to those that directly deliver
  the specified behavior.

## Project Structure

### Documentation (this feature)

```text
specs/001-mesh-subdivision-viewer/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── tasks.md
```

### Source Code (repository root)

```text
pyproject.toml
src/
└── mesh_subdivision_viewer/
    ├── __init__.py
    ├── __main__.py
    ├── mesh.py
    ├── subdivision.py
    └── viewer.py
tests/
├── test_mesh.py
├── test_subdivision.py
├── test_io.py
└── test_viewer.py
```

**Structure Decision**: Use one installable Python package and a focused pytest
suite. `mesh.py` owns the half-edge representation and conversion to/from the
rendering mesh; `subdivision.py` applies one requested VTK subdivision pass;
`viewer.py` owns the Qt window, file selection, key handling, and rendering.
`__main__.py` provides the application entry point. The project currently has
no source code, so these paths establish its initial structure.

## Complexity Tracking

No constitution violations. The half-edge representation is required by the
specification; VTK-backed subdivision avoids duplicating Loop and Butterfly
algorithm implementations.
