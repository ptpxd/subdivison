# Implementation Plan: Automatically Apply Iteration Changes

**Branch**: `005-auto-apply-iterations` | **Date**: 2026-11-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/005-auto-apply-iterations/spec.md`

## Summary

Apply a positive iteration count immediately when the slider or `+`/`-`
controls change, and recompute the selected count immediately when the user
changes between Loop and Butterfly. Treat the selection as the desired total
relative to the loaded mesh, preserve zero as a no-op (not a reset), and keep
the current failure behavior transactional so an unsuccessful computation
does not replace the displayed mesh or successful-result summary. Keep `N`
and the explicit subdivision menu action available for reapplying a positive
selection.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: PyVista, PyVistaQt, PySide6

**Storage**: In-memory viewer and mesh state; local STL/OBJ input files

**Testing**: pytest; focused Qt viewer tests and manual GUI acceptance checks

**Target Platform**: Desktop; Windows is the initial development platform

**Project Type**: Single Python desktop application

**Performance Goals**: Preserve current responsiveness for demonstration
meshes while applying up to four iterations; no large-mesh performance target
is established

**Constraints**: Keep the supported iteration range at 0–4. A selected
positive count is the total result count relative to the loaded mesh. Zero
selection must not change the displayed mesh or applied count. Reset remains
a separate action that restores the loaded mesh and preserves selections.
Failed subdivision must preserve the displayed mesh and successful-result
feedback.

**Scale/Scope**: One loaded mesh at a time; update iteration and scheme
selection transitions in the existing viewer, related user documentation,
and existing viewer tests. Do not change subdivision algorithms, mesh
formats, or dependencies.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Task-focused simplicity**: Pass. Reuse the current slider, scheme menu,
  status bar, result label, and subdivision operation. No new panels,
  dependencies, or architectural layers are needed.
- **Clean, readable code**: Pass. Keep state transitions and application in
  `MeshViewerWindow`; cover them in the existing Qt viewer test module.
- **Requirements-driven scope**: Pass. The design covers immediate
  application for positive slider and keyboard changes, immediate
  scheme-driven recomputation, zero no-op behavior, failure handling, and
  feedback.
- **Preserve required behavior**: Pass. Preserve the 0–4 range, reset and
  loading behavior, mesh display modes, subdivision schemes, and the optional
  `N` shortcut. The automatic interaction supersedes the earlier requirement
  to explicitly apply each selection.
- **Proportionate verification**: Pass. Test mesh and applied-state changes
  after slider, keyboard, and scheme inputs; zero behavior; feedback; no-mesh
  behavior; reset; and transactional failures.
- **Implementation constraints**: Pass. Use the existing Python, PyVista,
  PyVistaQt, and PySide6 stack.

## Project Structure

### Documentation (this feature)

```text
specs/005-auto-apply-iterations/
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
README.md
```

**Structure Decision**: Retain the single Python desktop application layout.
`viewer.py` owns selection, applied-result state, and Qt callbacks;
`test_viewer.py` already contains focused interaction tests. Update the
existing README rather than introducing new documentation surfaces. No API
contract or separate test module is needed.

## Design Direction

- On a positive slider change, update selected state and feedback, then
  automatically invoke the existing subdivision operation.
- The `+` and `-` actions continue to update the slider; therefore, they use
  the same automatic application path without duplicating subdivision logic.
- On a scheme change with a positive selection, retain the selection and
  recompute from the loaded mesh using the newly selected scheme. A scheme
  change at zero does not change the displayed mesh.
- Compute a selected positive total from the loaded mesh whenever the count
  is lower than the applied count or the scheme differs; for a higher count
  under the same scheme, retain the existing incremental path. Keep
  computation in a local variable until all iterations succeed, then update
  displayed mesh and applied-result state together.
- Keep zero as a no-op when the slider is changed to zero. Do not call reset
  implicitly; leave applied count, displayed mesh, and last successful result
  unchanged.
- Preserve `N` and the **Subdivide mesh** action as optional explicit
  reapplication actions, while removing instructions that imply they are
  required after changing a selection.
- Keep the selected-count label separate from feedback for the result
  currently represented by the displayed mesh.

## Complexity Tracking

No constitution violations.
