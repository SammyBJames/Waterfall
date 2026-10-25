---
name: review
description: "Runs Waterfall's review outside the full workflow: one reviewer on the working tree, or a base ref for a branch or stack, and --panel for the specialist panel."
argument-hint: "[base-ref] [--panel]"
disable-model-invocation: true
---

# waterfall: review

Arguments: $ARGUMENTS

1. **Scope.** With no base ref, review the working tree vs `HEAD`, including untracked files; with one, review `<ref>...HEAD` plus the working tree. If the scope is empty, say so and stop. If a plan in `.claude/plans/` covers this work, pass its path. Otherwise find the check commands (CI, `CLAUDE.md`, package scripts), run them, and pass the results and a short Quality bar inferred from the project (users, threat model, target scale), and tell reviewers there's no plan.
2. **Review.** By default, launch `waterfall:reviewer`. With `--panel`, launch all seven in parallel, in one message: `waterfall:correctness-reviewer`, `waterfall:security-reviewer`, `waterfall:reliability-reviewer`, `waterfall:performance-reviewer`, `waterfall:tests-reviewer`, `waterfall:design-reviewer` and `waterfall:simplicity-reviewer`.
3. **Validate.** Merge duplicates. Send `traced` blocking findings to a `waterfall:validator` per reviewer, in parallel, with the findings pasted into its prompt. Validators confirm, downgrade or reject each one; proven findings count as confirmed.
4. **Report.** Confirmed blocking findings, most severe first, each with `file:line`, scenario and suggested fix; then if-minor and downgraded findings, the test check, Questions, rejected findings in a line each, and out-of-scope notes. Don't change code unless the user asks.
