# TheKnowledge

A reusable knowledge base for software project operations, engineering
standards, and AI/human collaboration practices.

## Purpose

`TheKnowledge` captures the process backbone that remains useful across
radically different projects: web apps, desktop tools, data systems, CLI
utilities, and more. It is intentionally separate from any single product's
business logic.

## Long-term objective

This repository is intended to become a shared reference and eventually a Git
submodule that other projects can import. The goal is consistent execution:
- technical standards and operating practices,
- project management standards and operating practices,
- cross-platform validation strategies,
- reproducible quality gates and safety checks.

## Scope

This repository includes:
- `knacks/`: reusable knack documents: focused `.knack.md` knowledge units
  that may build on one another.
- `standards-and-practices/`: reusable workflows, standards, security
  practices, runbooks, and dev utilities.
- `templates/`: starter material meant to be copied into consuming projects.
- `scripts/`: reusable tooling plus setup helpers for submodule consumers.
- `internal/`: repository-local state for maintaining TheKnowledge itself.
  TheKnowledge's live project-management state lives under
  `internal/overrides/`; the starter material under
  `templates/project-management/` stays pristine unless the reusable framework
  itself is being revised.

This repository does **not** include product-specific source code or
application business logic.

## Intended use

1. Import this repository (or a subtree thereof) into active projects.
2. Run `scripts/initial-setup.py` from the submodule to install starter files
   from `templates/` into the consuming project root.
3. Use the starter `scripts/dev_setup.py` when you want the default pinned
   Black, Ruff, and pytest toolchain in the consuming project.
4. Let the installed `tool_execution_constraints.json` record managed
   environment-specific tool execution constraints for shared helpers.
5. Keep project state in the consuming project's own directories rather than
   inside the submodule.
6. Add language/technology SOPs under
   `standards-and-practices/docs/sop/` as needed.
7. Add focused knack documents under `knacks/` when a reusable body of
   know-how deserves a dedicated `.knack.md` file.

## Using as a submodule

For an existing Git repository, add TheKnowledge at the path you want the
team to keep stable:

```bash
git submodule add https://github.com/Hard-Problems-Group-LLC/TheKnowledge.git \
  TheKnowledge
git submodule update --init --recursive
python TheKnowledge/scripts/initial-setup.py \
  --project-root . \
  --knowledge-root TheKnowledge
```

For new or lightly customized consuming projects, then run:

```bash
python scripts/dev_setup.py
```

The starter installs `requirements-dev.txt`, `scripts/dev_setup.py`, and
`tool_execution_constraints.json`. Together they provide TheKnowledge's
default pinned Black, Ruff, and pytest toolchain plus a managed registry for
known environment-specific tool execution constraints. Projects with tighter
local environment policy may replace or extend those files instead of using
the starter unchanged.

For a brand-new repository, initialize the repo first and then add the
submodule:

```bash
mkdir TestProject
cd TestProject
git init -b trunk
git submodule add https://github.com/Hard-Problems-Group-LLC/TheKnowledge.git \
  TheKnowledge
git submodule update --init --recursive
python TheKnowledge/scripts/initial-setup.py \
  --project-root . \
  --knowledge-root TheKnowledge
```

Then optionally install the default pinned Python developer toolchain:

```bash
python scripts/dev_setup.py
```

After that setup, commit both the new `.gitmodules` file and the generated
project-management files, `AGENTS.md`, and any adopted starter setup files in
the consuming project.

When another developer clones the consuming project later, they should either
clone with submodules enabled:

```bash
git clone --recurse-submodules <project-url>
```

or initialize them after clone:

```bash
git submodule update --init --recursive
```

## Updating a submodule copy

When a consuming project wants newer TheKnowledge changes, first review the
incoming upstream delta in the submodule checkout, then adopt that reviewed
version and reconcile any managed-file drift before staging the result:

```bash
python TheKnowledge/scripts/update_theknowledge_submodule.py \
  --project-root . \
  --knowledge-root TheKnowledge
```

That helper prints the incoming commit summary and diffstat, advances the
active submodule checkout to the reviewed upstream `trunk` commit, runs the
managed drift report, refreshes the managed starter files when drift is
detected, and leaves a clean reviewable diff in the parent project.

If you need or prefer the fully manual path, the equivalent core steps are:

```bash
(cd TheKnowledge && git fetch origin trunk)
(cd TheKnowledge && git log --oneline HEAD..origin/trunk)
(cd TheKnowledge && git diff --stat HEAD..origin/trunk)
(cd TheKnowledge && git checkout --detach origin/trunk)
python TheKnowledge/scripts/report_managed_agents_drift.py \
  --project-root . \
  --knowledge-root TheKnowledge
python TheKnowledge/scripts/initial-setup.py \
  --project-root . \
  --knowledge-root TheKnowledge \
  --force \
  --template requirements-dev.txt \
  --template scripts \
  --template tool_execution_constraints.json
git diff
```

A brief summary review is enough for routine upgrades so long as the incoming
change set is not being adopted blindly. That flow keeps the submodule
pointer update, any managed `AGENTS.md` changes, and any related project
adjustments visible in one reviewable diff. Commit and push the updated
submodule pointer plus the resulting project-file changes together when they
belong to the same upgrade so the reviewed version becomes the project's new
shared baseline.

If the upgrade also changes the starter `requirements-dev.txt` or
`scripts/dev_setup.py`, rerun `python scripts/dev_setup.py` in the consuming
project before the next validation pass, unless the project intentionally uses
its own bootstrap flow instead. When the upgrade changes
`tool_execution_constraints.json`, review that policy diff alongside the
submodule update so the project's shared helpers stay aligned with the new
constraints.

## Review-first staging

Projects that use TheKnowledge should treat review as part of staging, not
just of committing. Before any `git add`, list the files about to be staged
and ask whether to review them. Offer `1` review at least one file,
`2` proceed without review for this changeset, and `3` proceed and suppress
review prompts for the rest of the current session until resumed.

If review is requested, prefer reviewing the changeset in Meld when
available. That is the default recommended visual review path for
TheKnowledge because the folder comparison stays open in one tab while
file comparisons open in additional tabs. Install Meld from the
official project page: https://gnome.pages.gitlab.gnome.org/meld/

If Meld is unavailable, either review files one by one in the
surrounding conversation or abort the staging step. Run `git diff`
before any `git add` and `git diff --cached` before any commit. The
standardized helper
`python TheKnowledge/scripts/git_standard_commit_push.py -m "<subject>"`
supports this flow; use `--assume-reviewed` only after an explicit review
decision, and `--resume-review-prompts` to re-enable prompts for the current
shell session.

## Timestamped Intermediary Updates

TheKnowledge recommends inline timestamp prefixes for substantive
AI-driven development updates in both direct-checkout maintenance
sessions and consuming projects. Use a bracketed ISO 8601 format
such as `[2026-03-25T01:05:12-07:00] Running full pytest.` at the
start of intermediary updates when work begins, before and after
long-running commands or waits, and at major phase boundaries. Add
elapsed durations when they are easy to compute.

This keeps workflow profiling visible in the shared conversation
itself, so teams can identify slow command startup, long
validation, GUI review pauses, and approval waits without scraping
hidden logs. Final answers and casual chat do not need timestamp
prefixes in every sentence.

## Submodule layout

The consuming project chooses the submodule path at `git submodule add` time.
For example:

```text
TestProject/
  TheKnowledge/
    knacks/
    standards-and-practices/
    templates/
    scripts/
```

After running the template installer, the consuming project keeps its own
stateful files outside the submodule:

```text
TestProject/
  TheKnowledge/
  knacks/
  project-management/
    backlog.txt
    tasks-in-progress.txt
    completed-tasks.txt
    deferred.txt
    ai-human-requests.txt
    proposals/
      approved/
      rejected/
      deferred/
      under-review/
    state/
      pending-commit-changes.txt
    bugs/
      open/
      in-progress/
      closed/
```

That top-level `knacks/` directory is where consuming projects can keep
proprietary or third-party knacks beside the stock knacks that ship inside the
TheKnowledge subtree. When a project-local knack path collides with a stock
TheKnowledge knack path, tooling should warn and evaluate both.

## Feedback Branch

When TheKnowledge is being maintained directly as its own checkout, keep
using the normal `trunk` workflow and the usual internal trees such as
`internal/overrides/`, bug tracking, and proposal records. Do not route
ordinary TheKnowledge maintenance through `Feedback`.

The `Feedback` branch exists for a different situation: a team is working
primarily inside some other project that uses TheKnowledge and wants to
check bugs, proposals, general notes, or complaints about TheKnowledge
back into the TheKnowledge checkout without interrupting the consuming
project's main work.

When that happens, use the active `TheKnowledge/` submodule checkout inside
the consuming project. Prefer the helper workflow:

```bash
python TheKnowledge/scripts/send_theknowledge_feedback.py prepare \
  --project-root . \
  --knowledge-root TheKnowledge
```

Then record the Feedback item in the active `TheKnowledge/` checkout and
finish with either a local-only commit:

```bash
python TheKnowledge/scripts/send_theknowledge_feedback.py finish \
  --project-root . \
  --knowledge-root TheKnowledge \
  --message "Record TheKnowledge feedback"
```

or a commit plus push when the configured remote push URL is writable for the
current operator:

```bash
python TheKnowledge/scripts/send_theknowledge_feedback.py finish \
  --project-root . \
  --knowledge-root TheKnowledge \
  --message "Record TheKnowledge feedback" \
  --push
```

Use `abort` instead of `finish` when you want the helper to restore the
previous submodule state without keeping the Feedback session open.

While maintaining TheKnowledge itself, periodically inspect `Feedback`.
Items there should either become evaluation tasks backlogged on `trunk`,
remain in `Feedback` with additional discussion, or be dropped from
`Feedback` by collaborative human-and-AI agreement. Evaluation work that
starts from `Feedback` should result in recommendations on `trunk`; if the
recommendation is approved, the resulting fix should be backlogged or the
proposal should be merged on `trunk`, and the originating `Feedback` item
should then be removed or updated accordingly.
