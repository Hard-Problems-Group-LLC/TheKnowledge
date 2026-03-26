# Source-Available Business Licenses

Load this knack when a component looks open because the source is visible, but
the actual license may block common commercial or service-provider use. This
document covers Business Source License 1.1 and Server Side Public License
1.0, two licenses that routinely trip policy reviews because people mistake
source availability for open-source approval. This is engineering guidance,
not legal advice.

## Licenses Covered

- Business Source License 1.1 (`BUSL-1.1`)
- Server Side Public License 1.0 (`SSPL-1.0`)

These licenses should not be treated like MIT, Apache, GPL, or MPL. Their
business posture is different, and many organizations review them under a
separate non-open-source policy path.

## Mental Model

Business Source License 1.1 is source-available, not OSI-approved open source.
It allows the licensor to define an "Additional Use Grant" and a future
"Change Date" after which the software converts to another license. Until that
date and outside the granted use, the restricted terms control.

SSPL-1.0 also is not OSI-approved open source. It is based on AGPL ideas but
adds a much broader service-provider condition. If you offer the functionality
as a service, the obligation can extend beyond the program itself to the
service stack used to make the service available.

The engineering summary is stark:

- visible source code does not mean low-friction commercial use;
- cloud or managed-service use is often the central policy question; and
- these licenses may be unacceptable by default in organizations that are fine
  with classic open-source licenses.

## BUSL-1.1 Practical Reading

With BUSL, the first question is not "is production use allowed?" The first
question is "what does this specific licensor's Additional Use Grant say?"
Some licensors allow fairly broad development or low-scale use. Others carve
out the core monetized use case entirely.

That means no generic BUSL approval is safe. You must read the actual license
file shipped with the product because the use grant and change date are part
of the operational meaning.

Disallowed or high-risk BUSL cases include:

- deploying into production beyond the Additional Use Grant;
- treating the future change date as if it already applies now;
- recording only "BUSL" in an SBoM without the project-specific use grant.

## SSPL-1.0 Practical Reading

SSPL is usually reviewed as hostile to unmanaged cloud-service reuse. If you
offer the program as a service, the required source release can extend to the
management software and service code needed to provide that service. That is a
much broader obligation than many teams expect.

Common high-risk SSPL cases:

- offering a managed service around SSPL software while assuming ordinary
  AGPL instincts are enough;
- embedding SSPL software in a cloud platform with proprietary orchestration
  or operations layers;
- approving SSPL because the source repository is public and therefore "looks
  open source."

## Compatibility And Policy Reality

The key compatibility point is that these licenses are often incompatible with
an organization's normal open-source intake assumptions. Even if technically
combinable with your code, they may violate policy because the business model
or disclosure trigger is the problem.

For SBoMs and due diligence, this means the right flag is not just "copyleft"
or "permissive." It is often "source-available" or "restricted commercial
use." If your tooling cannot express that distinction, human review has to.

## Common Scenario Triage

If the intended use is internal experimentation only, BUSL or SSPL may still
be acceptable for some organizations, but only through a conscious exception
path. If the intended use is a customer-facing SaaS or managed service, assume
from the start that the license is a commercial-strategy question, not just a
notice question.

For procurement and M&A diligence, these licenses deserve their own label in
inventories and dashboards. Collapsing them into generic "open source" counts
creates misleading risk summaries and can make later policy decisions look
like surprises.

## Review Checklist

- Record the exact full license name, not just an acronym.
- For BUSL, read the actual Additional Use Grant and Change Date in the
  project's license file.
- For SSPL, analyze the hosted-service model before any adoption decision.
- Do not mark either license as OSI-approved open source.
- Route the intake through the organization's restricted-license path.
- Reflect the precise license and any project-specific grant details in the
  SBoM and third-party review record.

## Further Information

- MariaDB Business Source License 1.1:
  <https://mariadb.com/bsl11/>
- SPDX BUSL-1.1 page: <https://spdx.org/licenses/BUSL-1.1.html>
- SPDX SSPL-1.0 page: <https://spdx.org/licenses/SSPL-1.0.html>
- OSI position on non-approved licenses:
  <https://opensource.org/licenses>
- MongoDB licensing overview:
  <https://www.mongodb.com/legal/licensing/server-side-public-license>
