# Performance

Judge the change at the scale the project actually targets. Use the plan or requirements if they state one (for example "100k tracks on a Raspberry Pi 4"). Otherwise assume realistic production data, not test fixtures.

- **Queries.** N+1 patterns. Queries inside loops. Loading whole tables or whole objects when a count, an exists check, or a few columns would do. Missing indexes for the `WHERE`, `JOIN` and `ORDER BY` columns actually used, checked against the migrations. Use `EXPLAIN` or `EXPLAIN QUERY PLAN` where you can. Missing pagination. Long write transactions that block other users of the database.
- **Algorithms.** Quadratic loops over collections that can grow. Repeated work that could be computed once. Sorting or copying large collections on every request or render.
- **Async and blocking.** CPU-heavy or blocking I/O on async executors or UI threads. Serialized awaits that could run concurrently. Missing streaming for large payloads.
- **Memory.** Large buffers held longer than needed. Unbounded caches. Cloning big structures in hot paths. Leaks through closures, listeners or global registries.
- **Frontend.** Reactive effects that cascade or loop. Re-rendering large lists without keys or virtualization. Bundle size added by new dependencies. Requests in waterfalls.
- **Network.** Chatty protocols. Missing batching or caching headers. Payloads that send far more than the client uses.
- **Hot paths.** Logging, allocation or locking inside tight loops.

Estimate the cost: "O(n) queries per page, about 100 per request at the target scale" is a finding. "This might be slow" is a question. Measure in the snapshot when it is cheap to do so.
