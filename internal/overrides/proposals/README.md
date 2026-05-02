# Repository Maintenance Proposals

Keep TheKnowledge proposal records here instead of in the starter templates.
Proposal records should be Markdown (`.md`) files.

Use `accepted-ecrs-list.md` to record imported ECR filenames that
TheKnowledge has accepted or implemented. External projects can compare that
filename list against their own submitted ECRs without TheKnowledge naming
the source project.

Use the status directories to reflect each proposal's current state:
- `approved/`
- `rejected/`
- `deferred/`
- `under-review/`

Imported ECR holding directories should use the project-neutral name
`imported-ecrs/`. Do not include the source project's name in the directory
path; keep the original ECR filename as the durable identifier. Filename
collisions are expected to be rare and should be resolved manually by an
operator when they occur.

Keep `templates/project-management/proposals/` as starter material unless the
template wording or examples are being revised.
