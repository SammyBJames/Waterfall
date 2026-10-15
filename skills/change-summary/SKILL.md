---
name: change-summary
description: "Summarize a code change for review: a high-level overview of how the changed parts work, a brief PR description (What Changed / What to Test), and a suggested one-line commit message that matches the repository's history. Use when asked for a change summary, PR description, or commit message, and at each devflow hand-off."
argument-hint: "[base-ref]"
---

# Change summary

**Scope:** the working tree compared with `HEAD` (staged, unstaged and untracked files). If a base ref is given, use `<ref>...` plus the working tree instead.

Read the whole diff and enough surrounding code to explain how the changed parts work. If there's a devflow plan (`.claude/plans/*.md`) for this change, use its design, step and decisions for the "why", and link any issues it names.

Print the summary in exactly three sections:

````markdown
## How it works
A short, high-level explanation for someone reviewing the change. Describe the moving parts and how they fit together: the main types, functions or modules, the data flow, and new concepts with their names. Point to `file:line` for the parts worth reading first. Explain any decision a reviewer might question. Mention what was deliberately left out. Aim for a few short paragraphs or a compact list, not a file-by-file tour.

## PR description
```markdown
### What Changed
- What changed in behavior, and why, in a few bullets.
- Issues: #123 (only if known)

### What to Test
- [ ] Concrete steps a person can follow, with the expected result for each: commands to run, pages or screens to open, inputs to try, including at least one edge case or failure path.
- [ ] Automated: the test command(s) and what they now cover.
```

## Commit message
```
<one line>
```
````

## Commit message

First read `git log --format=%s -30` and match the repository's style: tense or mood ("Add" or "Added"), capitalization, prefixes such as conventional-commit types or scopes if the history uses them, and typical length. Write one line under about 72 characters that says what the change does for the project, not how. No trailing period unless the history uses one.

Keep the whole summary brief. A reviewer should be able to read it in under two minutes.
