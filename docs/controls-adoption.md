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

## Probes

Run date (UTC): 2026-11-24. Each probe ran in its own clone under `.probe/`. The command was `python3 -m deterministic_controls check --root <copy> --profile ci --format json`. The tracked tree was not changed. The clones were deleted before the gate.

| Probe | Expected rule ID | Exit code | Result |
| --- | --- | --- | --- |
| Clean clone of `HEAD` | none | 0 | Pass. All seven checks passed. |
| Broken relative link in a Markdown file | `markdown.local-links` | 1 | Fail with `markdown.local-links.missing-file`. |
| Stale generated index (a script `Run me when:` line changed, index not rebuilt) | `context.index-freshness` | 1 | Fail with `context.index-freshness.stale`. |
| Plan step without `gate` | `plans.schema` | 1 | Fail with `plans.schema.missing-gate`. |
| Synthetic token in a committed Markdown file (built at run time in the shell) | `security.secrets` | 1 | Fail with `security.secrets.github-token`. `security.personal-data` also failed with `security.personal-data.token`. |
| Tracked `driver.out` file | `repo.forbidden-artifacts` | 1 | Fail with `repo.forbidden-artifacts.tracked`. |
| Internal error: an unreadable Markdown file | none (must not pass) | 3 | Not a pass. `markdown.local-links` and `security.personal-data` reported `error` with a permission error. The overall status was `error`. |

After each probe, the copy was restored. The restored copies for the plan step, the index and the unreadable file passed with exit `0`. The probes with an added file (link, token, artifact) use the file removal as the restore. The clean clone of `HEAD` is the reference for that state and passed with exit `0`.

The shim `python3 scripts/check_context.py` ran in the copy with the plan step that has no `gate`. Its exit code was `1`. It printed `FAIL check_plan.py` and kept the old output lines.

## Rollback

Run date (UTC): 2026-11-24.

Test result:

- The base commit is the parent of the `adopt apply` commit. In a clone, the old `python3 scripts/check_context.py` ran on that commit on a clean tree. It passed (exit `0`).
- The new shim ran in a clean clone of `HEAD`. It passed (exit `0`).
- Both pass. The old scripts are still in the repository, so the old check also works at `HEAD`.

Steps to roll back:

1. Option A, change the pin. Edit `scripts/controls-requirements.txt` and put another commit in the install line. Run `python3 scripts/check_context.py` once. It builds the new cache.
2. Option B, remove the adoption. Create a new branch. Run `git revert` on the adoption commits (the `adopt apply` commit, the docs commit and the `.dockerignore` commit of step `a02-apply`). Resolve conflicts if there are any. Do not use a force push.
3. Run `python3 scripts/check_context.py`. It must pass.
4. Run `bash scripts/test_docker.sh`. It must pass.

Files of the adoption:

- Added: `controls.toml`, `scripts/controls-requirements.txt`, `docs/controls-adoption.md`, `docs/controls-audit.json`.
- Changed: `scripts/check_context.py` (now a shim), `.github/workflows/context.yml` (new `controls` job), `Dockerfile` (cache build and `git`), `.dockerignore` (`!controls.toml`).
- Kept without change: `scripts/build_indexes.py`, `scripts/check_plan.py`, `scripts/check_links.py`, `scripts/scan_secrets.py`, `scripts/ctx_common.py`, `scripts/test_docker.sh`, the `check` CI job and the Docker `CMD`.

The cache under `$XDG_CACHE_HOME/deterministic-controls/<commit>/` is safe to delete. The shim builds it again on the next run (it needs the network).

## Receipt

Run date (UTC): 2026-11-24. The command was `python3 -m deterministic_controls adopt receipt --root <clean clone> --commit 3a2e9f3d95136958c54f73c831e84b971fc9a054`. It ran in a clean clone of `HEAD`.

- `repository` is the name of the temporary clone, not the name of this repository.
- `files_added` and `files_changed` are empty in a clean clone. This is a known defect of the library. The list of files is in the Rollback section.
- `enforcement_state` is `advisory`.
- The `rollback` text in the receipt names the base revision of the clone. It is not the pre-adoption commit. Use the Rollback section above.

```json
{
  "base_revision": "5819f4b9091b30744ee178858c4c08dda87f0484",
  "checks_run": [
    {"check_id": "context.index-freshness", "status": "passed"},
    {"check_id": "markdown.local-links", "status": "passed"},
    {"check_id": "plans.graph", "status": "passed"},
    {"check_id": "plans.schema", "status": "passed"},
    {"check_id": "repo.forbidden-artifacts", "status": "passed"},
    {"check_id": "security.personal-data", "status": "passed"},
    {"check_id": "security.secrets", "status": "passed"}
  ],
  "commands_kept": [
    "scripts/build_context_indexes.py",
    "scripts/build_indexes.py",
    "scripts/check_links.py",
    "scripts/check_plan.py",
    "scripts/ctx_common.py",
    "scripts/scan_context_secrets.py",
    "scripts/scan_secrets.py",
    "scripts/test_docker.sh",
    "test: python3 -m unittest discover -s tests",
    "test: docker build (Dockerfile)",
    "ci-job: check"
  ],
  "control_pin": "3a2e9f3d95136958c54f73c831e84b971fc9a054",
  "date": "2026-11-24",
  "enabled_checks": [
    "context.index-freshness",
    "markdown.local-links",
    "plans.graph",
    "plans.schema",
    "repo.forbidden-artifacts",
    "security.personal-data",
    "security.secrets"
  ],
  "enforcement_state": "advisory",
  "files_added": [],
  "files_changed": [],
  "profile": "ci",
  "repository": "head",
  "schema_version": 1
}
```

The block omits the `rollback` key of the receipt. The text above replaces it.

## Secret guard exceptions

none
