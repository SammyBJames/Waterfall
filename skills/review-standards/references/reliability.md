# Reliability

Ask what happens when things go wrong, partly wrong, or slowly.

- **Partial failure.** Multi-step writes that can stop halfway. Are they in a transaction, idempotent, or resumable? Files written in place instead of to a temp file plus rename. Caches and the database drifting apart.
- **Retries and idempotency.** Retried requests or messages applied twice. Missing idempotency keys or dedup. Retry loops without backoff, jitter or a cap.
- **Concurrency.** Data races. Locks held across `await` or I/O. Lock order that can deadlock. Poisoned mutexes. Blocking calls on async runtimes (use `spawn_blocking` or similar). Unbounded queues or channels. Tasks and timers that outlive their owner.
- **Resources.** File handles, connections, child processes, subscriptions and listeners that aren't released on every path. Memory or disk that grows without bound (logs, caches, temp files, history tables).
- **Timeouts and cancellation.** Network or IPC calls without timeouts. Cancelled work that leaves inconsistent state. Shutdown that drops in-flight work.
- **Restart and upgrade.** Does state survive a restart? Do migrations run safely on existing data, and are they ordered and repeatable? Is there a sensible path forward when old clients or old data meet new code?
- **Errors and visibility.** Panics or unchecked unwraps on paths that can fail. Errors swallowed so failures are silent. When something breaks, is there enough logging to see what and where, without logging secrets or personal data?
- **Mobile and network.** Network changes, background limits, process death, reconnects that duplicate or lose messages, and offline queues.

Back each finding with the sequence of events that triggers it.
