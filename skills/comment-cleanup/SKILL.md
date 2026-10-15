---
name: comment-cleanup
description: "Clean up code comments: a useful doc comment on every function or method, inline comments only where the code can't explain itself, and every comment describing the current code rather than its history. Use when asked to clean up, tidy, or fix comments or docs in code, and as the comment pass in the devflow workflow."
argument-hint: "[base-ref | files...]"
---

# Comment cleanup

Bring comments in scope up to these rules. **Change only comments.** Never change code, formatting outside comments, or behavior.

## Scope

- No arguments: functions and methods added or changed in the working tree compared with `HEAD`, including untracked files.
- A base ref (for example `main`, or a stack's base branch): functions added or changed in `<ref>...` plus the working tree.
- File or folder paths: everything in them. Use this only when the user names them.

Within a changed file, only touch comments on functions and methods the change added or altered, plus any comment the change made false. Stale comments you notice elsewhere get listed in your summary, not fixed.

## Rules

1. **Every function and method gets a doc comment.** That includes private ones and test helpers, but not test cases whose name already says what they check. A doc comment says what the function does and why it exists when that isn't obvious. It also covers what a caller must know: meaning of inputs and outputs, units, errors or panics, side effects, invariants, concurrency or ordering requirements. One sentence is often enough. Don't restate the signature or narrate the body.
2. **Inline comments are rare.** Keep or add one only where the code can't make itself clear: a non-obvious reason, a workaround with its cause, a subtle invariant, a tricky algorithm, or a reference such as an RFC section or upstream issue. Delete comments that restate the code. If an inline comment explains *what* the code does, a better name usually does the job; mention that in your summary instead of renaming anything.
3. **Comments describe the code as it is now.** Remove or rewrite history and process: "now", "new", "changed to", "previously", "no longer", "fixed", "added for step 3", "as the reviewer suggested", "per the plan". Also remove commented-out code and TODOs that aren't tracked in an issue or the plan's follow-ups.
4. **Comments must be true.** Check each one you keep against the code: names, parameters, units, error behavior, and referenced functions or sections. Fix the ones that are wrong.
5. **Follow the language's conventions and the file's existing style:** `///` and `//!` rustdoc, `/** */` JSDoc or TSDoc, Python docstrings, KDoc, Go doc comments starting with the name. Match the file's tone and length. Doc markup such as `@param` belongs only where the project already uses it.
6. **Be brief.** Write plain, direct sentences. No filler, and no marketing words ("robust", "seamless", "powerful").

## Finish

Run the project's formatter or linter if it checks comments (for example `cargo clippy` with missing-docs lints, `eslint` JSDoc rules). Review your diff to confirm that only comments changed.

Summarize in a few lines: the files you touched, roughly how many comments you added, rewritten and removed, and any stale comments outside scope or naming problems you noticed.
