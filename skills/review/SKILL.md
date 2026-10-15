---
name: review
description: "Run devflow's adversarial review outside the full workflow. By default one reviewer checks the working tree; pass a base ref to review a branch or stack, and add --panel to run the six-specialist panel instead."
argument-hint: "[base-ref] [--panel]"
disable-model-invocation: true
---

# devflow: review

Arguments: $ARGUMENTS

1. **Scope.** With no base ref, review the working tree vs `HEAD`, including untracked files. With a base ref, review `<ref>...HEAD` plus the working tree. If the scope is empty, say so and stop. If a devflow plan in `.claude/plans/` covers this work, pass its path. Otherwise, give the reviewers the check commands you find (CI workflows, `CLAUDE.md`, package scripts), and tell them there's no plan and to judge against the code's evident intent and the project's standards.
2. **Run the review.**
   - Default: launch `devflow:reviewer`.
   - `--panel`: launch these six in parallel, in one message: `devflow:correctness-reviewer`, `devflow:security-reviewer`, `devflow:reliability-reviewer`, `devflow:performance-reviewer`, `devflow:tests-reviewer`, `devflow:design-reviewer`.
3. **Validate.** Merge duplicate findings. Check each finding yourself against the code, and mark it confirmed, doubtful (with why) or invalid (with why). Drop the invalid ones from the main list, but mention them briefly.
4. **Report.** List the confirmed findings, most severe first, each with `file:line`, the scenario and the suggested fix. Then the test check and coverage gaps, the doubtful findings, and out-of-scope notes. Don't change any code unless the user asks you to fix things afterwards.
