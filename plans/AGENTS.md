# Plans index

<!-- IMMUTABLE HEADER: do not edit the text above the BEGIN marker. -->

This folder holds the plans for agents. Humans read `docs/` instead.

- Copy [for-each-plan/](./for-each-plan/) to start a plan in `plans/<plan-name>/`.
- `goal.md` holds the goal and the Ralph loop prompt. `plan.md` holds the high-level plan. `spec.md` holds the requirements and protected checks. `steps/` holds one file for each step.
- A step is small. A small model or agent can implement, test and verify it alone.
- Run a plan in its own Git worktree and on its own branch.
- Steps that run at the same time must not touch the same files (see `touches` in the step front matter).
- A plan must survive a stop at any time. Another agent must be able to continue from the files in the repository. Record status and evidence in the step files.
- Runtime output goes outside the repository, in `~/repo-work/<repo>/<plan>/`. Never track it.
- Never put PII, secrets or personal paths in a plan.
- Write in Simplified Technical English (ASD-STE100).
- This file is generated. Run `python3 scripts/build_indexes.py` after any change. Do not edit the list below by hand.

Read the list. Open only the plans whose "Read me when" line matches your task.

See the [archive](./archive/) for historical material, including the [legacy template](./archive/legacy-template/).

<!-- BEGIN GENERATED INDEX -->

* [adopt-controls/plan.md](./adopt-controls/plan.md)
  Read me when: you adopt the pinned deterministic-controls library and the secret guard in gpx_parser, in advisory mode, with the existing Docker gate kept.
* [for-each-plan/plan.md](./for-each-plan/plan.md)
  Read me when: you want to see the format of a plan. (Template only. Copy this folder to start a plan.)
* [ralphify/plan.md](./ralphify/plan.md)
  Read me when: you are bringing this repository onto the template or reproducing its Docker test.

<!-- END GENERATED INDEX -->
