# Performance

Judge costs at the Quality bar's target scale, with realistic data rather than test fixtures.

- **Queries.** N+1 patterns and queries in loops. Loading whole tables or rows when a count, exists check or a few columns would do. Missing indexes for the `WHERE`, `JOIN` and `ORDER BY` columns used, checked against the migrations (`EXPLAIN` where you can). Missing pagination. Long write transactions that block others.
- **Algorithms.** Quadratic loops over collections that grow. Repeated work that could be done once. Sorting or copying large collections per request or render.
- **Blocking.** CPU-heavy or blocking I/O on async executors or UI threads. Sequential awaits that could run concurrently. Large payloads that should stream.
- **Memory.** Large buffers held too long. Unbounded caches. Cloning big structures in hot paths. Leaks through closures, listeners or global registries.
- **Frontend and network.** Cascading reactive effects. Large lists without keys or virtualization. Bundle size from new dependencies. Request waterfalls, chatty protocols, payloads far bigger than the client uses.
- **Hot loops.** Logging, allocation or locking inside tight loops.

**Not reported unless the cost is concrete at the target scale:** quadratic work on small capped lists, one-off startup queries, micro-optimizations off the hot path, and caching, batching or streaming with no measured or estimated need.

Estimate the cost: "O(n) queries per page, about 100 per request at the target scale" is a finding; "this might be slow" is a question. Measure in the snapshot when cheap.
