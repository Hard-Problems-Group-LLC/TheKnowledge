# GNU Affero GPL v3

Load this knack when a component is under AGPL-3.0 and the question is not
"can we distribute this?" but "what happens if we run a modified version as a
service?" AGPL is where many teams discover that SaaS is not the loophole they
assumed it was. This is engineering guidance, not legal advice.

## Mental Model

AGPL-3.0 is GPL-3.0 plus a network interaction clause intended to close the
classic application-service-provider gap. Under plain GPL, a party could
modify the program, run it on a server, and never distribute a copy to users.
AGPL adds a requirement to offer the Corresponding Source of the modified
version to users who interact with it remotely over a network.

The engineering translation is:

- AGPL has strong copyleft like GPL-3.0;
- it keeps GPL-3.0's patent and installation-information structure; and
- it adds a source-availability trigger for network use of modified versions.

If your product model is hosted software, AGPL is a first-order design and
commercial issue, not a footnote.

## What It Usually Allows

AGPL still allows use, modification, and redistribution. It is free software.
You may run it internally. You may modify it. You may distribute it under the
license terms. You may even build a business around it. What you do not get is
the ability to keep a modified service-side version closed merely because
customers access it through a browser or API instead of by downloading a
binary.

## Core Trigger

The recurring review question is simple:

"Will outside users interact with our modified version over a network?"

If yes, AGPL likely matters immediately. If no, and the program remains purely
internal, the operational risk is lower. But do not stretch "internal" beyond
recognition. Customer-facing hosted software is exactly the use case AGPL was
written to reach.

## Compatibility And Combination Risks

AGPL is stricter than GPL for network deployment. That makes combination
analysis sensitive. If an AGPL component and your own code form one combined
program or derivative work, you should assume the AGPL may reach the combined
work unless a clear boundary or exception says otherwise.

This is why many companies treat AGPL as a policy-triggering license even when
they are comfortable with GPL in more limited desktop or device settings.

AGPL can also be incompatible with internal platform assumptions. A team may
intend to expose a modified service while keeping orchestration, admin layers,
or extension code closed. Depending on the architecture, that can be exactly
the scenario the AGPL disrupts.

## Disallowed Or High-Risk Use Cases

These should trigger immediate legal and architecture review:

- modifying AGPL software and exposing the modified service to customers
  without a source publication plan;
- embedding AGPL code into a larger hosted platform and assuming only the
  upstream files are affected;
- treating API-only access as a way around source duties;
- copying AGPL code into closed internal platform modules that will back a
  customer-facing service;
- confusing AGPL with "non-commercial only." It is not that. It is free
  software with strong copyleft conditions.

Another risk is operational drift. Teams may begin with a clean, unmodified
upstream service, then add local patches, integrations, or custom modules over
time. The compliance posture can quietly change with each customization.

## Common Scenario Triage

Three recurring scenarios help separate AGPL noise from AGPL substance.

First, if you run an unmodified AGPL service internally for staff only, the
primary engineering work is still governance and change tracking. The risk is
that "internal only" quietly turns into partner or customer access later.

Second, if you expose the service to customers and you modify it, assume from
the outset that a source-offer workflow is part of the product design. Waiting
until launch week to ask what "Corresponding Source" means is how teams end up
re-architecting or abandoning the component under deadline pressure.

Third, if your platform wraps an AGPL component with proprietary management,
workflow, or billing layers, do not rely on intuition about separability.
Document the boundaries and escalate the architecture for review before the
platform spreads through production.

## Review Checklist

- Confirm the exact identifier is AGPL-3.0 and not GPL-3.0.
- Determine whether customers or third parties interact with the running
  software over a network.
- Decide whether your organization will modify the AGPL component.
- Map whether local extensions create one combined work or stay clearly
  separable.
- Plan how Corresponding Source would be offered to network users if required.
- Treat hosted-product revenue models as part of the license review, not a
  separate business conversation.

## Practical Reading

AGPL is often manageable when you deliberately embrace the model: use the
software, comply, publish required source, and compete on operations or other
value. It is a bad fit when the business assumption is "we will take this
server software, customize it heavily, and never disclose those changes."

## Further Information

- GNU AGPL-3.0 text: <https://www.gnu.org/licenses/agpl-3.0.en.html>
- GNU "Why the Affero GPL":
  <https://www.gnu.org/licenses/why-affero-gpl.html>
- GNU GPL FAQ: <https://www.gnu.org/licenses/gpl-faq.html>
- SPDX AGPL-3.0-only page:
  <https://spdx.org/licenses/AGPL-3.0-only.html>
- GNU license list discussion of AGPL:
  <https://www.gnu.org/licenses/license-list.html>
