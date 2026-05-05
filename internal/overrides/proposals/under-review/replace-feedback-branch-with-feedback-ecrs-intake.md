# Replace the Feedback Branch With a feedback/ECRs Intake Branch

Title: Engineering Change Request: Replace TheKnowledge `Feedback` Branch
With a Dedicated `feedback/ECRs` Intake Branch
Author: Codex
Date: 2026-03-31T15:38:05-07:00
Status: Under Review
Reviewers: operator (repository maintainer), AI maintainers
Related Work: Direct operator request on 2026-03-31; AGENTS.md section
"Feedback Branch"; README.md section "Feedback Branch";
scripts/send_theknowledge_feedback.py;
internal/overrides/proposals/under-review/
structured-ecr-intake-lifecycle-and-deconfliction.md;
standards-and-practices/docs/specifications/
theknowledge_submodule_workflows.txt

Scope note: this proposal is now the narrower branch-policy companion to
`structured-ecr-intake-lifecycle-and-deconfliction.md`, which covers the
broader local ECR directory lifecycle and raw-import deconfliction process.

## Problem Statement
TheKnowledge currently routes cross-project feedback through a special branch
named `Feedback`. That branch was intended to isolate bugs, complaints,
proposals, and general notes discovered while working primarily in consuming
projects. In practice, the dedicated branch has become operationally awkward.

The branch name is unusually broad and easy to overload. It mixes intake,
draft discussion, and potentially stale items in one place while direct
TheKnowledge maintenance continues on `trunk`. That makes it harder to tell
whether a change is a reviewable ECR, a transient note, or an implementation
candidate. It also creates friction for tooling and contributors because the
workflow has to preserve and restore branch state that differs from the
normal `trunk` maintenance model.

The result is more ceremony than clarity. Contributors have to remember which
kind of feedback belongs on `Feedback`, maintainers have to periodically
reconcile that side branch with `trunk`, and helper/docs complexity grows
around a workflow that is still easy to misunderstand.

## Goals
- Replace the vague special-purpose `Feedback` branch with a more explicit
  intake branch named `feedback/ECRs`.
- Narrow the intake branch's purpose to reviewable Engineering Change
  Requests and related structured feedback, rather than an undifferentiated
  catch-all queue.
- Reduce ambiguity between direct TheKnowledge maintenance on `trunk` and
  cross-project feedback intake.
- Update helper/documentation language so contributors know exactly where to
  place structured cross-project feedback.

## Non-Goals
- Eliminate TheKnowledge's ordinary `trunk` maintenance workflow.
- Force every transient note or investigation scratchpad onto
  `feedback/ECRs`.
- Prevent maintainers from converting an ECR into a normal `trunk` task once
  it is reviewed and approved.
- Redesign the whole project-management record model inside
  `internal/overrides/`.

## Use Cases
1. A consuming-project maintainer discovers a cross-project TheKnowledge
   improvement and wants to file a structured ECR without interrupting the
   main project flow.
2. A direct TheKnowledge maintainer wants to review incoming feedback and
   quickly distinguish branch-intake proposals from ordinary trunk work.
3. Helper tooling needs a more explicit default ref name and purpose than the
   generic `Feedback` label.
4. Documentation needs to stop implying that a long-lived side branch should
   carry every kind of unresolved thought.

## Constraints and Assumptions
- Some contributors work through active submodule checkouts inside consuming
  projects, so any intake workflow still has to handle detached HEAD state and
  separate git-dir layouts safely.
- Existing helper tooling and docs currently encode `Feedback` directly, so
  the migration must update both behavior and guidance together.
- The intake branch still needs to be writable by contributors who have
  TheKnowledge push access, while remaining locally useful for contributors
  who can only commit but not push.
- Existing unresolved `Feedback` items may need a migration or closure plan.

## Proposed Approach
Replace the old branch policy with a narrower, clearer one.

Cross-project structured feedback should go to `feedback/ECRs`, not
`Feedback`. That branch should hold reviewable ECR-style records that capture
the problem, proposal, risks, and rollout expectations clearly enough for
later trunk-side evaluation.

To support that policy:
- update TheKnowledge `AGENTS.md` and `README.md` to name `feedback/ECRs`
  instead of `Feedback`;
- update `scripts/send_theknowledge_feedback.py` so its default branch is
  `feedback/ECRs` and its prompts/help text reflect the new purpose;
- update the submodule-workflow specification and any downstream managed
  guidance that still hardcodes `Feedback`;
- document how existing `Feedback` content should be triaged, migrated, or
  retired; and
- keep direct TheKnowledge maintenance on `trunk` unchanged.

This proposal intentionally does not require every unstructured comment to
become an ECR. It only says that the dedicated cross-project branch should
have a clear intake contract instead of acting as a vague side channel.

## Risks and Mitigations
- Risk: contributors may still treat `feedback/ECRs` as a general dumping
  ground.
  Mitigation: define the branch purpose narrowly around structured ECR-style
  records and point ad hoc notes back to ordinary issue/backlog/proposal
  triage on `trunk`.
- Risk: tooling and docs drift if only some surfaces rename the branch.
  Mitigation: update the helper, specs, AGENTS text, README guidance, and
  managed downstream mirrors in one coordinated change.
- Risk: existing `Feedback` history becomes orphaned or confusing.
  Mitigation: perform an explicit migration review, then either archive the
  branch, fast-forward the new intake branch from it, or close it with a
  written note.
- Risk: a dedicated intake branch still proves unnecessary.
  Mitigation: keep the proposal scoped so a later follow-up can retire the
  branch model entirely if trunk-only intake turns out to be better.

## Testing and Validation
- Add or update tests for `scripts/send_theknowledge_feedback.py` so the
  default branch name and help text use `feedback/ECRs`.
- Update doc-wiring tests that assert branch-policy language in TheKnowledge
  and downstream template surfaces.
- Perform a submodule-checkout smoke test: capture state, switch to
  `feedback/ECRs`, record a draft ECR, restore the previous state, and verify
  that the helper still works without assuming push rights.
- Review and document the disposition of any existing `Feedback` items before
  declaring the migration complete.

## Alternatives Considered
1. Keep `Feedback` and only clarify its docs.
   Rejected because the name and branch purpose remain too broad and keep the
   existing ambiguity alive.
2. Put all cross-project feedback directly on `trunk`.
   Not selected yet because the operator specifically requested a clearer
   dedicated intake branch rather than no intake branch at all.
3. Use a differently named dedicated branch such as `feedback/intake` or
   `feedback/proposals`.
   Not selected at draft time because `feedback/ECRs` best matches the
   structured-record intent that prompted this proposal.
4. Keep the branch but drop the helper.
   Rejected because submodule state capture/restore remains valuable even if
   the branch name changes.

## Open Questions
1. Should `feedback/ECRs` be created fresh from `trunk`, or should it inherit
   the current `Feedback` history first?
2. Which existing `Feedback` items, if any, should be migrated verbatim into
   ECR records?
3. Should the helper keep its current name
   (`send_theknowledge_feedback.py`) for compatibility even if the branch
   becomes ECR-focused?

## Milestones
1. Review and approve or revise this ECR.
   Target date: 2026-04-02.
   Owners: operator, AI maintainers.
   Dependencies: review of the existing `Feedback` workflow pain points.
   Entry criteria: proposal exists under review.
   Exit criteria: operator decision recorded in the proposal.
2. Define the migration plan for existing `Feedback` content.
   Target date: 2026-04-03.
   Owners: operator, AI maintainers.
   Dependencies: proposal approval.
   Entry criteria: approved branch-policy direction.
   Exit criteria: historical `Feedback` disposition is documented.
3. Implement the branch-policy update.
   Target date: 2026-04-04.
   Owners: AI maintainers.
   Dependencies: approved policy and migration plan.
   Entry criteria: docs/specs/helper targets are identified.
   Exit criteria: helper defaults, docs, and tests all point at
   `feedback/ECRs`.

## Adoption and Rollout
If approved, land the branch-policy update on `trunk`, create or migrate the
new intake branch deliberately, and update helper/docs/tests together so
contributors get one coherent story.

After the migration, trunk-side evaluation should continue to decide whether
an intake ECR becomes an implemented trunk change, a deferred proposal, or a
rejected idea. The intake branch should stay for structured cross-project
feedback only.

## Decision Log
- 2026-03-31T15:38:05-07:00 - Drafted by Codex after an operator requested a
  clearer replacement for the old `Feedback` side branch, which had become a
  source of workflow friction and branch-management overhead.
