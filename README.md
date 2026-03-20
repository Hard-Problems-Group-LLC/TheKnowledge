# TheKnowledge

A reusable knowledge base for software project operations, engineering
standards, and AI/human collaboration practices.

## Purpose

`TheKnowledge` captures the process backbone that remains useful across
radically different projects: web apps, desktop tools, data systems, CLI
utilities, and more. It is intentionally separate from any single product's
business logic.

## Long-term objective

This repository is intended to become a shared reference and eventually a Git
submodule that other projects can import. The goal is consistent execution:
- technical standards and operating practices,
- project management standards and operating practices,
- cross-platform validation strategies,
- reproducible quality gates and safety checks.

## Scope

This repository includes:
- `standards-and-practices/`: reusable workflows, standards, security
  practices, runbooks, and dev utilities.
- `templates/`: starter material meant to be copied into consuming projects.
- `scripts/`: reusable tooling plus setup helpers for submodule consumers.
- `internal/`: repository-local state for maintaining TheKnowledge itself.
  TheKnowledge's live project-management state lives under
  `internal/overrides/`; the starter material under
  `templates/project-management/` stays pristine unless the reusable framework
  itself is being revised.

This repository does **not** include product-specific source code or
application business logic.

## Intended use

1. Import this repository (or a subtree thereof) into active projects.
2. Run `scripts/initial-setup.py` from the submodule to install starter files
   from `templates/` into the consuming project root.
3. Keep project state in the consuming project's own directories rather than
   inside the submodule.
4. Add language/technology SOPs under
   `standards-and-practices/docs/sop/` as needed.

## Using as a submodule

For an existing Git repository, add TheKnowledge at the path you want the
team to keep stable:

```bash
git submodule add https://github.com/Hard-Problems-Group-LLC/TheKnowledge.git \
  TheKnowledge
git submodule update --init --recursive
python TheKnowledge/scripts/initial-setup.py \
  --project-root . \
  --knowledge-root TheKnowledge
```

For a brand-new repository, initialize the repo first and then add the
submodule:

```bash
mkdir TestProject
cd TestProject
git init -b trunk
git submodule add https://github.com/Hard-Problems-Group-LLC/TheKnowledge.git \
  TheKnowledge
git submodule update --init --recursive
python TheKnowledge/scripts/initial-setup.py \
  --project-root . \
  --knowledge-root TheKnowledge
```

After that setup, commit both the new `.gitmodules` file and the generated
project-management and `AGENTS.md` files in the consuming project.

When another developer clones the consuming project later, they should either
clone with submodules enabled:

```bash
git clone --recurse-submodules <project-url>
```

or initialize them after clone:

```bash
git submodule update --init --recursive
```

## Submodule layout

The consuming project chooses the submodule path at `git submodule add` time.
For example:

```text
TestProject/
  TheKnowledge/
    standards-and-practices/
    templates/
    scripts/
```

After running the template installer, the consuming project keeps its own
stateful files outside the submodule:

```text
TestProject/
  TheKnowledge/
  project-management/
    backlog.txt
    tasks-in-progress.txt
    completed-tasks.txt
    deferred.txt
    ai-human-requests.txt
    proposals/
      approved/
      rejected/
      deferred/
      under-review/
    state/
      pending-commit-changes.txt
    bugs/
      open/
      in-progress/
      closed/
```
