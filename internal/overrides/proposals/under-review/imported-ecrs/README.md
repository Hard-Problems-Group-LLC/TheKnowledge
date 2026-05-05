# Engineering Change Requests

This directory holds imported engineering change requests that were carried
into TheKnowledge for review.

Imported ECR holding directories must not include source-project names. Keep
the original ECR filename as the durable source-facing identifier and record
accepted or implemented entries in
`internal/overrides/proposals/accepted-ecrs-list.md`.

This directory is a raw intake inbox, not the final proposal set. Deconflict
the imported ECRs into top-level actionable TheKnowledge proposals under the
parent `under-review/` directory and keep the mapping in
`deconfliction-map.md`.

When a consuming project's source ECR enters active upstream handling, its
local record should normally move from `ECRs/TheKnowledge/open/` to
`ECRs/TheKnowledge/in-progress/`. When the upstream proposal, implementation,
rejection, or deferral is recorded, move the source ECR to
`ECRs/TheKnowledge/closed/` with a note pointing to the TheKnowledge record
that resolved it.

Filename collisions are expected to be rare. If an incoming ECR filename
collides with an existing imported ECR, stop and ask the operator how to
disambiguate the record.
