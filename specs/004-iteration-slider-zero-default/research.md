# Research: Zero-Default Iteration Slider

## Existing Project Findings

- `MeshViewerWindow` initializes `_iteration_count` to 0 and the horizontal slider supports values 0–4.
- `_update_iteration_count` updates selection feedback only; it does not subdivide the mesh.
- The `N` shortcut invokes the explicit subdivision action. The existing `M` action decreases the selected count without applying subdivision; there is no keyboard action to increase the count yet.
- The iteration label describes the selected count, while `_applied_iterations` tracks the count represented by the displayed mesh.
- `subdivide_selected` compares only the selected and applied iteration counts. If the count is unchanged, it returns early even when `_scheme` changed since the displayed result was produced.
- `_select_scheme` changes the selected scheme without changing `_iteration_count` or the displayed mesh. This preserves the count, but pressing `N` at the same applied count currently does not recompute the mesh under the new scheme.
- When the selected count decreases, `subdivide_selected` recomputes from `_loaded_mesh`; when it increases, it applies the difference to the current mesh.
- Successful result feedback reports the resulting applied iteration count and face counts. Repeated application currently reports an already-applied message.
- `reset_mesh` restores the loaded mesh and sets the applied count to zero without changing `_iteration_count`.
- The project uses PySide6 Qt controls and pytest tests in `tests/test_viewer.py`; no new dependency or public API is needed.

## Decisions

### Use zero as the initial iteration selection

- **Decision**: Initialize selected iterations to zero and keep the slider range at 0–4.
- **Rationale**: This places the thumb at the far-left position and communicates that no subdivision iteration is selected or applied at startup.
- **Alternatives considered**: Keeping one as the default conflicts with the requested initial position and the new specification.

### Separate selection from application

- **Decision**: The slider and `+`/`-` keyboard actions update only the selected iteration count and selection feedback. `N` and the explicit subdivision menu action apply the selection.
- **Rationale**: This distinguishes a setting from a change to the displayed mesh and matches feature 003's documented two-step interaction.
- **Alternatives considered**: Applying immediately on slider movement makes it impossible to inspect a selected value without changing the mesh and conflicts with FR-004.

### Make zero a no-op, not a reset

- **Decision**: A subdivision command with zero selected iterations leaves the displayed mesh and applied count unchanged and reports that no subdivision occurred. Reset remains a separate command.
- **Rationale**: The specification defines zero as no selected iteration and explicitly requires the zero-count attempt not to change geometry.
- **Alternatives considered**: Treating zero as reset would conflate selection with a separate mesh-state command and violate the acceptance scenario.

### Align keyboard controls and state feedback

- **Decision**: Keep `N` bound to applying the selected count, add `+` and `-` to adjust the selected count, and keep the label associated with selection while result feedback describes the current mesh.
- **Rationale**: `N` remains a predictable apply command; count adjustment is available without a mouse and does not apply subdivision.
- **Alternatives considered**: Using `N` to both change the count and apply it would make it difficult to apply an unchanged selection and would conflate selection with execution.

### Reapply when the subdivision scheme changes

- **Decision**: Track which scheme produced the displayed subdivision result. If the selected scheme differs when the user invokes `N`, recompute the selected iteration count from the loaded mesh using the newly selected scheme.
- **Rationale**: Scheme selection alone remains non-destructive, but applying after a scheme change must not silently do nothing merely because the selected count equals the previous applied count.
- **Alternatives considered**: Requiring users to reset manually before every scheme comparison preserves the old behavior but adds an easily missed extra step and does not satisfy the requested workflow.

### Describe successful state without double-count ambiguity

- **Decision**: Report the resulting applied count, and handle an already-applied selection with a clear “already applied” message rather than reporting zero new passes against a positive total.
- **Rationale**: Users need to understand the resulting mesh state, not the internal difference between the requested count and previously applied count.
- **Alternatives considered**: Retaining the existing “new passes (total)” phrasing continues to produce the exact confusing zero-versus-total message addressed by the specification.
