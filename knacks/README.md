# Knacks

Knacks are focused, reusable knowledge units. They are analogous to skills in
that they package practical know-how for repeated use, but they live in
TheKnowledge as repository-managed reference material.

A single-file knack may live directly in a category root as `foo.knack.md`.
When a topic grows into a fileset, use `foo.overview.knack.md` plus API
companions whose names begin with `foo.api`.

Small, language-neutral API references may use `foo.api.knack.md`. When an
API is language-specific, append the language tag before `.knack.md`, for
example `foo.api.C.knack.md`, `foo.api.CPP.knack.md`, or
`foo.api.Python.knack.md`. Large APIs may insert subsection tokens before the
language tag, as in `foo.api.rendering.CPP.knack.md`, optionally inside
`foo.knack/` when the fileset becomes large enough to deserve its own
directory.

Projects that use TheKnowledge may also keep proprietary or third-party
knacks in their own top-level `knacks/` directory.
When a project-local knack path collides with a stock TheKnowledge knack
path, tooling should warn and still evaluate both files.

For sizing, split guidance, source expectations, consumer-project layout, and
lightweight validation rules, see `knacks/authoring-guide.md`.

This subtree is organized by topic. Placeholder `README.md` files keep the
scaffold visible in Git until the first knack files for a topic are ready to
land.

Current stock areas include `UI/` for interface work, `sandboxing/` for
process-isolation and execution-boundary guidance, `debugging/` for
high-level AI-assisted debugging habits that stay language-neutral,
`licenses/` for software license triage, `auditing/` for evidence-oriented
review topics such as software bills of materials, and `performance/` for
measurement and profiling guidance such as route load and render profiling.
