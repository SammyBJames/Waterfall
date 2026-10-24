# Correctness

Work out what the code should do from the plan, the requirements and any spec. Then try to break it.

- **Requirements and spec.** Behavior that differs from the plan step, requirements or API spec: status codes, error shapes, field names, nullability. Check both directions: what the code does that the spec doesn't describe, and the reverse.
- **Boundaries.** Empty, one, many and maximum. Zero, negative and overflow. Off-by-one in ranges, pagination, slicing and cursors. Unicode, case and whitespace in names and keys.
- **State and ordering.** Running twice, out of order, or after a partial failure. Invariants broken on an exit path (early return, `?`, `throw`).
- **Conditions.** Inverted or incomplete conditions, `&&` vs `||`, a missing `else`, match arms that fall through to a wrong default, truthiness traps (`0`, `""`, `NaN`, `None`).
- **Data handling.** Lost precision (money as floats, time zones and DST, ms vs s). Lossy conversions, unhandled parse failures, defaults that hide a missing field.
- **Seams.** Callers that rely on behavior the change altered. Types that allow states the code doesn't handle. Schema, migration and code that disagree.
- **Error paths.** Errors swallowed, mapped to the wrong kind, reported as success, or with misleading messages.
- **Concurrency logic.** Check-then-act races, lost updates from read-modify-write, stale client state sent back to the server.

**Not reported:** inputs the types, callers or boundary validation already rule out; failures only on inputs the Quality bar excludes; code that looks wrong but isn't (check before you claim it).
