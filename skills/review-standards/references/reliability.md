# Reliability

Ask what happens when things fail, partly fail, or run slowly, in the environment the Quality bar describes.

- **Partial failure.** Multi-step writes that can stop halfway without a transaction, idempotency or resume. Files written in place instead of temp file plus rename. Caches drifting from the database.
- **Retries.** Retried requests or messages applied twice where retries actually happen.
- **Concurrency.** Data races. Locks held across `await` or I/O. Lock orders that can deadlock. Blocking calls on async runtimes. Tasks and timers that outlive their owner.
- **Resources.** Handles, connections, child processes and listeners not released on every path. Logs, caches, temp files or tables that grow without bound.
- **Restart and upgrade.** State lost on restart. Migrations that are unsafe on existing data, out of order, or not repeatable. Old clients or data meeting new code.
- **Errors and visibility.** Panics or unchecked unwraps on fallible paths. Swallowed errors that make failures silent. Too little logging to see what broke, or logging of secrets or personal data.

**Not reported unless the Quality bar makes it a concrete risk:**

- timeouts, backoff, jitter and retry caps on calls to local or trusted components;
- bounds on queues, channels and caches whose size the code controls;
- network changes, background limits, process death and offline queues outside mobile or flaky-network targets;
- graceful shutdown of work that is safe to lose or redo.

Back each finding with the sequence of events that triggers it.
