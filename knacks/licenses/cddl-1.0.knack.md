# CDDL 1.0

Load this knack when you encounter software under the Common Development and
Distribution License 1.0 and need to know why it often triggers more caution
than MPL or EPL in Linux and mixed copyleft ecosystems. CDDL is file-level
copyleft, but it has a reputation for compatibility friction. This is
engineering guidance, not legal advice.

## Mental Model

CDDL-1.0 descends from the Mozilla Public License lineage and is usually
understood as a file-based copyleft license. The broad operating idea is:

- covered files remain under CDDL when distributed;
- modifications to those files must stay under CDDL; and
- the larger work can include files under other licenses, at least in many
  architectural arrangements.

That sounds familiar if you know MPL. The reason CDDL creates more operational
friction is not that it is always harsher in isolation, but that it is widely
treated as incompatible with GPL-family combined-distribution paths.

## What You May Usually Do

CDDL does allow commercial use, modification, and redistribution. It is an
open-source license, not a field-of-use restriction or source-available
business license. Internal use is normally straightforward. Distribution is
also possible if you comply with the CDDL terms for the covered files.

This is why CDDL-covered components can still be perfectly usable when they
remain isolated as separate programs or when the integration boundary is clean
and the product distribution plan has been reviewed deliberately.

## Obligations That Matter

For covered files, preserve the license notices and keep modifications to
those files under CDDL. Make the source for the covered code available when
you distribute executable forms in ways the license requires. Keep the notice
trail intact.

CDDL also includes patent language and defines a contributor-oriented
framework. Like other software licenses, it does not grant trademark rights.

The engineering discipline is similar to MPL in one respect: know exactly
which files are covered and which ones are not. If you blur that boundary, you
make compliance and architecture review harder.

## Why CDDL Gets Special Attention

The major reason is GPL incompatibility. In many organizations, the headline
memory of CDDL is not its file-level structure but the long-running concern
that you cannot safely create one combined distribution that must satisfy both
CDDL and GPL obligations at the same time.

That is why CDDL often appears in policy discussions about filesystem code,
operating-system distributions, and storage stacks. The question is less "is
CDDL commercial?" and more "does this integration path force an impossible or
contested dual-compliance position?"

## Disallowed Or High-Risk Use Cases

Treat these as stop signs:

- combining CDDL-covered code with GPL-covered code in one distributed work
  without deliberate compatibility review;
- moving CDDL-covered content into files the team expects to treat as purely
  proprietary or GPL-only;
- redistributing modified CDDL files without preserving notices and source
  obligations;
- assuming that because the license is open source, Linux-distribution
  compatibility is automatic.

The recurring failure mode is distribution optimism. A component may be fine
in isolation but become problematic once someone insists on shipping it as one
integrated GPL-governed product image.

## Common Scenario Triage

If the component remains a separately distributed program or a clearly
packaged adjacent tool, CDDL may be manageable with ordinary notice and source
discipline. If the plan is to fold the code into a GPL-governed kernel,
runtime, or monolithic appliance image, the compatibility risk becomes central
immediately.

That is why teams should decide early whether the strategy is coexistence or
combination. CDDL often becomes controversial not because of daily development
use, but because product packaging later tries to erase the boundaries that
made the original choice tolerable.

## Review Checklist

- Record the exact identifier as CDDL-1.0.
- Map which files are CDDL-covered.
- Separate internal-use analysis from redistribution analysis.
- Check explicitly for any GPL-family combination or distribution path.
- Keep notices, source-delivery planning, and patent terms visible in the
  release checklist.
- Treat clean process or packaging separation as an architectural fact to
  verify, not an assumption.

## Further Information

- CDDL-1.0 text at SPDX: <https://spdx.org/licenses/CDDL-1.0.html>
- OSI CDDL page: <https://opensource.org/license/cddl-1-0>
- GNU license list discussion of CDDL:
  <https://www.gnu.org/licenses/license-list.html>
- Oracle CDDL page:
  <https://oss.oracle.com/licenses/CDDL+GPL-1.1>
- OpenZFS licensing overview:
  <https://openzfs.org/wiki/License>
