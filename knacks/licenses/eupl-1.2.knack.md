# EUPL 1.2

Load this knack when software is under the European Union Public Licence 1.2
and the review needs to answer two unusual questions: "what exactly is its
copyleft scope?" and "does its compatibility list help us relicense this into
another approved license?" This is engineering guidance, not legal advice.

## Mental Model

EUPL-1.2 is a copyleft license published by the European Commission. It aims
to be enforceable across EU jurisdictions while also providing an explicit
compatibility path to a list of other licenses in certain redistribution
scenarios. The practical engineering summary is:

- the covered work remains under EUPL by default;
- source must remain available when distributing the work;
- trademarks are not granted; and
- the license contains a compatibility mechanism that can allow onward
  distribution under certain listed compatible licenses.

That last point is what makes EUPL different from many engineers' default
mental models. The compatibility path is explicit and structured, not merely a
hopeful interpretation.

## What You May Usually Do

You may use, modify, and distribute EUPL-covered software, including in
commercial settings, so long as you comply with the license. It is open source
and not a non-commercial license.

Where teams become uncertain is mixed-license distribution. EUPL anticipated
that issue and therefore provides a compatibility list that can matter when
you distribute derivatives that would otherwise have conflicting obligations.

## Obligations That Matter

When distributing or communicating copies of the work, you must provide source
code or indicate a repository where the source remains easily and freely
available while you continue distributing or communicating the work. Preserve
the copyright and license trail. Do not assume the license grants trademark
rights.

EUPL also contains warranty and liability limitations, but unlike some short
permissive licenses it spends more attention on authorship chain and European
legal framing.

## Compatibility And Relicensing

The compatibility list is the most operationally important EUPL feature. When
the obligations of a listed compatible license conflict with EUPL in a
derivative distribution, the compatible license can prevail for that
distribution path. That makes EUPL unusually explicit about certain outward
relicensing routes.

However, do not treat the list as a general permission to relicense into
anything. It is a bounded compatibility mechanism. If the target license is
not on the list, or the derivative structure does not match the intended use
of the mechanism, the safe answer is still "pause and review."

## Disallowed Or High-Risk Use Cases

Watch for these patterns:

- redistributing EUPL-covered code without an actual source-availability plan;
- assuming the compatibility clause means "universal compatibility";
- using the upstream project name or institutional identity as if trademark
  rights were granted;
- moving EUPL-covered code into a product with conflicting terms without
  checking whether the target license is actually on the compatibility list.

EUPL is often manageable, but only if the compatibility step is treated as a
documented legal mechanism rather than a vague intuition that European public
licenses must somehow be flexible.

## Common Scenario Triage

If you are simply redistributing an EUPL-covered application with your own
unrelated software, the main work is ordinary notice and source-path hygiene.
If you are creating a derivative that must enter an ecosystem under another
license, the compatibility appendix becomes the first document to inspect, not
the last.

That makes EUPL a license where release engineering and legal triage have to
talk early. The value of the compatibility list is real, but only when the
target license and the derivative structure actually fit what the text allows.

## Review Checklist

- Confirm the exact version is EUPL-1.2.
- Record the planned distribution scenario and the target jurisdictions if
  relevant.
- Verify whether you are staying under EUPL or relying on a listed compatible
  license.
- Ensure source availability remains concrete and durable.
- Preserve notices and keep trademark assumptions out of the implementation
  plan.
- Escalate if the proposed target license is not explicitly listed.

## Further Information

- European Commission EUPL collection:
  <https://joinup.ec.europa.eu/collection/eupl>
- SPDX EUPL-1.2 page: <https://spdx.org/licenses/EUPL-1.2.html>
- EUPL text and compatibility appendix:
  <https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12>
- European Commission EUPL FAQ:
  <https://joinup.ec.europa.eu/collection/eupl/faq>
- OSI EUPL page: <https://opensource.org/license/eupl-1-2>
