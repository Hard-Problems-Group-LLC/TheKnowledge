# Boost Software License 1.0

Load this knack when you encounter C++, systems, or tooling code under the
Boost Software License 1.0 and need to know whether it behaves more like MIT
or more like a library copyleft license. The short answer is that it is a very
permissive license, but it is worth keeping its exact notice rule and name
distinct from Business Source License terms. This is engineering guidance, not
legal advice.

## Mental Model

Boost Software License 1.0 is a short permissive license designed for broad
reuse, including in commercial and proprietary software. In practice it lives
in the same adoption bucket as MIT, BSD, ISC, and PostgreSQL for many review
purposes.

The broad pattern is:

- use, reproduce, display, distribute, execute, and transmit the software;
- prepare derivative works and allow third parties to do the same; and
- preserve the license notice in copies of the software and derivative works.

It has no copyleft trigger, no source-publication requirement, and no general
field-of-use restriction.

## What You May Usually Do

Commonly allowed cases:

- vendor the code into proprietary repositories;
- ship products that statically or dynamically link it;
- modify it without publishing the modifications;
- redistribute source or binary forms commercially; and
- sublicense your surrounding code under other terms.

This is why BSL-1.0 is popular in C++ ecosystems and low-friction distribution
pipelines.

## Obligations That Matter

The core continuing duty is preserving the license notice. The license also
contains the familiar disclaimer of warranty and liability. That means the
usual permissive-license packaging discipline still applies: keep third-party
licenses somewhere real in your source or binary distribution.

Boost Software License does not grant trademark rights, and it does not carry
the explicit patent machinery of Apache-2.0. If patents matter, compare the
risk posture rather than assuming all permissive licenses are equivalent.

## Compatibility Picture

BSL-1.0 is widely compatible with permissive, weak-copyleft, and many stronger
copyleft distributions because its notice obligations are light. It usually
behaves like a component that can be absorbed into a stricter overall
distribution so long as its own notice survives.

The real compatibility trap here is naming confusion. Engineers often say
"BSL" and mean either Boost Software License 1.0 or Business Source License
1.1. Those are profoundly different licensing models. Boost is OSI-approved
open source. Business Source License is source-available and typically
time-delayed into a later open-source license after a change date.

Never let a dependency-review spreadsheet record only "BSL" without the full
name or SPDX identifier.

## Disallowed Or High-Risk Use Cases

Watch for these errors:

- dropping the license notice during vendoring or code-generation steps;
- confusing Boost Software License with Business Source License;
- assuming the permissive code license grants permission to use project marks
  in product branding;
- using a repository-level BSL label without checking whether some subtrees
  carry different licenses.

The biggest real-world problem is not hostility from the Boost license. It is
misclassification that sends the component down the wrong policy path.

## Common Scenario Triage

For most adoption reviews, Boost Software License behaves like a low-friction
permissive license. The right questions are packaging hygiene, notice
retention, and whether the repository contains any differently licensed
subtrees.

The moment someone says "it is under BSL," slow down and expand the acronym.
If they mean Business Source License instead, the intake path changes
completely. That one naming ambiguity is important enough to treat as a
standard review checkpoint in SBoMs and third-party spreadsheets.

## Review Checklist

- Record the identifier as `BSL-1.0` or "Boost Software License 1.0."
- Preserve the notice in source and redistributed binary materials.
- Keep trademark review separate from copyright review.
- If patent comfort matters, compare Apache-2.0 alternatives.
- Reject ambiguous spreadsheets or SBoMs that say only "BSL."

## Further Information

- Boost license information:
  <https://www.boost.org/users/license.html>
- SPDX BSL-1.0 page: <https://spdx.org/licenses/BSL-1.0.html>
- Boost license background and FAQ:
  <https://www.boost.org/doc/libs/release/more/license_info.html>
- GNU license list discussion of Boost:
  <https://www.gnu.org/licenses/license-list.html>
- OSI license category overview:
  <https://opensource.org/licenses>
