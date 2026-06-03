# Codex-Wrangler Awareness And Proactive Ignore Baseline

| Field | Value |
| --- | --- |
| Title | Codex-Wrangler Awareness And Proactive Ignore Baseline |
| Author | Codex |
| Date | 2026-05-02T15:50:17-07:00 |
| Status | Approved |
| Reviewers | operator (repository maintainer), AI maintainers |
| Related Work | `AGENTS.md`; `.gitignore`; `internal/overrides/proposals/approved/project-root-dot-local-for-local-operator-state-and-tooling.md`; `internal/overrides/proposals/approved/theknowledge-tool-runtime-isolation-and-bootstrap-reliability.md` |

## Problem Statement
TheKnowledge already needs to coexist with repo-local Codex CLI installs and
codex-wrangler-managed local artifacts. When a repository is not prepared for
those artifacts before first use, maintainers get avoidable noise:
untracked-path surprises, accidental staging risk, and confusion about which
files are local operator tooling versus tracked project payload.

The current repository now ignores the known local Codex artifacts, but that
expectation is not yet captured as an approved TheKnowledge proposal that can
drive starter guidance and future managed setup behavior across consuming
projects.

## Goals
- Make codex-wrangler awareness an explicit part of TheKnowledge guidance.
- Require proactive ignore coverage for known local Codex artifacts even
  before a repository starts using them.
- Keep those artifacts clearly classified as local operator state, not
  tracked project dependencies or shipped runtime payload.
- Keep the ignore baseline deliberate and reviewable rather than ad hoc.

## Non-Goals
- Requiring every repository to install or use codex-wrangler.
- Treating all future hidden paths as ignorable without review.
- Checking codex-wrangler-generated local artifacts into version control.

## Use Cases
1. A repository adopts TheKnowledge before any local Codex CLI bootstrap has
   happened and still wants a clean `git status` when those artifacts appear
   later.
2. A maintainer uses codex-wrangler to provision a repo-local Codex CLI and
   should not have to decide path by path which generated files belong in
   `.gitignore`.
3. An AI maintainer sees `.codex-local/` or `bin/codex-local` and needs an
   explicit rule that they are local-only artifacts rather than tracked
   product files.

## Constraints And Assumptions
- TheKnowledge should remain usable in repositories that never adopt
  codex-wrangler.
- The ignore baseline must be safe to ship in starter material even when the
  corresponding paths do not yet exist.
- The managed ignore set should be limited to known codex-wrangler and local
  Codex CLI artifacts with clear operator-local intent.

## Proposed Approach
Treat codex-wrangler awareness as baseline repository hygiene in
TheKnowledge-managed projects.

The managed `.gitignore` baseline should include the currently known local
Codex artifacts whether or not they already exist in the checkout:
- `.codex-local/`
- `.codex-home/`
- `.codex`
- `bin/codex-local`
- `README-LOCAL-Start-Codex.md`

TheKnowledge guidance should also state that:
- these paths are local operator tooling or generated artifacts;
- they must not be treated as tracked project dependencies;
- `.codex-local/package.json` must not be classified as the repository's own
  dependency manifest; and
- future codex-wrangler-generated artifact paths should be added to the
  managed ignore baseline intentionally, not left to per-repository
  improvisation.

This policy should apply to TheKnowledge itself and to generated starter
material for consuming projects.

## Risks And Mitigations
- Risk: a future real project file could collide with a proactively ignored
  path.
  Mitigation: keep the list narrow, documented, and specific to known local
  Codex artifact paths.
- Risk: repositories that never use codex-wrangler may view the ignores as
  noise.
  Mitigation: the entries are low-cost, stable, and prevent later accidental
  staging when codex-wrangler is introduced.

## Testing And Validation
- Verify that TheKnowledge guidance and managed ignore behavior treat the
  listed paths as local-only artifacts.
- Verify that repositories generated from TheKnowledge starter material carry
  the proactive codex-wrangler ignore baseline.
- Verify that introducing those local artifacts after repository bootstrap
  does not create avoidable untracked or staged noise.

## Alternatives Considered
1. Add ignore entries only after codex-wrangler is first used.
   Rejected because it creates predictable first-use churn and invites
   accidental staging.
2. Rely on operator memory or local global Git ignores.
   Rejected because TheKnowledge should provide a repository-local baseline.
3. Fold these entries into the general `.local/` policy only.
   Rejected because the codex-wrangler artifacts use distinct established
   paths that still need explicit ignore coverage.

## Open Questions
None at approval time. The approved scope is to keep TheKnowledge and its
starter guidance proactively aware of the currently known codex-wrangler
artifact set and to extend that set deliberately when codex-wrangler grows.

## Milestones
1. Record the approved policy.
   Target date: 2026-05-02.
   Owners: operator, AI maintainers.
   Dependencies: none.
   Entry criteria: operator requests an approved baseline policy.
   Exit criteria: proposal exists under `approved/`.
2. Align starter guidance and managed ignore behavior with the approved
   policy.
   Target date: next implementation pass.
   Owners: operator, AI maintainers.
   Dependencies: review of how managed `.gitignore` content is generated for
   consuming projects.
   Exit criteria: TheKnowledge guidance and starter material both carry the
   proactive codex-wrangler ignore baseline.

## Adoption And Rollout
Keep the current TheKnowledge ignore behavior, then carry the same proactive
ignore baseline into starter guidance and any managed `.gitignore`
generation path used for consuming projects.

## Decision Log
- 2026-05-02T15:50:17-07:00 - Added directly as an approved proposal per
  operator instruction so TheKnowledge treats codex-wrangler awareness and
  proactive ignore coverage as baseline behavior.
- 2026-05-08T13:36:20-07:00 - Marked implemented. TheKnowledge's own
  `.gitignore`, managed starter `.gitignore` template, direct and downstream
  guidance, local-operator-state specification, and regression coverage now
  treat `.codex-local/`, `.codex-home/`, `.codex`, `bin/codex-local`, and
  `README-LOCAL-Start-Codex.md` as proactive local Codex or codex-wrangler
  ignores, and clarify that `.codex-local/package.json` is not a tracked
  project dependency manifest.
