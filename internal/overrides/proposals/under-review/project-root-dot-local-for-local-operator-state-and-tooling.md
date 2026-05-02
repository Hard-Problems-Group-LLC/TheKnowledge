# Project-Root `.local/` For Local Operator State And Tooling

Title: Project-Root `.local/` For Local Operator State And Tooling
Author: Codex
Date: 2026-04-25T10:21:12-07:00
Status: Under Review
Reviewers: operator, AI maintainers
Related Work: `install.sh`; `bootstrap.sh`; `scripts/initial-setup.py`;
`templates/README.md`; `templates/AGENTS-footer.md`;
`standards-and-practices/docs/installation.txt`;
`internal/overrides/proposals/under-review/`
`theknowledge-tool-runtime-isolation-and-bootstrap-reliability.md`

## Problem Statement
TheKnowledge needs a standard place for checkout-local mutable artifacts such
as tool runtimes, helper wrappers, scratch launchers, and other operator-only
state used while maintaining the repository directly. That state must stay out
of tracked files, stay out of shipped starter material, and avoid polluting a
consuming project's view of TheKnowledge when TheKnowledge is present as a
submodule.

Using `.git/` for such material is the wrong default. It is easy to forget,
harder to discover, and conflates operator-maintained tooling with Git's own
metadata. Some helper caches belong under `.git/`, but ad hoc virtual
environments and repo-local launch wrappers should not be treated as Git
internals.

Using tracked top-level paths is also wrong. That risks accidental commits,
template drift, and downstream confusion when consuming projects inspect or
vendor TheKnowledge.

## Goals
- Standardize one repo-local, untracked layout for mutable operator state used
  while maintaining TheKnowledge directly.
- Keep that state clearly outside tracked starter material and outside
  generated submodule payloads.
- Give maintainers an obvious place for local wrappers such as `.local/bin/`
  and local testing tool environments.
- Update initial setup and direct-checkout guidance so agents do not improvise
  ad hoc locations such as `.git/<tooling-name>/`.

## Non-Goals
- Check any local runtime, cache, or wrapper into version control.
- Force consuming projects to create or use TheKnowledge's own local operator
  state.
- Replace a consuming project's own `.venv`, `uv`, `poetry`, or other local
  runtime policy.
- Move Git's own internal caches out of `.git/` when they are intentionally
  tied to Git metadata.

## Proposed Guidance
TheKnowledge should reserve a top-level ignored `.local/` directory for
checkout-local operator state. Initial setup guidance should describe it as
the default home for local mutable artifacts that are:

- specific to one checkout;
- not part of shipped project behavior;
- not intended for starter templates; and
- not safe or useful to track in Git.

The standard initial subtree should include:

- `.local/bin/` for local helper wrappers, launch shims, and convenience
  entrypoints;
- `.local/share/` or another documented sibling for local data when needed;
  and
- named tool-runtime directories such as
  `.local/theknowledge-tool-runtime/` when a direct-checkout maintenance
  environment is required.

Guidance should explicitly say:

1. Prefer `.local/` over ad hoc top-level directories.
2. Prefer `.local/` over `.git/` for operator-managed runtimes, wrappers, and
   mutable helper state.
3. Keep `.local/` ignored by Git in TheKnowledge itself and in generated
   starter material when appropriate.
4. Do not assume `.local/` exists in a consuming project unless that project
   creates it deliberately.
5. Do not put source-of-truth project configuration in `.local/`.

## Why This Helps

### Clearer Boundaries
`.local/` reads as local mutable state owned by the checkout operator. That is
easier to understand than burying a virtual environment inside `.git/`, where
it looks like a Git implementation detail rather than a local maintenance
tool.

### Better Submodule Hygiene
When TheKnowledge is a submodule, ignored local state inside a standard
`.local/` path is easier to reason about than mixed-purpose hidden paths or
tool-specific one-offs. The intent is obvious: local-only, untracked, not part
of the shared payload.

### Better Guidance For AI Agents
Agents should not have to invent where local wrappers and test runtimes go.
If the initial setup guidance names `.local/` and `.local/bin/` explicitly,
future sessions can follow that rule instead of improvising new locations.

## Requested Changes
- Update TheKnowledge direct-checkout and installation guidance to name
  project-root `.local/` as the standard home for checkout-local operator
  state.
- Update initial setup guidance so starter material explains the difference
  between tracked project files, Git metadata, and ignored local state.
- Add `.local/` to TheKnowledge's own `.gitignore`.
- Update any runtime-isolation follow-up implementation to use `.local/`
  rather than `.git/` for direct-checkout local tool environments unless a
  narrower Git-metadata cache is genuinely required.

## Validation
- Confirm a direct TheKnowledge checkout can create and use
  `.local/theknowledge-tool-runtime/` without introducing tracked changes.
- Confirm local wrappers under `.local/bin/` remain ignored.
- Confirm starter guidance does not tell consuming projects that `.local/`
  content is part of the tracked repository payload.
- Confirm TheKnowledge-authored docs stop recommending `.git/` as the default
  home for repo-local operator runtimes.

## Alternatives Considered
1. Keep using `.git/` for local runtimes.
   Rejected because it hides operator state inside Git metadata and makes the
   intent less clear.
2. Keep using ad hoc ignored top-level paths per tool.
   Rejected because it encourages path sprawl and undocumented conventions.
3. Use only repo-local `.venv`.
   Rejected because `.venv` is one runtime convention, not a general home for
   wrappers and other checkout-local operator artifacts.

## Decision Log
- 2026-04-25T10:21:12-07:00 - Drafted after a direct-checkout maintenance
  session created a local TheKnowledge tool runtime under `.git/` and the
  operator requested that such state live under project-root `.local/`
  instead.
