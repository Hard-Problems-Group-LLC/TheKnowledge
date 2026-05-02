# TheKnowledge ECR: Python Bootstrap and Context Strategy

## Purpose

This document is an engineering change request for another Codex instance
working inside a writable checkout of `TheKnowledge`.

The goal is to turn the Python bootstrap and context-selection approach used
in an external project into the new normal guidance and starter behavior for
TheKnowledge.

## Problem Statement

TheKnowledge currently has a real mismatch between:

- a bootstrap path that is still expected to be friendly to Python `3.9`
- a starter validation and tooling stack that now wants a modern Python such
  as `3.12`

That mismatch is already reflected in TheKnowledge's own maintenance notes.
The practical result is that consuming projects can inherit starter scripts
and pinned tools that do not bootstrap cleanly under the repository's stated
floor.

## Desired Direction

Adopt this split as the new normal:

- bootstrap and setup scripts should run on Python `3.9`
- runtime and heavier tooling should run on Python `3.12`
- `pyenv`, `virtualenv`, and `pyenv-virtualenv` should be the standard
  mechanism for reaching that split
- a repo-local JSON file should be the source of truth for the target Python
  versions and the named pyenv environments
- `.python-version` should default the repository to the runtime environment
  when pyenv shell integration is active
- explicit context scripts should exist for both bootstrap and runtime

## External-Project Reference Implementation

The consuming-project reference implementation now lives in an external project and
can be used as a concrete model:

- `python-environments.json`
- `.python-version`
- `bootstrap.sh`
- `bootstrap-stage2.py`
- `set-context-bootstrap.sh`
- `set-context.sh`
- `scripts/install_prerequisites.sh`
- `scripts/prereq_python.sh`
- `scripts/runtime_python.sh`
- `docs/python-environment-strategy.md`

The key behavior in that implementation is:

- `bootstrap.sh` only assumes Python `3.9` or better and hands off to a stage
  two Python script
- `bootstrap-stage2.py` reads the JSON config, ensures `pyenv` and
  `pyenv-virtualenv` are present, creates the named environments, installs
  runtime tooling, writes `.python-version`, and updates shell startup files
  when appropriate
- `set-context-bootstrap.sh` and `set-context.sh` are intended to be sourced
  and switch between the bootstrap and runtime contexts
- the old `scripts/` entrypoints remain available as compatibility wrappers
  for the starter layout

## What I Want Changed In TheKnowledge

TheKnowledge should be revised so that its reusable starter guidance,
bootstrap scripts, and template files align with this split model.

The work should cover both:

- TheKnowledge's own direct-checkout maintenance workflow
- the starter material that consuming projects inherit from `templates/`

## Required Outcomes

### 1. Establish a canonical Python-version config record

Add a checked-in JSON file that defines:

- bootstrap required major/minor version
- bootstrap base version
- bootstrap pyenv environment name
- runtime required major/minor version
- runtime base version
- runtime pyenv environment name

Do not leave the version split scattered across multiple scripts as magic
literals.

### 2. Replace the old single-stage bootstrap story

Introduce a top-level bootstrap story equivalent in spirit to:

- `bootstrap.sh`
- `bootstrap-stage2.py`

The bootstrap shell entrypoint should:

- require only Python `3.9` or better to get started
- install or locate a suitable Python when feasible
- defer the bulk of the work to a Python stage-two script

The stage-two Python entrypoint should:

- read the JSON config
- ensure `pyenv` and `pyenv-virtualenv` are available
- ensure the configured base versions exist
- create the configured bootstrap and runtime envs
- install runtime packages into the runtime environment
- write `.python-version` for runtime-default behavior

### 3. Add explicit context-selection commands

Add shell scripts equivalent in spirit to:

- `set-context-bootstrap.sh`
- `set-context.sh`

These should be designed to be sourced by users who need to force one context
or the other.

Expected behavior:

- bootstrap context selects the bootstrap env
- runtime context selects the runtime env
- default repo behavior should still prefer the runtime env through
  `.python-version`

### 4. Preserve compatibility where practical

The existing TheKnowledge starter layout currently expects things like:

- `scripts/install_prerequisites.sh`
- `scripts/dev_setup.py`

Those entrypoints should either remain valid or be replaced with clear,
minimal compatibility wrappers that delegate to the new canonical bootstrap
path.

The goal is not to break every downstream instruction at once.

### 5. Update TheKnowledge guidance and templates

Revise the documentation so the new split is explained clearly and
consistently.

At minimum, update:

- `README.md`
- relevant `AGENTS.md` language if needed
- bootstrap/setup docs
- starter template docs under `templates/`
- any SOPs or validation docs that currently imply a single interpreter path

The guidance should make these points explicit:

- Python `3.9` remains the bootstrap/setup floor
- Python `3.12` is the preferred runtime/tooling target
- `pyenv` plus `pyenv-virtualenv` is the preferred bridge between those
  realities
- `.python-version` should default a repository to runtime context
- bootstrap and runtime context scripts should be used deliberately

### 6. Reconcile testing and validation helpers with the split

Inspect the current helper scripts and testing guidance so they stop assuming
one interpreter context for all purposes.

Examples of areas to inspect:

- prerequisite installers
- quality-gate wrappers
- validation instructions
- starter bootstrap docs
- any commands that assume `.venv`

The goal is not necessarily to rewrite every helper immediately, but the
documented happy path must stop fighting the new model.

## Acceptance Criteria

The change should not be considered done unless all of the following are
true inside the writable TheKnowledge checkout:

1. A checked-in JSON file defines the bootstrap/runtime versions and env
   names.
2. There is a top-level bootstrap flow that works from Python `3.9` or
   better.
3. There are explicit bootstrap/runtime context scripts.
4. `.python-version` defaults the repo to the runtime env.
5. Existing starter entrypoints still work or delegate cleanly.
6. TheKnowledge's docs explain the split clearly.
7. Consuming-project starter guidance points to the new model rather than the
   old `.venv`-centric story.
8. The resulting local verification demonstrates:
   - bootstrap context resolves to Python `3.9.x`
   - runtime context resolves to Python `3.12.x`
   - runtime validation tools install and execute in the runtime env

## Suggested Work Plan For The Other Codex Instance

1. Read the current TheKnowledge notes about the Python bootstrap mismatch.
2. Inspect the current starter scripts and template docs.
3. Implement the JSON-configured bootstrap/context structure.
4. Add compatibility wrappers instead of breaking old entrypoints outright.
5. Update docs and starter guidance.
6. Run the local bootstrap and verify both contexts.
7. Record the change in TheKnowledge's own project-management files.

## Important Constraints

- Preserve TheKnowledge's existing project-management and workflow discipline.
- Avoid forcing consuming projects to understand a large migration all at
  once.
- Prefer clear migration wrappers over abrupt deletion of well-known starter
  entrypoints.
- Keep the documented bootstrap path practical on machines that only have
  Python `3.9` available at first.

## Recommended Prompt For The Other Codex Instance

Use the following as the starting task text in the writable TheKnowledge
checkout:

```text
Adopt the external project-style Python bootstrap split as the new normal for
TheKnowledge.

Implement a JSON-driven Python version/env config, a top-level bootstrap.sh
that only requires Python 3.9 or better to get started, a bootstrap-stage2.py
that creates pyenv/pyenv-virtualenv environments for bootstrap and runtime,
explicit set-context-bootstrap.sh and set-context.sh scripts, runtime-default
selection via .python-version, and compatibility wrappers for existing
starter entrypoints where practical.

Update TheKnowledge's starter docs and guidance so Python 3.9 is the
bootstrap/setup floor, Python 3.12 is the runtime/tooling target, and pyenv +
pyenv-virtualenv is the standard bridge between them.

Use the external project's implementation as a reference model, but adapt it cleanly to
TheKnowledge's structure rather than copying blindly.
```
