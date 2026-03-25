# Knacks

Knacks are focused, reusable knowledge units. They are analogous to skills in
that they package practical know-how for repeated use, but they live in
TheKnowledge as repository-managed reference material.

A single-file knack may live directly in a category root as `foo.knack.md`.
When a topic grows into a fileset, use `foo.overview.knack.md` and
`foo.api.knack.md`, optionally inside `foo.knack/` when the fileset becomes
large enough to deserve its own directory.

Projects that use TheKnowledge may also keep proprietary or third-party
knacks in their own top-level `knacks/` directory.
When a project-local knack path collides with a stock TheKnowledge knack
path, tooling should warn and still evaluate both files.

For sizing, split guidance, source expectations, consumer-project layout, and
lightweight validation rules, see `knacks/authoring-guide.md`.

This subtree is organized by topic. Placeholder `README.md` files keep the
scaffold visible in Git until the first knack files for a topic are ready to
land.
