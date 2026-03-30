# TheKnowledge ECR: Dual-Python Coding Standards and Dramatically Complete Documentation

## Purpose

This document is an engineering change request for another Codex instance
working inside a writable checkout of `TheKnowledge`.

The goal is to make two expectations part of TheKnowledge's normal guidance:

- Python `3.9` best practices for bootstrap and setup code
- Python `3.12` best practices for normal runtime, application, test, and
  automation code

It also asks TheKnowledge to adopt a much stronger documentation standard
than it currently defines.

## Problem Statement

TheKnowledge's current guidance is not strong enough in two ways.

First, its Python baseline is still expressed as a general `3.9+`
compatibility statement instead of distinguishing between bootstrap/setup code
and modern runtime/tooling code.

Second, its current documentation standard is materially weaker than the bar
needed for long-lived AI-assisted maintenance. The current
`documentation_standard_profile.txt` says, in effect:

- public modules should have concise docstrings
- public or externally consumed call points should be documented where needed
- inline comments should be used sparingly for rationale

That is not the same as requiring complete, systematic, high-fidelity
documentation across the codebase. It leaves too much room for undocumented
internal helpers, undocumented local complexity, and thin source-file
introductions that force future readers to reverse-engineer design intent.

## Desired Direction

Adopt the following as the new normal for TheKnowledge.

### Python Version Expectations

- Bootstrap, setup, prerequisite, and environment-selection code should
  follow Python `3.9` best practices.
- Normal runtime, application, automation, test, and developer-tooling code
  should follow Python `3.12` best practices unless a specific component is
  intentionally constrained.
- The guidance should make the split explicit instead of implying one Python
  standard fits every part of the tree.

### Documentation Expectations For Every Language

Documentation should be dramatically complete: thorough, accurate, readable,
and maintained as part of delivery.

At minimum, the standard should require:

- top-of-file documentation for every source file, covering purpose, role in
  the project, scope, theory of operation, important dependencies or
  constraints, testing strategy, and any additional context needed for safe
  maintenance
- documentation for every class, dataclass, struct, enum, protocol, or
  similar construct
- documentation for every function, method, coroutine, closure, local helper,
  or other callable at any scope
- documentation for every structured block of logic with non-trivial McCabe
  complexity
- documentation that explains intent, invariants, control flow, failure
  behavior, side effects, and usage contracts rather than merely restating
  syntax

When a language has native docstrings or API comment conventions, the
documentation should live there. When it does not, the same standard should
be met with block comments or other idiomatic equivalents.

## AutoTomato Reference

AutoTomato now carries a local override in its top-level `AGENTS.md` that
captures this stronger standard for the consuming project. That override can
be used as a starting reference for the wording and intent, but TheKnowledge
should adapt the policy to its own repository structure and template model.

## What I Want Changed In TheKnowledge

### 1. Strengthen the central documentation standard

Revise:

- `AGENTS.md`
- `standards-and-practices/docs/specifications/documentation_standard_profile.txt`

The updated language should stop framing documentation as mainly a
public-API-level concern and should explicitly require complete source-file,
type, function, and non-trivial control-flow documentation.

### 2. Distinguish bootstrap Python from runtime Python guidance

Revise the relevant standards and workflow text so TheKnowledge explicitly
states:

- Python `3.9` best practices apply to bootstrap/setup paths
- Python `3.12` best practices apply to normal runtime and tooling paths

This should align with the Python bootstrap split already proposed in the
separate AutoTomato handoff for startup scripts.

### 3. Update starter and template guidance

Inspect the managed starter material and template docs so consuming projects
inherit the stronger standard rather than the older, weaker one.

Likely update targets include:

- managed `AGENTS.md` language or generator inputs
- workflow documentation
- starter templates under `templates/`
- any language-specific SOPs that currently underspecify documentation depth

### 4. Keep the rule actionable

The final wording should be specific enough that reviewers and AI agents can
apply it consistently. Avoid vague formulations such as "document where
helpful" or "document public APIs where needed" without also defining the
minimum required coverage.

## Acceptance Criteria

This request is not complete unless all of the following are true in the
writable TheKnowledge checkout:

1. `AGENTS.md` clearly states the stronger documentation expectations.
2. The canonical documentation standard profile reflects the same coverage
   requirements.
3. TheKnowledge's Python guidance explicitly distinguishes bootstrap/setup
   work from normal runtime/tooling work.
4. Managed starter guidance for consuming projects inherits the stronger
   documentation expectations.
5. The updated language is concrete enough that a reviewer can tell when a
   file, type, function, or complex logic block is under-documented.

## Suggested Work Plan For The Other Codex Instance

1. Read the current `AGENTS.md`, documentation standard profile, and relevant
   workflow docs.
2. Identify every place where TheKnowledge currently describes documentation
   as a concise or public-API-only concern.
3. Update the standards docs and managed guidance to require dramatically
   complete documentation.
4. Update the Python-language guidance so bootstrap/setup paths and
   runtime/tooling paths are treated separately.
5. Regenerate or revise any managed starter material that would otherwise
   continue emitting the weaker policy.
6. Run the affected validation and test suite.
7. Record the change in TheKnowledge's own project-management files.

## Recommended Prompt For The Other Codex Instance

Use the following as the starting task text in the writable TheKnowledge
checkout:

```text
Adopt AutoTomato's stronger coding and documentation standard as the new
normal for TheKnowledge.

Update TheKnowledge so bootstrap/setup code follows Python 3.9 best
practices, while normal runtime, application, test, and tooling code follows
Python 3.12 best practices unless intentionally constrained.

Strengthen TheKnowledge's documentation standard so it requires dramatically
complete documentation for every language: top-of-file documentation for each
source file; documentation for every class, dataclass, struct, enum,
protocol, or similar construct; documentation for every function or callable
at any scope; and local documentation for every structured block of logic
with non-trivial McCabe complexity.

Update AGENTS.md, the canonical documentation standard profile, and any
managed starter/template guidance needed so consuming projects inherit this
standard rather than the current weaker public-API-focused one.
```
