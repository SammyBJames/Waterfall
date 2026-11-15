#!/usr/bin/env python3
"""Runs a Waterfall plan's project checks once per working tree and caches the result.

usage: checks.py <checks.json> [--wait SECONDS] [--only NAME,...] [--cached] [--rerun]

The result is keyed by the working tree's content (tree.sh fingerprint) and the
check commands, so running it again on an unchanged tree prints the stored result
instantly. That is what lets the implementer run the full suite once and everyone
after it verify without rerunning anything. Results are written by this script,
not by an agent, so a cached PASS can be trusted.

The checks run in a detached process, so a tool timeout never kills them: if they
take longer than --wait seconds (default 540), the command exits 3 and running it
again keeps waiting on the same run. Only one run per worktree is active; starting
one for a changed tree stops the run for the old tree, whose result could no
longer be used anyway. If the tree changes while checks run, the result is
discarded.

checks.json: {"checks": [{"name": "rust-test", "run": "cargo test -q", "group": "rust",
                          "dir": "web", "timeout": 3600}, ...]}
Checks in different groups run in parallel; checks in one group run in order.
`dir` is relative to the repo root; `group` defaults to the name; `timeout` (seconds)
defaults to 3600.

Exit codes: 0 all passed, 1 a check failed, 3 still running, 4 no cached result
(--cached), 2 usage or setup error.
"""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

TREE_SH = Path(__file__).resolve().parent / "tree.sh"
TAIL_LINES = 40
KEEP_RESULTS = 40
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def git(top, *args):
    """Returns a git command's trimmed stdout in the given directory."""
    return subprocess.run(["git", "-C", str(top), *args], check=True, capture_output=True, text=True).stdout.strip()


def fingerprint(top):
    """Returns the hash of the working tree's tracked and untracked, non-ignored files."""
    return subprocess.run([str(TREE_SH), "fingerprint"], cwd=top, check=True, capture_output=True, text=True).stdout.strip()


def cache_dir(top):
    """Returns this repo's checks cache, shared by its worktrees and matching tree.sh's layout."""
    common = git(top, "rev-parse", "--path-format=absolute", "--git-common-dir")
    main = os.path.dirname(common) if os.path.basename(common) == ".git" else common
    base = os.environ.get("WATERFALL_CACHE") or os.path.join(
        os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "waterfall")
    repo_key = os.path.basename(main) + "-" + hashlib.sha1(common.encode()).hexdigest()[:8]
    path = Path(base) / repo_key / "checks"
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_checks(config, only):
    """Reads the check list, keeping only the named checks when `only` is given."""
    checks = json.loads(Path(config).read_text())["checks"]
    names = [c["name"] for c in checks]
    if len(set(names)) != len(names) or any(not c.get("run") for c in checks):
        raise SystemExit("checks.py: every check needs a unique name and a run command")
    if only:
        unknown = set(only) - set(names)
        if unknown:
            raise SystemExit(f"checks.py: unknown checks: {', '.join(sorted(unknown))}")
        checks = [c for c in checks if c["name"] in only]
    return checks


def alive(pid):
    """Says whether a process with this id is still running, reaping it first if it is our finished child."""
    with contextlib.suppress(ChildProcessError):
        if os.waitpid(pid, os.WNOHANG)[0] == pid:
            return False
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False
    except OSError:
        return False


def write_json(path, data):
    """Writes JSON atomically so readers never see a partial file."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1))
    tmp.replace(path)


def fmt_secs(secs):
    """Formats a duration like 4m12s."""
    secs = int(round(secs))
    return f"{secs // 60}m{secs % 60:02d}s" if secs >= 60 else f"{secs}s"


def run_checks(config, key, top, only):
    """Runs the checks for one tree in this detached process and stores the result."""
    cache = cache_dir(top)
    rundir = cache / key
    rundir.mkdir(exist_ok=True)
    checks = load_checks(config, only)
    tree = key.split("-")[0]
    status = {"started": time.time(), "checks": {c["name"]: {"state": "pending"} for c in checks}}
    lock = threading.Lock()
    write_json(rundir / "status.json", status)
    env = dict(os.environ, NO_COLOR="1", CARGO_TERM_COLOR="never", FORCE_COLOR="0")

    def run_group(group):
        for c in group:
            with lock:
                status["checks"][c["name"]] = {"state": "running", "started": time.time()}
                write_json(rundir / "status.json", status)
            t0 = time.time()
            log = rundir / f"{c['name']}.log"
            with open(log, "w") as out:
                try:
                    code = subprocess.run(["bash", "-c", c["run"]], cwd=top / c.get("dir", "."), stdout=out,
                                          stderr=subprocess.STDOUT, env=env, timeout=c.get("timeout", 3600)).returncode
                    state = "pass" if code == 0 else "fail"
                except subprocess.TimeoutExpired:
                    state = "timeout"
            with lock:
                status["checks"][c["name"]] = {"state": state, "secs": time.time() - t0}
                write_json(rundir / "status.json", status)

    groups = {}
    for c in checks:
        groups.setdefault(c.get("group", c["name"]), []).append(c)
    threads = [threading.Thread(target=run_group, args=(g,)) for g in groups.values()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    status["finished"] = time.time()
    if fingerprint(top) == tree:
        write_json(rundir / "result.json", status)
    else:
        (rundir / "invalid").write_text("the tree changed while the checks ran\n")
    prune(cache)


def prune(cache):
    """Deletes all but the newest stored runs."""
    runs = sorted((p for p in cache.iterdir() if p.is_dir()), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in runs[KEEP_RESULTS:]:
        for f in old.iterdir():
            f.unlink()
        old.rmdir()


def report(rundir, result, cached):
    """Prints one line per check, the failing logs' tails, and returns the exit code."""
    checks = result["checks"]
    took = result["finished"] - result["started"]
    when = f"cached from {fmt_secs(time.time() - result['finished'])} ago, " if cached else ""
    print(f"Checks for tree {rundir.name[:12]} ({when}took {fmt_secs(took)}); logs in {rundir}")
    failed = [n for n, s in checks.items() if s["state"] != "pass"]
    width = max(len(n) for n in checks)
    for name, s in checks.items():
        print(f"{s['state'].upper():8s}{name:{width}s}  {fmt_secs(s.get('secs', 0))}")
    for name in failed:
        lines = ANSI.sub("", (rundir / f"{name}.log").read_text(errors="replace")).splitlines()
        print(f"--- {name}: last {min(TAIL_LINES, len(lines))} lines ---")
        print("\n".join(lines[-TAIL_LINES:]))
    print(f"RESULT: {'FAIL' if failed else 'PASS'}" + (f" ({len(failed)} of {len(checks)} failed: {', '.join(failed)})" if failed else ""))
    return 1 if failed else 0


def progress(rundir):
    """Prints how far a run that is still going has got."""
    try:
        status = json.loads((rundir / "status.json").read_text())
    except (OSError, ValueError):
        print("RUNNING: starting")
        return
    states = status["checks"]
    done = [n for n, s in states.items() if s["state"] in ("pass", "fail", "timeout")]
    running = [f"{n} {fmt_secs(time.time() - s['started'])}" for n, s in states.items() if s["state"] == "running"]
    failed = [n for n, s in states.items() if s["state"] in ("fail", "timeout")]
    print(f"RUNNING: {len(done)} of {len(states)} done" + (f"; failed so far: {', '.join(failed)}" if failed else "")
          + (f"; running: {', '.join(running)}" if running else "") + ". Run the same command again to keep waiting.")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "_run":
        _, _, config, key, top, only = sys.argv
        run_checks(config, key, Path(top), [o for o in only.split(",") if o])
        return 0

    ap = argparse.ArgumentParser(description="Run a Waterfall plan's checks once per working tree.")
    ap.add_argument("config")
    ap.add_argument("--wait", type=int, default=540, help="seconds to wait before returning (default 540)")
    ap.add_argument("--only", default="", help="comma-separated check names to run")
    ap.add_argument("--cached", action="store_true", help="print the stored result for this tree; never start a run")
    ap.add_argument("--rerun", action="store_true",
                    help="discard the stored result for this tree and run again (for a flaky or environmental failure)")
    args = ap.parse_args()

    top = Path(git(Path.cwd(), "rev-parse", "--show-toplevel"))
    config = Path(args.config).resolve()
    only = sorted(o for o in args.only.split(",") if o)
    checks = load_checks(config, only)
    tree = fingerprint(top)
    digest = hashlib.sha1(json.dumps([checks, only], sort_keys=True).encode()).hexdigest()[:8]
    key = f"{tree}-{digest}"
    cache = cache_dir(top)
    rundir = cache / key
    result_file = rundir / "result.json"

    if result_file.exists() and not args.rerun:
        return report(rundir, json.loads(result_file.read_text()), cached=True)
    if args.cached:
        print(f"No stored result for tree {tree[:12]}: the checks haven't run on this exact tree.")
        return 4

    running_file = cache / f"running-{hashlib.sha1(str(top).encode()).hexdigest()[:8]}.json"
    with open(cache / "launch.lock", "w") as lockf:
        fcntl.flock(lockf, fcntl.LOCK_EX)
        running = None
        with contextlib.suppress(OSError, ValueError):
            running = json.loads(running_file.read_text())
        if running and alive(running["pid"]) and running["key"] != key:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(running["pid"], signal.SIGTERM)
            print(f"checks.py: stopped the run for the previous tree {running['key'][:12]}; the tree has changed since.",
                  file=sys.stderr)
            running = None
        if not (running and alive(running["pid"]) and running["key"] == key):
            if rundir.exists():
                for f in rundir.iterdir():
                    f.unlink()
            proc = subprocess.Popen([sys.executable, __file__, "_run", str(config), key, str(top), ",".join(only)],
                                    cwd=top, start_new_session=True, stdin=subprocess.DEVNULL,
                                    stdout=subprocess.DEVNULL, stderr=open(cache / f"{key}.runner.log", "w"))
            write_json(running_file, {"key": key, "pid": proc.pid, "started": time.time()})
            running = {"key": key, "pid": proc.pid}

    deadline = time.time() + args.wait
    while time.time() < deadline:
        if result_file.exists():
            return report(rundir, json.loads(result_file.read_text()), cached=False)
        if (rundir / "invalid").exists():
            print("INVALID: the working tree changed while the checks ran (a check may have rewritten files; see "
                  "`git status`). Run the command again on the settled tree.")
            return 1
        if not alive(running["pid"]) and not result_file.exists() and not (rundir / "invalid").exists():
            print("ERROR: the check runner exited without a result (another run for a changed tree may have "
                  f"replaced it); see {cache / (key + '.runner.log')}")
            return 2
        time.sleep(2)
    progress(rundir)
    return 3


if __name__ == "__main__":
    sys.exit(main())
