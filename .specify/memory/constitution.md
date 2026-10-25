<!--
Sync Impact Report
Version change: unversioned template -> 1.0.0 (initial adoption)
Modified principles: none; all five principles are newly defined.
Added sections: Implementation Constraints; Development Workflow.
Removed sections: none.
Follow-up TODO: Confirm the original ratification date.
-->

# Task One Constitution

## Core Principles

### I. Task-Focused Simplicity
Implement the simplest solution that fully meets the stated requirements. Do not add
features, configuration, or abstractions that the task does not require. Keep complexity
proportionate to the problem.

### II. Clean, Readable Code
Use clear names, cohesive units, and the project's established conventions. Avoid
unnecessary duplication and indirection. Introduce abstractions only when they make the
required behavior clearer or easier to maintain.

### III. Requirements-Driven Scope
Every change MUST serve a stated requirement or be necessary to implement it correctly.
Keep unrelated files and behavior unchanged. Resolve minor ambiguities with the simplest
reasonable interpretation; ask for clarification when an ambiguity materially affects
behavior.

### IV. Preserve Existing Behavior
Preserve existing behavior and compatibility unless the task explicitly requires a change.
When a required change affects existing behavior, identify the impact and verify the new
behavior.

### V. Proportionate Verification
Verify changed behavior using the project's existing tests and quality checks where
available. Add or update tests for changed behavior when appropriate. Do not introduce
new tooling solely for a task unless it is necessary to verify its requirements.

## Implementation Constraints

Use the existing technology stack and project patterns. Add dependencies only when they
are necessary to meet a requirement and no suitable existing capability is available.
Do not impose project-wide conventions or technical requirements that are not established
by the repository or needed by the task.

## Development Workflow

Before changing code, inspect the relevant implementation and tests. Make a focused,
complete change, then run the smallest existing checks that verify it. Review the final
diff for unrelated changes and confirm each changed behavior is tied to a requirement.
Report any verification that could not be performed and why.

## Governance

This constitution governs implementation and review decisions. Amendments require a
documented rationale and approval from the project maintainer. Each amendment MUST update
the version and last-amended date.

Use semantic versioning for this constitution: increase MAJOR for incompatible governance
changes, MINOR for new principles or materially expanded guidance, and PATCH for
clarifications or non-semantic refinements. The ratification date records the original
adoption date and MUST NOT change after it is confirmed.

Every implementation and review MUST check changes against these principles. Any
necessary deviation MUST be explained in the change description or review, with the
reason it is required.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): confirm original adoption date | **Last Amended**: 2026-10-25
