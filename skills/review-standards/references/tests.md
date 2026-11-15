# Tests

Would the tests catch the bugs they claim to, and is the important behavior tested at all?

- **Assertions.** Tests that pass without checking the outcome. Snapshot tests that accept any output. Assertions on mocks instead of behavior. Expected values computed by the code under test, or simply wrong.
- **Realism.** Mocks that hide the behavior under test. Fixtures too small to hit pagination, batching or limits. No test against the real database, file system or protocol where those matter.
- **Flakiness.** Dependence on test order, wall-clock time, sleeps, the network, unseeded randomness or shared global state.
- **Regression tests.** A bug fixed in this change without a test that fails without the fix.
- **Over-testing.** Tests that repeat each other with trivially different inputs, test the framework instead of the change, or pin implementation details so any refactor breaks them.
- **Conventions.** Location, naming and helpers that don't follow the project's. Names that don't say what the test checks. Duplicated setup that an existing helper covers.

Test vectors for standards (RFCs, crypto, encodings) must come from the standard itself.

## Mutations and coverage

Mutate new or changed logic that makes real decisions: conditions, calculations, error paths, state changes. Skip glue, plain data and pass-through code.

1. Make one realistic mutation per piece in your review worktree: flip a condition, shift a boundary by one, delete a call or early return, swap arguments, return a default, drop an error path.
2. Run only the tests meant to cover it, by name or filter (`cargo test -q -p <crate> <test_name>`, `pytest -q path::test`, `vitest run <file> -t <name>`). Script the apply, run and revert loop for all your mutations in one command.
3. Record killed or survived, then undo it with `git -C "$wt" checkout -- .`.
4. A survivor means a test misses the bug it should catch: name the test and the missing assertion.

Use the project's mutation tool on the changed code if it has one (`cargo mutants --in-diff`, Stryker `--mutate`); don't add one.

**Coverage:** map each behavior the change adds or alters (done-criteria, requirements, error paths users can hit) to the test that covers it. For each gap that matters, give the test to add: case, input, expected result. Don't ask for a test per branch or input permutation.
