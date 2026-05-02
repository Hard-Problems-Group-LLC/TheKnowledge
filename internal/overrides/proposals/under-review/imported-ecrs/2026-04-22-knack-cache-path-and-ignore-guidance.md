# Engineering Change Request: Safe Knack Cache Path And Ignore Guidance

## Summary

TheKnowledge should revise its knack-validation cache guidance and defaults so
consuming projects do not end up with a fake `.git/` directory when they are
not initialized Git repositories.

The current guidance says the default cache path is
`.git/knack-validation-cache.json` and that the cache path should be ignored
by Git. That is not enough for consuming projects that are not yet Git
repositories, are intentionally no-VCS repositories, or are preparing for a
future GitHub migration. In those cases the validator can create
`project_root/.git/knack-validation-cache.json` as ordinary project data,
which conflicts with Git's reserved metadata path.

The recommended non-Git fallback should be a dedicated project-local
`.cache/` directory that consuming projects can ignore wholesale.

## Incident

During an external project GitHub-preparation cleanup on 2026-04-22, the
operator asked whether `.git/knack-validation-cache.json` was already covered
by `.gitignore`.

Investigation found:

- the external project's root `.gitignore` did not ignore the cache path.
- The workspace contained a literal `.git/` directory, but it was not a Git
  repository metadata directory.
- The only file inside that directory was
  `.git/knack-validation-cache.json`.
- `git status` failed with `fatal: not a git repository`, proving the path was
  project data, not live Git control state.
- TheKnowledge's `validate_knacks.py` default cache path is
  `.git/knack-validation-cache.json`.
- The validator resolves `.git/...` through `git rev-parse --git-dir` only
  when Git reports a real Git directory. Otherwise it falls back to creating
  the configured path under the consuming project root.
- An external project adopted `.cache/knack-validation-cache.json` as the local
  safe cache path and ignores the entire `.cache/` directory.

The result was an avoidable migration hazard: a tool-created `.git/` directory
occupied a path that must later become real Git metadata.

## Current Guidance Gap

TheKnowledge already documents that the default cache should be ignored by
Git. However, that statement assumes the project is already a Git repository
or that writing inside `.git/` is always Git-private.

That assumption fails for consuming projects that are:

- not yet initialized as Git repositories;
- intentionally no-VCS but still using TheKnowledge validators;
- in the middle of preparing for a future GitHub migration;
- using separate Git directories or submodule worktrees; or
- using validation helpers before repository initialization.

In a real Git worktree, files under the actual Git directory are not ordinary
tracked project files, so `.gitignore` is not the primary protection. In a
non-Git consuming project, `.git/` is just another directory until Git is
initialized, so a validator must not create it as cache storage.

## Requested Change

Update TheKnowledge so cache guidance and implementation distinguish three
cases:

1. Real Git worktree.
   If `git rev-parse --git-dir` succeeds, Git-private caches may be placed
   under the resolved real Git directory.

2. Non-Git or no-VCS consuming project.
   If no real Git directory exists, validation helpers must not create
   `project_root/.git/`. They should use a project-visible, explicitly
   ignorable cache path under a project-local `.cache/` directory, such as
   `.cache/knack-validation-cache.json`.

3. Invalid or fake `.git/` path.
   If `project_root/.git` exists but `git rev-parse --git-dir` fails, helpers
   should treat the state as suspicious and avoid writing under that path.
   They may warn, fail with a clear message, or fall back to the documented
   non-Git cache path.

## Documentation Changes Requested

Update these TheKnowledge surfaces:

- `standards-and-practices/docs/specifications/knack_documents.txt`
  - Replace the unconditional `.git/knack-validation-cache.json` default with
    a Git-aware rule.
  - State that non-Git consuming projects must use a non-reserved cache path.
- `knacks/authoring-guide.md`
  - Explain where the cache lives in Git and non-Git projects.
- `templates/AGENTS-footer.md`
  - Avoid telling every consuming project that the validator uses a `.git/`
    cache path without qualification.
- `scripts/validate_knacks.py`
  - Prevent automatic creation of `project_root/.git/` when Git is not
    initialized.
  - Add a safe non-Git fallback cache path or require an explicit cache path.
- Starter `.gitignore` or managed ignore guidance
  - Include `.cache/` as the recommended project-local generated cache root.

## Requirements

- Do not create `.git/` as ordinary project data.
- Preserve correct behavior for real Git repositories, submodules, and
  separate-Git-dir worktrees.
- Keep lightweight knack validation cacheable.
- Make the cache path discoverable from `--help`.
- Make the recommended non-Git cache path easy to ignore before GitHub
  migration.
- Prefer a dedicated project-local `.cache/` directory that is entirely
  ignored by Git.
- Add tests for non-Git consuming projects, fake `.git/` directories, and
  separate-Git-dir repositories.

## Non-Goals

- Remove caching from knack validation.
- Mandate one specific project-visible cache directory for every consuming
  project if TheKnowledge can support `.cache/` as a documented default plus
  override.
- Redesign the unrelated quality-gate cache in this ECR, except to apply the
  same reserved-path principle if similar behavior exists there.
- Initialize Git in no-VCS consuming projects.

## Recommended Validation

- Run `validate_knacks.py` in a temporary project with no Git repository and
  confirm no `.git/` directory is created.
- Run the validator in a real Git repository and confirm Git-private cache
  behavior still works.
- Run the validator in a separate-Git-dir worktree and confirm the cache maps
  to the real Git directory when Git-private cache mode is selected.
- Run the validator in a project with a fake `.git/` directory and confirm it
  does not write additional files there.
- Confirm generated starter ignore guidance covers any adopted non-Git cache
  directory.
- Confirm a consuming project can ignore `.cache/` wholesale without losing
  source files, retained reports, or other operator-visible artifacts.

## External-Project Adoption Note

An external project adopted the local version on 2026-04-22 by moving the
existing `.git/knack-validation-cache.json` to
`.cache/knack-validation-cache.json`, removing the cache-bearing fake `.git/`
directory state, ignoring `.cache/` in the root `.gitignore`, and routing
local knack validation through a project-local validation helper. The current
Codex execution environment may still expose an empty read-only `.git`
mountpoint, but that mountpoint no longer contains project cache data.
