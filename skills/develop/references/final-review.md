# Phase 2: final review

Set the plan's status to `final review`. The scope is the whole change, `<stack-base>...HEAD`, run from the top of the stack. Take a tree fingerprint (see `step-loop.md`).

## 1. Launch the panel

In a single message, launch these six reviewers in parallel:

- `devflow:correctness-reviewer`
- `devflow:security-reviewer`
- `devflow:reliability-reviewer`
- `devflow:performance-reviewer`
- `devflow:tests-reviewer`
- `devflow:design-reviewer`

Give each one:

- the plan path;
- the scope `<stack-base>...HEAD`;
- the list of steps, with each step's branch and commit, so findings can be tagged with where they came from;
- the plan's **Follow-ups** list, so they can judge which items belong in this change.

Keep every agent ID. When they finish, check the fingerprint again.

## 2. Validate

1. **Merge duplicates.** Specialists often report the same root cause from different angles. Merge those into one item, and note every specialist that raised it.
2. **Check each finding yourself.** Read the code path, reproduce the scenario, or run the test. Mark each one **valid**, **invalid** (write the rebuttal with evidence), or **valid but deferred** (out of scope or not worth it, with your reason).
3. **Triage Follow-ups.** Decide which items belong in this change. Any that do and that change the plan, such as a new step or a change of scope, need the user's approval first.

## 3. Fix

Make the valid fixes. Do small ones yourself. For larger ones, use a `devflow:implementer` with the specific findings and the plan path.

Every fix goes on the branch that introduced the problem, lowest branch first (see `git.md`). A cross-cutting fix, such as removing duplication across steps, goes on the lowest branch where it fits. Every bug fix gets a regression test. Run the checks on each branch you touch and on the top branch.

## 4. Re-review

With SendMessage, send each specialist its own findings, with what was fixed (branch and commit) and your rebuttals. Each reports resolved, withdrawn or still open, plus any new findings and a new verdict.

Repeat validate → fix → re-review until every specialist approves, for **at most 3 rounds**. Then settle anything still open yourself. Record each decision as a dispute in the plan, and include it in the final overview.

## 5. Docs and specs

Check that the README, design docs, requirements status and API spec (for example `api/openapi.yaml`) describe what was built. Put each update on the branch whose step introduced the behavior. Then go back to the Finish phase in `SKILL.md`.
