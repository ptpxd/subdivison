# Research: Subdivision Controls and Result Feedback

## Existing Project Findings

- The viewer has exclusive Loop/Butterfly scheme actions and exclusive 1–4
  iteration-count actions in the Mesh menu.
- Selecting either setting updates only viewer selection state and status-bar
  text; it does not call the subdivision operation.
- The **Subdivide mesh** action and `N` shortcut call
  `subdivide_selected`, which applies the chosen number of passes to the
  currently displayed mesh.
- Successful feedback currently reports scheme and applied pass counts, but
  not the before-and-after face counts.
- Subdivision calculates into a local variable and only replaces `self._mesh`
  after all passes complete. Failures report an error and retain the prior
  displayed mesh and applied-iteration total.
- Reset restores the latest successfully loaded mesh, permitting comparisons
  from a consistent baseline.

## Decisions

### Explain settings versus applying subdivision

- **Decision**: Add concise guidance to the scheme and iteration controls and
  to the subdivision action, stating that settings apply only when the user
  invokes **Subdivide mesh** or presses `N`.
- **Rationale**: The current operation model is already correct but the
  distinction between configuration and execution is not obvious to users.
  Contextual help and action wording clarify it without changing behavior.
- **Alternatives considered**: Automatically applying subdivision when a
  setting changes contradicts the intended two-step interaction and could
  unexpectedly refine the mesh.

### Report operation result

- **Decision**: Capture the displayed mesh face count before subdivision and,
  after every requested pass succeeds, report the selected scheme, requested
  pass count, and before/after face counts in the existing status feedback.
- **Rationale**: Face counts provide a measurable confirmation that the
  topology became more detailed, independent of how visually different a
  particular input appears.
- **Alternatives considered**: Reporting vertex counts or relying on a visual
  change alone is less directly tied to the subdivision into triangular
  faces. A new results panel would add UI complexity without being necessary
  for the requested feedback.

### Preserve last successful state on failure

- **Decision**: Keep operation summary values tied to successful operations;
  on failure show the error, leave the current mesh and successful-operation
  statistics unchanged, and do not emit success feedback.
- **Rationale**: This preserves the existing transactional multi-pass
  subdivision behavior and makes failures distinguishable from successful
  results.
- **Alternatives considered**: Updating counters or statistics during each
  pass risks showing partial success when a later pass fails.

### Compare schemes

- **Decision**: Use the existing reset action to return to the last loaded mesh
  before applying the other scheme; changing the scheme affects future
  subdivision only.
- **Rationale**: This makes the comparison fair and avoids reprocessing a
  previously subdivided result under a different scheme.
- **Alternatives considered**: Changing schemes on an already refined mesh
  without resetting would not compare the two methods from the same input.
