# Simplicity

Look for code to remove. The best version of a change is the smallest one that is still clear and correct.

- **Simpler alternatives.** Custom code that a standard library feature, framework built-in, project helper or well-known pattern replaces. Features a simpler design makes unnecessary.
- **Duplication.** Logic copied within the change or from existing code, including helpers that several steps each re-implemented. Name the one place it should live.
- **Over-engineering.** Interfaces, generics, options or config with a single use. Wrappers that only forward calls. Extension points or flexibility no requirement asks for.
- **Defensive bloat.** Checks for states the types or callers rule out. `try`/`catch` that only rethrows, or logs and continues. Fallbacks for situations that can't happen. Re-validating data already validated at the boundary. Handling for inputs the Quality bar rules out.
- **Fix bloat.** Review-round fixes that handle more than their scenario, or bolt on a special case where a small restructure would remove the problem.
- **Dead code.** Unused functions, parameters, fields, exports, flags and config; unreachable branches; leftover scaffolding or debug code. Search for callers before you claim something is unused.
- **Dependencies.** A new dependency that a few lines or something already in the project would replace, or the reverse: lots of custom code that an existing dependency covers.

A simplification must keep every behavior the plan needs. Show the simpler result and roughly how many lines it removes.
