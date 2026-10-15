# Design and simplicity

The owner wants the simplest implementation that meets their requirements, with as little code and as few dependencies as possible. The best version of a change is usually the smallest one that is still clear and correct.

- **Simpler alternatives.** Could a standard library feature, a framework built-in, an existing project helper, or a well-known pattern replace custom code? Could a feature be dropped because a simpler design makes it unnecessary? Show the alternative concretely.
- **Duplication.** Logic copied within the change, or between the change and existing code. In the final review, look especially for helpers that several steps each re-implemented a little differently. Point to the one place it should live.
- **Non-standard patterns.** Home-made versions of well-known patterns or protocols (state machines, retries, caching, migrations, auth flows, parsing). Code that breaks the project's existing conventions for structure, naming, error handling or layering.
- **Dead code.** Unused functions, parameters, fields, exports, feature flags, configuration, branches that can't be reached, and leftover scaffolding or debug code. Search for callers before you claim something is unused.
- **Abstractions.** Interfaces, generics, traits or config added for a single use. Wrappers that only forward calls. Indirection that makes the code harder to follow without buying anything.
- **Boundaries.** Logic in the wrong layer, for example business rules in handlers or UI, or SQL leaking into the view. Modules that know too much about each other. Public APIs bigger than they need to be.
- **Naming and shape.** Names that mislead. Functions that do several unrelated things. Long parameter lists that should be a struct.
- **Dependencies.** Any new dependency must be clearly worth it compared with a few lines of code or something already in the project.

For each finding, show what the simpler result would look like and roughly how much code it removes.
