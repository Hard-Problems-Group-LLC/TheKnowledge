# Knack Authoring Guide

Knacks are meant to be loaded whole for a concrete task or debugging session,
then summarized back out when active context needs to shrink. That operating
model drives the size, naming, sourcing, and validation guidance here.

## Size Guidance

Overview documents should target about 1,250 words. That is usually enough
space to explain the mental model, common workflows, sharp edges, and
cross-references without turning the overview into a manual of its own.

API-reference documents should target about 2,500 words per file. When a
technology has a large API surface, split it into API section documents of
roughly that size when practical. Keep `<basename>.api.knack.md` as either the
complete API reference for a small API or the index document for the larger
API subsection set.

Treat 5,000 words as the recommended absolute maximum for any single knack
file. This is a per-file ceiling, not a cap on an entire multi-file knack
fileset. If a topic still needs more room, prefer more files over bigger
files.

Rationale: these targets keep a knack small enough to load alongside related
knacks and the live task context while still being substantial enough to solve
real implementation and debugging problems. The 5,000-word ceiling is there to
preserve composability and reload speed with today's models.

## Naming And Layout

Use a single-file knack directly in the category root when one document is
enough, for example `ansi.knack.md`.

When a topic needs more than one document, use
`<basename>.overview.knack.md` for the conceptual and operational entry point
and `<basename>.api.knack.md` for the API-focused companion.

When a fileset grows large enough to deserve its own container, move it into a
subdirectory named `<basename>.knack/`. For example, a larger terminal knack
set might use `xterms.knack/xterms.overview.knack.md` and
`xterms.knack/xterms.api.knack.md`.

Rationale: the naming scheme keeps related files adjacent in directory
listings, makes it obvious which file to load first, and leaves room for API
subsections without hiding the main overview document.

## Consumer Project Layout

TheKnowledge may be used in isolation or as a submodule inside another
project. In a consuming project, keep stock knacks inside the TheKnowledge
subtree and keep project-specific or third-party knacks in the consuming
project's own top-level `knacks/` directory.

When a project-local knack path collides with a stock knack path, warn the
operator and evaluate both files instead of silently preferring one.

Rationale: this keeps proprietary or vendor-specific knowledge outside the
shared TheKnowledge subtree while still allowing stock and project-local
material to coexist.

## Lightweight Validation

Knack-specific validation should stay light. Individual knack files do not need
dedicated unit tests beyond the lightweight validation described here unless a
separate project-specific requirement explicitly demands more.

Use `scripts/validate_knacks.py` to validate changed knack files. The validator
checks basic Markdown well-formedness and high-entropy findings as errors, and
reports word-count recommendation overruns as warnings. It uses a hash cache at
`.git/knack-validation-cache.json` so unchanged knack files can be skipped.

Rationale: drafting a knack should trigger only the checks that protect the
library's usability and safety. Broader code-oriented test suites are usually
noise when the change is only a knowledge document.

## Sources And Further Information

Each knack should include a clearly labeled further-information section. When
possible, include at least five authoritative, high-longevity URLs.

Prefer durable sources such as official documentation, language standards,
standards-body publications, vendor manuals, reference manuals, and canonical
project repositories. When fewer than five durable sources exist, include the
best available set and note the limitation plainly.

Rationale: knacks should help an agent act now, but they should also make it
easy to verify claims, refresh stale details, and hand the work to a human or
another model without losing the provenance trail.

## Validation And Triage

Treat knack naming and size tests as hygiene and consistency checks. If one of
those tests fails, record the issue in bug tracking so it stays visible and
gets cleaned up deliberately.

Do not default those bugs to serious or high-priority status. They should
normally be triaged as lower-priority maintenance issues unless the failure is
symptomatic of a broader correctness problem, blocks active delivery, or shows
that the guidance itself is no longer workable.

Rationale: these failures matter because they preserve the reliability of the
knack library, but they usually do not represent the same class of risk as a
runtime defect, data-loss bug, or security problem.
