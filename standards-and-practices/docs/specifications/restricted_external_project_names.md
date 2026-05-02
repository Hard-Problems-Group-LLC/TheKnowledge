# Restricted External-Project Names

## Purpose
Prevent TheKnowledge from naming external client projects that include it as a
submodule, dependency, or standards source.

## Requirements
- TheKnowledge-authored records, proposals, bugs, standards, templates,
  scripts, tests, and generated guidance must not name external client
  projects unless an operator explicitly approves a narrow exception.
- Use `an external project` or another operator-approved generic phrase when
  a client-project name would otherwise appear in prose, code comments, test
  data, or diagnostics.
- Keep the restricted-name list local and untracked. The default checkout
  location is `.theknowledge-restricted-names.local`; an out-of-tree local
  path is also acceptable when an operator configures it deliberately.
- Validation and review scans must skip the restricted-name list itself and
  other explicitly local policy-input files.
- A restricted name in a path component is a hard error. Agents and tooling
  must stop and ask the operator how to resolve the path before renaming,
  deleting, redacting, or moving anything.
- Non-path references should be redacted to the approved generic phrase once
  the path scan is clear or the operator has resolved any path-component
  blocker.
- Imported ECR holding directories must use project-neutral names such as
  `imported-ecrs/`, not source-project names.
- Imported ECR basenames should remain unchanged as source-facing identifiers.
  Record accepted or implemented imported ECR filenames in
  `internal/overrides/proposals/accepted-ecrs-list.md`.
- Filename collisions between imported ECRs should be rare. When one occurs,
  tooling and agents must stop and ask the operator how to disambiguate
  before overwriting, renaming, merging, or dropping either file.

## Non-Goals
- Storing client-project names in tracked TheKnowledge configuration.
- Guessing restricted names from repository history, remotes, hostnames, or
  adjacent project directories.
- Automatically rewriting path names that may affect history, provenance, or
  imported handoff material.
- Storing source-project provenance in tracked directory names.

## Review Checklist
- Check the local restricted-name list before broad edits, validation, or
  staging.
- Confirm no restricted names appear in tracked content outside approved
  exceptions.
- Confirm no restricted names appear in path components. If one appears, stop
  and ask for operator resolution.
