---
gist: "Read me when: you change, run or debug the pinned deterministic-controls checks, or the shim, the pin or the Docker cache for them."
---

# Controls adoption

This repository uses the pinned `deterministic-controls` library in advisory mode. The CI job `controls` is not a required check yet.

## How it works

- `scripts/check_context.py` is a shim. It runs the library with the `ci` profile. It keeps the old output lines (`ok  <script>` or `FAIL <script>`) and the exit codes `0` (pass) and `1` (a check fails).
- `scripts/controls-requirements.txt` holds the pin: one install line with a full commit.
- `controls.toml` lists the enabled checks.
- The shim runs the library from a cached virtual environment. The cache path is `$XDG_CACHE_HOME/deterministic-controls/<commit>/`. The default is `~/.cache/deterministic-controls/<commit>/`.
- The first run for a commit needs the network. The shim builds the cache then.
- If the library cannot run, the shim exits `2`. It never passes without a result. It never falls back to the old scripts.
- The old check scripts and `scripts/build_indexes.py` stay in the repository.

## How the adoption was made

1. Audit: `docs/controls-audit.json` (step `a01-audit`).
2. Plan: `adopt plan` with the pinned commit (a dry run).
3. Apply: `adopt apply` with the same commit, on a clean tree. Its output was committed on the step branch.

## Where the tools did not fit

- `adopt apply` rewrote `scripts/install_hooks.sh` (a `secretguard.path` fallback). That file is outside the scope of the step. It was restored to the previous version.
- `adopt apply` did not commit its output. The agent committed it.
- The Docker run has no network and a read-only root. The shim cannot build its cache there. The `Dockerfile` now builds the cache at image build time, as user `tester`, with the shim functions. The `Dockerfile` also installs `git` with `apt-get`. The shim needs `git` to install the pinned commit. `tests/test_secret_guard.py` also needs it. The `CMD`, `--network none` and `--read-only` did not change.
- `.dockerignore` is an allowlist. `adopt apply` did not add `controls.toml` to it. The image then lacked the manifest, and the shim failed with "manifest not found". The step now adds `!controls.toml`. The excludes for secrets did not change.
- Not verified: whether the shim writes outside `/tmp` at run time. The agent session cannot run Docker. The driver gate shows it.

## Secret guard exceptions

none
