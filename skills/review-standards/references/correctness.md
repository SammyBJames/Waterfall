# Correctness: logic flaws and bugs

Work out what the code should do from the plan, the requirements and any spec. Then try to break it.

- **Requirements and spec.** Does the behavior match the plan step, the requirements and the API spec, including status codes, error shapes, field names and nullability? Check both directions: things the code does that the spec doesn't describe, and the reverse.
- **Boundaries.** Empty, one item, many items, maximum size. Zero, negative and overflow. Off-by-one in ranges, pagination, slicing and cursors. Unicode, case and whitespace in names and keys.
- **State and ordering.** What if this runs twice, out of order, or after a partial failure? Are invariants kept across every exit path, including early returns and `?` or `throw`?
- **Conditions.** Inverted or incomplete conditions, `&&` vs `||`, a missing `else`, match or switch arms that fall through to a wrong default, truthiness traps (`0`, `""`, `NaN`, `None`).
- **Data handling.** Lost precision (money as floats, timestamps across time zones and DST, millisecond vs second units). Lossy conversions, parse failures, default values that hide a missing field.
- **Contracts at the seams.** Callers that rely on behavior the change altered. Types that allow states the code doesn't handle. Places where a schema, migration and code disagree.
- **Error paths.** Errors swallowed, mapped to the wrong kind, or reported as success. Messages that mislead.
- **Concurrency logic.** Check-then-act races, lost updates from read-modify-write, and stale client state sent back to the server.

Prove each bug with a scenario, and where you can, with a failing test in the snapshot.
