# Interpreters and Package Management Environments

## Scope

Define the default environment-selection and package-management precedence
model that TheKnowledge should prefer across Python, Node.js, and other
interpreter-driven toolchains.

This document is broader than the current Python bootstrap specification. It
describes the desired cross-language standard that language-specific setup
flows should implement.

## Precedence Model

When looking for an interpreter or packages for that interpreter, prefer this
order, with each later layer overriding the earlier layer when it exists:

1. System-wide installation
2. User-local installation
3. User-selected profile or context
4. Project-specific override

The intent is:

- System-wide installation is the lowest common denominator and the fallback
  when nothing more specific exists.
- User-local installation lets one user override system defaults without
  mutating the operating system for other users.
- User-selected profiles let one user intentionally choose a language runtime
  family or version line across many projects.
- Project-specific overrides let one project force the exact interpreter and
  package set it requires for development or validated execution.

The project-specific override is the highest-precedence layer.

## Required Behavior

### General

- Environment resolution should be explicit, deterministic, and documented.
- Higher-precedence layers must not silently disappear just because a lower
  layer is present.
- Setup flows should prefer reusing an existing suitable lower layer before
  installing a more local layer unnecessarily.
- Project-local overrides should be checked into the repository when practical
  so the expected runtime is reviewable.

### Development or Edit Install

- A development or editable install must bind execution to the project-specific
  environment.
- If the project provides a launcher for developer use, that launcher should
  keep using the project-specific interpreter and packages even when invoked
  outside the project directory.
- For Python projects using TheKnowledge's managed bootstrap, the usual place
  to implement that launcher behavior is a repository-local
  `scripts/install_project.py` hook invoked by `scripts/install-stage-2.py`.
- Entering the project directory should be sufficient to activate the expected
  development interpreter and package set automatically.
- Supporting shell hooks and directory-entry tooling are part of the developer
  install contract, not optional polish.

### Normal Per-User Install

- A normal per-user install should stay in user scope, not system scope.
- It should avoid excessive side-by-side copies where practical, while still
  guaranteeing the required interpreter and package versions.
- Reusing one user-scoped interpreter family with multiple environment roots is
  usually preferred over repeatedly bundling fully independent interpreter
  trees for every tool.
- If a dedicated per-tool environment is used, that choice should be justified
  by version isolation, distro packaging constraints, or safety.

### Automatic Project Entry

- For development workflows, the user should normally only need to `cd` into
  the project directory to get the expected interpreter and packages.
- That implies a checked-in project selector plus user-installed shell
  integration.
- The project selector should win over user-global profiles while the shell is
  inside the project.

## Language-Specific Interpretation

### Python

The usual target model is:

1. System Python
2. User-local Python installation
3. User-selected Python profile, typically through `pyenv`
4. Project-specific override, typically `.python-version` plus a repo-local
   `.venv`

For packages, the normal development target is:

1. System site packages only as a bootstrap fallback
2. User-local packages only for user-scoped tools or bootstrap recovery
3. User-selected Python profile selects the interpreter family
4. Project-local virtual environment provides the final development package set

`direnv` or equivalent automatic activation is the preferred way to make the
project-local package set active on directory entry.

### Node.js

The usual target model is:

1. System Node.js and npm
2. User-local Node.js installation
3. User-selected Node.js profile, for example through `fnm`, `nvm`, `volta`,
   `asdf`, or an equivalent user-scoped selector
4. Project-specific override through a checked-in version selector such as
   `.node-version`, `.nvmrc`, `.tool-versions`, or a project-managed launcher

For packages, the normal development target is:

1. System-global packages only as a last-resort bootstrap layer
2. User-global packages only for user tools that are intentionally shared
3. Project-local package installs and lockfiles for project behavior
4. Project-local command shims such as `node_modules/.bin` taking precedence
   in development shells

Where possible, use `corepack` or the checked-in package-manager declaration so
the project chooses the expected package-manager family and version.

### Other Interpreters

The same pattern should hold for Ruby, Rust, Java, Go, and similar stacks:

1. System-wide runtime
2. User-local runtime
3. User-selected profile manager
4. Project-specific override

Examples include `rustup`, `sdkman`, `asdf`, language-native toolchains, or
checked-in wrapper scripts. The exact tool may vary, but the precedence rule
should not.

## Design Rules for TheKnowledge

- Language-specific bootstrap documents should describe how they implement this
  precedence model.
- New managed starter flows should prefer user-scoped runtime managers over
  system mutation once a bootstrap interpreter exists.
- Project-local overrides should be explicit files or managed launchers rather
  than undocumented shell assumptions.
- Managed developer installs should set up both the runtime selector and the
  directory-entry activation mechanism.
- Managed user installs should prefer a sensible user-scoped package layout
  over direct system package mutation.

## Practical Implications

- A project-specific override is not complete if it only works after a manual
  activation command that developers are expected to remember.
- A user-selected profile is not a substitute for a project-specific override.
- A project-specific override should not require the developer to uninstall or
  bypass their preferred user-global runtime manager.
- A bootstrap flow that only addresses Python but ignores Node.js or other
  required interpreters is only a partial implementation of this standard.

## Relationship to Existing TheKnowledge Specs

- `standards-and-practices/docs/specifications/python_bootstrap_and_context_strategy.txt`
  defines the current Python-specific managed implementation.
- `standards-and-practices/docs/specifications/tool_validation_profiles_and_python_runtime_selection.txt`
  defines how Python validation tooling resolves its managed runtime.
- This document is the broader policy that future multi-language bootstrap
  designs should satisfy.
