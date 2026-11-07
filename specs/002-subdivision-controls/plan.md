# Implementation Plan: Subdivision Iteration Controls and Reset

**Branch**: `002-subdivision-controls` | **Date**: 2026-11-07 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-subdivision-controls/spec.md`

## Summary

Add a one-to-four iteration selector, clarify that subdivision applies complete
passes to the current mesh, and add a reset action that restores the mesh state
from the most recent successful file load. Preserve the existing one-pass
default and subdivision schemes. Reuse the current Qt menu patterns and
single-pass `subdivide_mesh` operation, applying the requested passes
successively and updating displayed state only after the requested operation
completes successfully.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: PyVista, PyVistaQt, PySide6

**Storage**: Loaded STL/OBJ files and in-memory mesh state; no persistent application data

**Testing**: pytest; focused subdivision and Qt viewer tests, plus manual GUI acceptance checks

**Target Platform**: Desktop; Windows is the initial development platform

**Project Type**: Single Python desktop application

**Performance Goals**: Apply up to four subdivision passes on the demonstration meshes while keeping the viewer responsive; no large-mesh performance target is established

**Constraints**: Preserve current one-pass behavior as the default. Each pass operates on the previous pass's result. Reset restores the latest successfully loaded mesh, retains the selected scheme and iteration count, and reports zero applied iterations.

**Scale/Scope**: One loaded mesh at a time; iteration selection from one through four; existing Loop and Butterfly schemes; reset to loaded state. No save or per-operation undo.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Task-focused simplicity**: Pass. Reuse the existing single-pass subdivision
  function and Qt menu pattern; add no new dependencies or general-purpose
  framework.
- **Clean, readable code**: Pass. Keep UI state in the viewer and mesh
  transformations in the existing subdivision module.
- **Requirements-driven scope**: Pass. The design is limited to iteration
  selection, explanatory UI wording, and reset.
- **Preserve existing behavior**: Pass. The default remains one iteration,
  existing schemes and display mode remain available, and one selected pass
  preserves current behavior.
- **Proportionate verification**: Pass. Extend existing pytest coverage for
  single/multiple passes, reset, and viewer actions; manually verify visible
  behavior.
- **Implementation constraints**: Pass. The design uses the existing Python,
  PyVista, PyVistaQt, and PySide6 stack.

## Project Structure

### Documentation (this feature)

```text
specs/002-subdivision-controls/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── tasks.md              # Created by /speckit-tasks
```

### Source Code (repository root)

```text
src/
└── mesh_subdivision_viewer/
    ├── mesh.py
    ├── subdivision.py
    └── viewer.py
tests/
├── test_subdivision.py
└── test_viewer.py
```

**Structure Decision**: Keep the existing single Python desktop application
structure. Iteration selection, reset action, and loaded-mesh state belong in
`viewer.py`; repeated refinement continues to use `subdivision.py`'s existing
single-pass operation. Focused behavior tests belong in the existing
subdivision and viewer test modules. No external service or public library
interface is introduced, so no separate contracts directory is needed.

## Complexity Tracking

No constitution violations.
