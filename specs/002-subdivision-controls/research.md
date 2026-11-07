# Research: Subdivision Iteration Controls and Reset

## Existing Project Findings

- The viewer already exposes Loop and Butterfly choices through an exclusive
  Qt action group in the Mesh menu.
- The current `N` shortcut calls `subdivide_mesh` once and displays the returned
  mesh. The function performs exactly one pass and returns a new validated
  mesh with its revision incremented.
- Mesh loading assigns a newly built mesh to viewer state; subdivision does
  not mutate the input mesh in place.
- The viewer tests already exercise menu actions, keyboard shortcuts, the
  displayed mesh, and subdivision state.

## Decisions

### Iteration count selection

- **Decision**: Provide four mutually exclusive choices (1–4) in the existing
  Mesh menu, defaulting to 1, consistent with the existing subdivision-scheme
  menu.
- **Rationale**: This preserves the application's existing interaction style
  and makes the allowed values explicit without adding dependencies or a new
  dialog.
- **Alternatives considered**: A free-form numeric input would require
  validation for a value set that has only four allowed choices. A separate
  dialog would add interaction steps for a small setting.

### Applying multiple iterations

- **Decision**: Repeat the existing one-pass subdivision operation using each
  preceding result as the next input. Replace the viewer's displayed mesh only
  after all requested passes succeed.
- **Rationale**: The current operation already performs the required complete
  pass and returns a new mesh. This keeps the algorithm single-purpose and
  avoids displaying a partial result if a later pass fails.
- **Alternatives considered**: Reworking `subdivide_mesh` to change its
  one-pass contract would impact existing callers and tests unnecessarily.

### Reset behavior

- **Decision**: Retain the loaded mesh state as the reset target and restore
  that state on reset. Clear the applied-iteration count while preserving the
  selected scheme and requested iteration count.
- **Rationale**: The requirement is to return to the just-loaded mesh without
  reopening its file. The mesh transformations are non-mutating, so the
  original loaded state can be retained directly.
- **Alternatives considered**: Reloading the source file on reset adds file I/O
  and can fail if the source has moved. Resetting only one pass would not meet
  the requirement to restore the original loaded state.

### User-facing explanation

- **Decision**: Replace the ambiguous "Subdivide once" wording with an action
  label that describes applying the selected number of complete iterations,
  and report the applied iteration count in viewer status feedback.
- **Rationale**: The user specifically does not know what "once" means; stating
  that an iteration is a complete pass over the current mesh clarifies the
  scope of the operation.
- **Alternatives considered**: Relying on documentation alone would leave the
  ambiguous wording in the control itself.
