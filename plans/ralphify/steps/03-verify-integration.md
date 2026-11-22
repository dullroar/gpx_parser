---
id: 03-verify-integration
status: pending
depends_on: [02-build-and-test]
touches:
  - plans/ralphify/steps/03-verify-integration.md
lane: none
requirements: [R3]
gate: python3 scripts/check_context.py && bash scripts/test_docker.sh && git diff --check
evidence: ""
---

# 03-verify-integration

Depends on `02-build-and-test`. Update only the step file. Rerun the context and Docker gate from the integrated worktree as the driver would. Check the template and runner links in `AGENTS.md` and the structural-change rule. Verify README commands and the existing entry points. Record the worktree base commit, exact commands, build result, test counts or concrete smoke assertions, expected opt-in skips, real FUSE result where required, and UTC date. Keep logs outside Git. Gate: `python3 scripts/check_context.py && bash scripts/test_docker.sh && git diff --check`.

The driver writes its own `evidence` field. Put detailed test evidence in the body of the verification step and commit it. The parent verifies the final child commit and result. A green build alone cannot satisfy R2 or R3.

## Repository gate

Keep the stdlib-only package footprint and single-file CLI. Add an isolated CLI test under `tests/` using synthetic GPX. Exercise explicit-file and directory input. Assert CSV columns, rows, and representative distance or elevation values. Use a temporary working directory because the CLI writes `gpx_summary.csv` to the current directory. Preserve the existing sample output.

Run `git merge-base HEAD plan/ralphify` to identify the integrated base commit. Replace each pending value in the results below. For each passing check, put details after `PASS`. Include the actual Docker commands or image reference and test counts or concrete smoke results. Record `n/a` in the FUSE field for other repos. If a required test fails or skips, record that in resume notes and leave the result pending.

## Results

- Base commit: `5116c07ae7f884ff0d4a4461a4b5df7dd79137dd` from `git merge-base HEAD plan/ralphify`.
- Commands: PASS `python3 scripts/check_context.py && bash scripts/test_docker.sh && git diff --check` with access to the local Docker socket. The context check passed on the host and in the container.
- Docker build: PASS `docker build --tag gpx-parser-test:a9ngUAVv5y .` from the worktree. The test script built the image from `python:3.12-slim-bookworm` and ran it as `tester` with `--network none`, a read-only root filesystem, and writable `/tmp`.
- Tests: PASS 2 of 2 in Docker and 2 of 2 on the host. Explicit-file input gave one route row. Directory input gave two rows for the route and track, ignored a text file, and accepted an uppercase `.GPX` extension. Both tests checked the CSV columns and the full expected rows, including distance and elevation values.
- Skips: None expected. None observed.
- FUSE: n/a.
- UTC date: 2026-11-22.

## Links and entry points

- Both upstream links in `AGENTS.md` match the origins of the local reference checkouts. The structural-change rule requires reading both projects and accounting for their layout, plan format, generated indexes, worktree rules, and validation commands.
- The README build command uses the same Dockerfile and build context as the gate, with a different image tag. The documented Docker test command passed. The host command `python3 -m unittest discover -s tests -v` also passed.
- The local Ralph Looper source accepts `--repo`, `--plan`, and `--agent codex` as documented in the README. The current step ran under the driver.
- `gpx_parser.py` and `gpx_summary.csv` match `master`. The CLI remains a single Python file with no third-party dependencies.
