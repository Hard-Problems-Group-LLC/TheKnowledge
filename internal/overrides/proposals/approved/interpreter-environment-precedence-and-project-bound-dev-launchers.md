# Engineering Change Request: Interpreter Environment Precedence and Project-Bound Developer Launchers

Title: Engineering Change Request: Interpreter Environment Precedence and
Project-Bound Developer Launchers
Author: Codex
Date: 2026-03-31T20:40:57-07:00
Status: Approved
Reviewers: operator, AI maintainers
Related Work: `standards-and-practices/docs/`
`Interpreters-and-Package-Management-Environments.md`;
converged managed bootstrap starter on 2026-03-31

## Problem Statement
The new interpreter/package environment standard defines a four-layer
precedence model:

1. system-wide
2. user-local
3. user-selected profile
4. project-specific override

The current managed Python bootstrap mostly satisfies that model for directory
entry through `pyenv`, `.python-version`, repo-local `.venv`, and `direnv`,
but it does not yet state clearly how a development install should keep the
project-specific override active when the project command is launched outside
the repository directory. It also does not yet push repositories toward
reusing a sensible shared user-scoped interpreter family for normal
per-user installs.

## Goals
- Make the environment-precedence standard concrete enough that consuming
  projects can implement it incrementally.
- Establish project-bound developer launchers as the Python-side mechanism for
  keeping the project override active outside the repository directory.
- Encourage normal per-user installers to reuse an already-available managed
  user-scoped interpreter family when practical.
- Keep the managed starter generic by using optional project install hooks
  rather than forcing one launcher policy on every repository.

## Non-Goals
- Full multi-language bootstrap implementation in the same change.
- Making TheKnowledge itself ship a one-size-fits-all project launcher
  template for every consuming repository.
- Replacing repo-local `.venv` with named `pyenv-virtualenv` environments.

## Proposed Approach
Document the broader environment-precedence policy in a new repository-level
doc and explicitly connect the existing Python bootstrap spec to it.

Clarify in the Python bootstrap spec and installation guidance that
repositories may use `scripts/install_project.py` to install or remove a
project-bound developer launcher in development mode. That hook is the
intended place to enforce the highest-precedence project override outside the
repository directory without hard-coding one launcher contract into the
managed starter.

Recommend that normal per-user installers prefer an already-installed
user-scoped managed runtime, such as the relevant `pyenv` selection, before
falling back to whatever system interpreter happens to be current.

## Adoption and Rollout
Implement the first repository-side example in `codex-wrangler` itself by:

- adding a repo-specific install hook that publishes or removes a
  project-bound developer launcher; and
- teaching the stable user installer to reuse the managed pyenv runtime when
  available.

Use that repo as the proving ground before deciding whether TheKnowledge
should later ship more reusable helper code for project-bound launchers.

## Decision Log
- 2026-03-31T20:40:57-07:00 - Approved after the operator requested that the
  new environment standard be turned into an implementation proposal and that
  work begin immediately.
