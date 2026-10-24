# Design

Judge how the change fits the plan's design and the project's structure, boundaries and conventions. Size and complexity belong to the simplicity checklist.

- **Plan fit.** Where the change departs from the plan's design or decisions, whether that is better or worse, and whether it was approved.
- **Non-standard patterns.** Home-made versions of well-known patterns or protocols (state machines, retries, caching, migrations, auth flows, parsing). Code that breaks the project's conventions for structure, naming, error handling or layering.
- **Boundaries.** Logic in the wrong layer, such as business rules in handlers or UI, or SQL in views. Modules that know too much about each other. Public APIs bigger than needed.
- **Consistency.** The same job done differently across the change, or differently from the rest of the project.
- **Naming and shape.** Misleading names. Functions that do unrelated things. Long parameter lists that should be a struct.

For each finding, show the better structure and what it costs to get there.
