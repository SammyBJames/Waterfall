# Tests

Would the tests catch the bugs they claim to, and is the important behavior tested at all? Use the mutation and coverage procedure in the review standards.

- **Assertions.** Tests that pass without checking the outcome. Snapshot tests that accept any output. Assertions on mocks instead of behavior. Expected values computed by the code under test, or simply wrong.
- **Realism.** Mocks that hide the behavior under test. Fixtures too small to hit pagination, batching or limits. No test against the real database, file system or protocol where those matter.
- **Flakiness.** Dependence on test order, wall-clock time, sleeps, the network, unseeded randomness or shared global state.
- **Regression tests.** A bug fixed in this change without a test that fails without the fix.
- **Over-testing.** Tests that repeat each other with trivially different inputs, test the framework instead of the change, or pin implementation details so any refactor breaks them.
- **Conventions.** Location, naming and helpers that don't follow the project's. Names that don't say what the test checks. Duplicated setup that an existing helper covers.

Test vectors for standards (RFCs, crypto, encodings) must come from the standard itself.
