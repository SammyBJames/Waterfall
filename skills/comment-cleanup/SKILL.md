---
name: comment-cleanup
description: "Cleans up comments in changed code: a doc comment on every function, inline comments only where the code can't explain itself, and no history. Use when asked to tidy comments or docs, and for devflow's comment pass."
argument-hint: "[base-ref | files...]"
context: fork
model: sonnet
effort: medium
background: false
---

# Comment cleanup

Arguments: $ARGUMENTS

Bring comments in scope up to these rules. Change only comments: never code, formatting or behavior.

## Scope

- No arguments: functions and methods added or changed in the working tree vs `HEAD`, including untracked files.
- A base ref: functions added or changed in `<ref>...` plus the working tree.
- File or folder paths: everything in them.

In changed files, touch only comments on functions the change added or altered, plus any comment the change made false. List stale comments elsewhere in your summary instead of fixing them.

## Rules

1. **Every function and method gets a doc comment,** including private ones and test helpers, but not test cases whose names say what they check. Say what it does and, if not obvious, why it exists, plus what a caller must know: inputs and outputs, units, errors, side effects, invariants, ordering. One sentence is often enough. Don't restate the signature or narrate the body.
2. **Inline comments are rare.** Keep one only for what the code can't say: a non-obvious reason, a workaround and its cause, a subtle invariant, a tricky algorithm, or a reference such as an RFC section. Delete comments that restate the code. If a comment explains *what* the code does, note in your summary that a better name would help; don't rename anything.
3. **Comments describe the code as it is.** Remove history and process: "now", "new", "changed to", "previously", "no longer", "fixed", "added for step 3", "per the reviewer", "per the plan". Remove commented-out code and untracked TODOs.
4. **Comments must be true.** Check each one you keep against the names, parameters, units, error behavior and references in the code.
5. **Match the language and the file:** rustdoc `///` and `//!`, JSDoc or TSDoc `/** */`, Python docstrings, KDoc, Go comments starting with the name. Use markup such as `@param` only where the project already does.
6. **Be brief and plain.** No filler or marketing words.

## Finish

Run the project's formatter or linter if it checks comments, and confirm your diff changes only comments. Reply with the files touched, roughly how many comments you added, rewrote and removed, and any stale comments or naming problems you noticed outside scope.
