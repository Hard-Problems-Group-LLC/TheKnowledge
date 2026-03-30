# TheKnowledge ECR: Standardize `ECRs/TheKnowledge/` For Read-Only Upstream Feedback

## Purpose

This document is an engineering change request for another Codex instance
working inside a writable checkout of `TheKnowledge`.

The goal is to make `ECRs/TheKnowledge/` a standard consuming-project
directory pattern for change requests aimed at TheKnowledge when the
consuming project has only read-only access to the TheKnowledge checkout or
submodule it is using locally.

## Problem Statement

Consuming projects regularly discover gaps, bugs, missing guidance, or
desirable upstream improvements in TheKnowledge while working in a repository
where `TheKnowledge/` is present only as a read-only submodule or otherwise
not directly writable.

Today, there is not a clearly standardized place in the consuming project to
record those proposed upstream changes in a durable, reviewable form. The
result is predictable:

- requests get buried in general `docs/` folders
- requests get mixed into unrelated project notes
- naming and placement vary from project to project
- future handoff to a writable TheKnowledge checkout becomes less obvious

That is a process gap. TheKnowledge already has a `Feedback` branch workflow
for upstream-directed findings, but consuming projects also need a local,
human-readable holding area for engineering change requests before those
requests are executed upstream.

## Desired Direction

Adopt this directory structure as the standard consuming-project pattern when
TheKnowledge is being used read-only:

- `ECRs/README.md`
- `ECRs/TheKnowledge/README.md`
- one or more request documents under `ECRs/TheKnowledge/`

The intended meaning is:

- `ECRs/` is the top-level home for engineering change requests aimed at
  external or upstream systems
- `ECRs/TheKnowledge/` is the dedicated area for requests aimed at
  TheKnowledge
- each ECR file should be named clearly enough that another operator or AI
  agent can pick it up and execute it in a writable upstream checkout

## What I Want Changed In TheKnowledge

### 1. Document the pattern

Update TheKnowledge's guidance so consuming projects are told to use
`ECRs/TheKnowledge/` when they need to draft upstream engineering change
requests locally before those requests can be implemented in a writable
TheKnowledge checkout.

### 2. Explain when to use it

The guidance should make this distinction clear:

- use TheKnowledge's existing direct-maintenance workflows when working in a
  writable TheKnowledge checkout
- use `ECRs/TheKnowledge/` in the consuming project when TheKnowledge is
  effectively read-only in that environment and the team needs a local,
  reviewable request record

### 3. Keep it first-class and visible

The pattern should not be left as tribal knowledge or scattered examples.
Relevant starter docs, workflow docs, or managed guidance should mention it
explicitly so different consuming projects converge on the same structure.

### 4. Keep it compatible with existing upstream feedback flow

This directory convention should complement, not replace, TheKnowledge's
`Feedback` branch and proposal workflows. The local ECR tree is for drafting,
tracking, and handing off upstream requests from a consuming project. Actual
TheKnowledge maintenance still belongs in TheKnowledge's writable workflows.

## Acceptance Criteria

This request is not complete unless all of the following are true in the
writable TheKnowledge checkout:

1. TheKnowledge documentation defines `ECRs/TheKnowledge/` as the standard
   consuming-project location for upstream change requests when TheKnowledge
   is read-only locally.
2. The guidance explains the purpose of both `ECRs/README.md` and
   `ECRs/TheKnowledge/README.md`.
3. The guidance distinguishes local ECR drafting from direct writable
   maintenance in TheKnowledge itself.
4. Managed starter or workflow guidance points consuming projects toward this
   structure rather than leaving the storage location ad hoc.

## Suggested Work Plan For The Other Codex Instance

1. Inspect the current feedback-branch and consuming-project workflow docs.
2. Identify the best canonical doc locations for this new convention.
3. Update the guidance to define the `ECRs/` and `ECRs/TheKnowledge/`
   structure and explain when it should be used.
4. Add or refresh any template text needed so consuming projects inherit the
   pattern cleanly.
5. Run the relevant validation and test suite.
6. Record the change in TheKnowledge's own project-management files.

## Recommended Prompt For The Other Codex Instance

Use the following as the starting task text in the writable TheKnowledge
checkout:

```text
Adopt `ECRs/TheKnowledge/` as the standard consuming-project directory
structure for upstream TheKnowledge change requests when TheKnowledge is
present read-only in the consuming project.

Update TheKnowledge's workflow and starter guidance so consuming projects use
`ECRs/README.md`, `ECRs/TheKnowledge/README.md`, and clearly named ECR files
under `ECRs/TheKnowledge/` instead of scattering upstream requests through
generic docs folders.

Make sure the guidance distinguishes this local ECR staging area from direct
writable maintenance inside TheKnowledge itself and from the existing
Feedback-branch workflow.
```
