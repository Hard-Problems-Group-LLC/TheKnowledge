# Eclipse Public License 2.0

Load this knack when a dependency or extension ecosystem is under EPL-2.0 and
you need to decide whether proprietary integration is routine, conditional, or
blocked. EPL-2.0 is a weak copyleft license with its own vocabulary and
secondary-license machinery. This is engineering guidance, not legal advice.

## Mental Model

EPL-2.0 is designed for collaborative software ecosystems in which
contributors want reciprocal treatment for modifications to the covered
program, but do not necessarily want every surrounding tool or plug-in to be
forced under the same license. The practical middle ground is:

- modifications and certain derivative treatments of the EPL-covered program
  stay under EPL;
- separate modules may remain under other licenses; and
- commercial use is allowed.

That makes EPL common in toolchains, runtimes, IDE ecosystems, and
infrastructure projects built around extension boundaries.

## What You May Usually Do

Typical allowed patterns include:

- using EPL software internally;
- distributing unmodified or modified versions under EPL terms;
- building commercial products around EPL software; and
- combining the EPL-covered program with separate modules under other terms
  when the architecture truly preserves separateness.

The exact module boundary matters. EPL is weaker than GPL, but not so weak
that every integration pattern becomes irrelevant.

## Obligations That Matter

If you distribute the covered program or your modifications to it, you must
make source for the EPL-covered portions available under EPL. Preserve notices
and respect the patent and liability framework in the license.

EPL-2.0 also includes a "Secondary License" mechanism that can allow certain
GPL-family compatibility paths when the initial contributor has not disabled
that option. This is one of the most useful and most overlooked parts of the
license in mixed ecosystems.

Like Apache and MPL, EPL does not hand out trademark rights.

## Compatibility Picture

The central compatibility questions are:

- are we modifying the EPL-covered program itself?
- are we merely building a separate module that uses its interfaces?
- does the code include or permit a secondary-license path to GPL-family
  terms?

If the answer is "separate module," many commercial use cases are fine. If the
answer is "we modified and redistributed the EPL-covered code," the EPL duties
are front and center. If the answer is "we need GPL compatibility," check the
secondary-license posture explicitly instead of guessing.

## Disallowed Or High-Risk Use Cases

These cases deserve deliberate review:

- merging EPL-covered code into proprietary files while assuming the result is
  still just a separate module;
- redistributing modified EPL code without publishing the covered source;
- ignoring the license's patent and secondary-license provisions;
- treating extension APIs and derivative code as if the line is always
  obvious;
- relying on GPL compatibility without checking whether the relevant material
  actually carries the secondary-license permission.

The operational danger with EPL is boundary optimism. Teams often assume that
because a system has plug-ins, every part of it must count as separate. That
is an architectural claim, not a default truth.

## Common Scenario Triage

In plug-in ecosystems, the safest initial question is whether your code is
truly just using published interfaces or whether it copies, modifies, or
embeds EPL-covered implementation code. The more your module depends on the
covered internals rather than stable extension points, the weaker the
"separate module" argument becomes.

For redistributors, another useful distinction is vendor packaging versus
upstream contribution. If you are only shipping an unchanged EPL component next
to your own software, the duties are clearer. If you are maintaining a private
fork of the EPL component, then source-delivery and patch management become
release-gating tasks.

## Review Checklist

- Identify whether you are consuming, extending, or modifying the EPL-covered
  code.
- Map the exact boundary between the covered program and your own modules.
- Confirm whether a secondary-license path is available or disabled.
- Preserve required notices and source-delivery planning for covered code.
- Review patents, trademarks, and distribution packaging explicitly.
- Do not collapse "commercial use allowed" into "all proprietary embedding is
  safe."

## Further Information

- Eclipse EPL-2.0 FAQ:
  <https://www.eclipse.org/legal/epl-2.0/faq/>
- EPL-2.0 text:
  <https://www.eclipse.org/legal/epl-2.0/>
- SPDX EPL-2.0 page: <https://spdx.org/licenses/EPL-2.0.html>
- Eclipse legal resources overview:
  <https://www.eclipse.org/legal/>
- GNU license list discussion of EPL:
  <https://www.gnu.org/licenses/license-list.html>
