# Agent contract

A small command-line summarizer for GPX route and track files; gpx_parser.py contains the complete implementation.

## Standing rules

- Before changing this repository's structure, read [repo-template](https://github.com/dullroar/repo-template) and [ralph-looper](https://github.com/dullroar/ralph-looper). Account for their layout, plan format, generated indexes, worktree rules, and validation commands in the change.
- Start work on a branch. Do not commit directly to the base branch, `master`.
- Write documents in Simplified Technical English. Use short sentences, active voice, and consistent terms.

## Load context in this order

1. Read this file.
2. Read the short indexes in full. Start with `README.md` and `docs/README.md`. Then read the indexes in `memory/AGENTS.md`, `plans/AGENTS.md`, and `scripts/AGENTS.md`.
3. Match the task to the **Read when**, **Read me when**, and **Run me when** entries. Open only the matching documents.
4. For a large file, search its headings and read only the relevant ranges.
5. Stop loading when the decision, intended files, constraints and validation method are known.

User instructions take precedence over repository guidance. When sources conflict, prefer: user
instruction, this file, `docs/design/`, the named plan, domain documentation and references,
`memory/`, implementation and tests, historical notes.

## Context ownership

- Universal rules belong here.
- Architectural reasons belong in `docs/design/` (one premise per file).
- Non-obvious findings that cost time to discover belong in `memory/` (one topic per file; edit the existing topic, do not append a rival).
- Execution state belongs in `plans/`; deterministic automation in `scripts/`.
- Every routed Markdown file starts with `gist` front matter that begins with `Read when:` or `Read me when:`.
- Give each script a `Run me when:` line in its first 25 lines. Run `python3 scripts/build_indexes.py` to regenerate indexes.
- Keep runtime output such as logs, usage records, and locks in the runner's work directory outside the repository.

Do not duplicate a fact across layers. Correct its canonical source.

## Planned work (spec-driven)

- Work only on a named plan in `plans/<plan>/` or an explicitly identified off-plan task. Copy [plans/for-each-plan/](plans/for-each-plan/) to start a plan. Keep the goal and loop prompt in `goal.md`, the approach in `plan.md`, the requirements in `spec.md`, and each step in `steps/`.
- Once its spec is approved, proceed through the steps without asking permission for routine work. Failed tests and dead ends inside scope: diagnose, repair, continue. Return to the user only for a new decision: contradictory requirements, scope expansion, or an action outside the spec's delegated authority.
- Acceptance checks named in the spec are protected. Never weaken, skip or delete one to get green; if one cannot pass as written, escalate.
- Run each plan and its steps in their assigned Git worktrees and branches. Parallel steps must have no dependency between them and no overlapping `touches`. If independence is uncertain, run the steps in sequence. After parallel steps merge, run the spec's combined validation.
- A step is done only with recorded evidence. Report unavailable verification and record unfinished work in the step's resume notes.
- Record rule retirements, documentation corrections, and tolerated violations as distinct outcomes. See the [spec template](plans/for-each-plan/spec.md).

## Validation

Run the smallest check that proves the change, then `python scripts/check_context.py` for any change to context files.

## Controls

Do not weaken the controls. You may run the local checks at any time. CI runs them in all cases. Do not change or disable the controls, the pin (`scripts/controls-requirements.txt`), `controls.toml` or the workflows to make an unrelated task pass. The driver checks the gate and `touches` of each step. A change to the gate or a file outside `touches` fails the step. Send each piece of work to the cheapest executor that can do it, and let the gate decide if the work is done. The full policy is at https://github.com/dullroar/ralph-looper/blob/main/docs/routing.md.

## Safety

Do not commit credentials, personal data, personal filesystem paths or sensitive record-level examples. Use placeholders and aggregate evidence. Do not push, publish, force-push or add a remote without authorization.
