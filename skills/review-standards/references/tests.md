# Tests

The question is whether the tests would catch the bugs they claim to catch, and whether the important behavior is tested at all.

- **Mutations.** Use the mutation procedure in the review standards on every new or changed piece of logic. A surviving mutation is a finding.
- **Coverage map.** For each new or changed branch, error path, boundary and requirement, name the test that covers it. Each gap is a finding with the test you want added: its case, input and expected result.
- **Assertions.** Tests that pass without checking the outcome. Snapshot tests that would accept any output. Assertions on mocks instead of behavior. Expected values that were computed by the code under test, or were simply wrong.
- **Realism.** Mocks that hide the behavior under test. Fixtures too small to hit pagination, batching or limits. No test with the real database, file system or protocol where those matter.
- **Isolation and flakiness.** Tests that depend on order, wall-clock time, sleeps, network, randomness without a seed, or shared global state.
- **Regression tests.** Every bug fixed in this change should have a test that fails without the fix.
- **Placement and naming.** Do the tests follow the project's conventions for location, naming and helpers? Do the names describe the behavior they check?
- **Test code quality.** Duplicated setup that should use an existing helper. Tests so long or clever that a reader can't tell what they check.

Test vectors for standards (RFCs, crypto, encodings) must come from the standard itself, not from memory.
