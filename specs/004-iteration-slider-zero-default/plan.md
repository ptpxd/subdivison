# Implementation Plan: Zero-Default Iteration Control

**Branch**: `004-iteration-slider-zero-default` | **Date**: 2026-11-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/004-iteration-slider-zero-default/spec.md`

## Summary

Initialize the iteration slider at zero and use iteration terminology consistently. Slider and `+`/`-` keyboard controls update the selected iteration count without changing the mesh; `N` applies a positive count. Track the scheme used to create the displayed subdivision result so `N` can recompute from the loaded mesh when the selected scheme changes, while preserving the selected count. A zero selection is a no-op with clear feedback.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: PyVista, PyVistaQt, PySide6

**Storage**: In-memory viewer and mesh state; local STL/OBJ input files

**Testing**: pytest; focused Qt viewer tests and manual GUI acceptance checks

**Target Platform**: Desktop; Windows is the initial development platform

**Project Type**: Single Python desktop application

**Performance Goals**: Preserve current responsiveness for demonstration meshes while applying up to four passes; no large-mesh performance target is established

**Constraints**: Keep the supported iteration range at 0–4. Zero means no iteration selected, not one iteration and not a reset command. Slider and keyboard count changes must not modify the mesh. Reset remains a separate operation and preserves the selected count. A successful load clears the applied count and applied scheme.

**Scale/Scope**: One loaded mesh at a time; update iteration control state and feedback in the existing viewer and cover it in the existing viewer tests. Do not change subdivision algorithms, mesh formats, or dependencies.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Task-focused simplicity**: Pass. Reuse the current slider, labels, and status bar; add only the explicit subdivision menu action needed to apply the selected count. Add no dependencies or new panels.
- **Clean, readable code**: Pass. Keep state transitions in the existing viewer and add focused tests to the existing Qt test module.
- **Requirements-driven scope**: Pass. The design covers zero as the initial selection, keyboard and slider count control, selected versus applied iteration counts, and scheme-aware reapplication.
- **Preserve required behavior**: Pass. Keep the 0–4 range, positive-count subdivision, schemes, mesh loading, and reset behavior. The new zero default supersedes the older default-one requirements.
- **Proportionate verification**: Pass. Test startup value and wording, slider/keyboard non-destructiveness, zero-count no-op, positive-count application, feedback, reset selection preservation, and reapplication after changing schemes.
- **Implementation constraints**: Pass. Use the existing Python, PyVista, PyVistaQt, and PySide6 stack.

## Project Structure

### Documentation (this feature)

```text
specs/004-iteration-slider-zero-default/
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
    └── viewer.py
tests/
└── test_viewer.py
```

**Structure Decision**: Retain the single Python desktop application layout. `viewer.py` owns the slider, selection and applied state, commands, and status feedback; `test_viewer.py` already owns Qt interaction tests. No API contract or separate test module is needed.

## Design Direction

- Initialize the selected iteration count to zero and keep the slider range at zero through four.
- Keep selected iteration count, applied iteration count, and applied scheme as distinct state. The slider label describes the selected count; result feedback describes the displayed mesh.
- Make slider and `+`/`-` selection changes non-destructive. The explicit subdivision command and `N` apply a positive selected count; zero reports that no subdivision was performed and leaves the current mesh untouched.
- If the selected scheme differs from the scheme used for the displayed result, recompute the selected count from the loaded mesh with the selected scheme. Keep reset separate and preserve the selected count.
- Avoid changing subdivision algorithms or the mesh model.

## Complexity Tracking

No constitution violations.
