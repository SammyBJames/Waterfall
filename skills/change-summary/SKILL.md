---
name: change-summary
description: "Summarizes a code change for review: how it works, a PR description (What Changed / What to Test), and a one-line commit message in the repo's style. Use when asked for a change summary, PR description or commit message."
argument-hint: "[base-ref]"
context: fork
model: sonnet
effort: medium
background: false
---

# Change summary

Arguments: $ARGUMENTS

Scope: the working tree vs `HEAD` (staged, unstaged and untracked), or `<ref>...` plus the working tree if a base ref is given. Read the whole diff and enough surrounding code to explain it. If a devflow plan in `.claude/plans/` covers the change, use its design and decisions for the "why" and link any issues it names.

For the commit message, read `git log --format=%s -30` and match the history's mood, capitalization, prefixes and length. Write one line under about 72 characters saying what the change does for the project.

Reply with exactly these three sections and nothing else, readable in under two minutes:

````markdown
## How it works
A few short paragraphs or a compact list: the main types, functions or modules, how data flows, and new concepts by name. Point to `file:line` for what to read first. Explain decisions a reviewer might question, and what was left out. Not a file-by-file tour.

## PR description
```markdown
### What Changed
- Behavior changes and why, in a few bullets.
- Issues: #123 (only if known)

### What to Test
- [ ] Steps a person can follow, each with its expected result, including at least one edge case or failure path.
- [ ] Automated: the test commands and what they now cover.
```

## Commit message
```
<one line>
```
````
