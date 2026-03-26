# GPL And LGPL v2/v3

Load this knack when a dependency is under GPL-2.0, GPL-3.0, LGPL-2.1, or
LGPL-3.0 and you need to know whether linking, bundling, modification, or
distribution turns a routine dependency choice into a release blocker. This is
engineering guidance, not legal advice.

## Licenses Covered

This knack covers four core licenses:

- GNU General Public License version 2;
- GNU General Public License version 3;
- GNU Lesser General Public License version 2.1; and
- GNU Lesser General Public License version 3.

Treat the exact version string as material. `GPL-2.0-only`,
`GPL-2.0-or-later`, `GPL-3.0-only`, `LGPL-2.1-only`, and `LGPL-3.0-only`
are not interchangeable labels.

## Mental Model

GPL is strong copyleft. LGPL is library-oriented weaker copyleft. The
practical distinction is:

- GPL is designed so that distributing a derivative or combined work triggers
  GPL terms for the whole combined program.
- LGPL is designed to allow proprietary or differently licensed applications
  to use the library under defined conditions, while modifications to the
  library itself remain under LGPL.

Version 3 added important rules around installation information, anti-
circumvention, patents, and additional permissions. Version 2 lacks those
specific structures. That means the "v2 or v3?" question is not cosmetic.

## Trigger Question: Internal Use Or Distribution?

Pure internal use is usually much less eventful. Copyleft obligations
primarily become acute when you convey or distribute the software to others.
Once you distribute binaries, however, GPL-family obligations are not a minor
notice issue. They become central to the product design.

If the software is GPL and your product is one combined distributed program,
the safe engineering assumption is that you are in full copyleft territory
unless counsel says otherwise.

## GPL Practical Effects

With GPL-covered code, high-risk cases include:

- statically or dynamically linking GPL code into a proprietary application;
- copying GPL source into a non-GPL codebase;
- shipping GPL binaries without complete corresponding source or a compliant
  written offer where allowed; and
- trying to impose additional downstream restrictions that the GPL does not
  allow.

The GNU FAQ makes clear that static versus dynamic linking is not treated as a
magic escape. If the combination is one derivative or combined work, the GPL
analysis does not become permissive merely because the linker mode changed.

GPL-3.0 adds further sharp edges:

- patent arrangements are more explicit;
- anti-tivoization provisions can require installation information for user
  products in qualifying cases; and
- additional restrictions are constrained more tightly.

## LGPL Practical Effects

LGPL is easier to consume, but it is not "MIT for libraries." The common
working rule is:

- you may use the LGPL library from a proprietary application;
- modifications to the LGPL library itself stay under LGPL; and
- users must be able to replace or relink the LGPL-covered library portion.

The GNU FAQ highlights the relinkability point clearly. If you statically link
an LGPL library, you may need to provide object files or another workable path
that lets users relink against a modified version of the library. Dynamic
linking can be easier, but it is not a universal exemption from all source and
notice duties, especially if you distribute the library itself.

## Compatibility And Known Stop Signs

The most famous compatibility trap is Apache-2.0 with GPL-2.0-only. Apache's
patent terms make that combination incompatible for a combined distribution.
Apache-2.0 can generally work with GPL-3.0 instead.

Other major stop signs:

- GPL code inside a closed-source distributed product without a plan to
  release the combined work under GPL-compatible terms.
- GPL-2.0-only assumptions where a dependency is actually GPL-3.0-only.
- LGPL library modifications merged into a proprietary fork without publishing
  the covered library changes under LGPL.
- Shipping a locked-down appliance with GPL-3.0 software while refusing the
  installation path required for the user's modified version.

Always distinguish "mere aggregation" from one combined program. Two separate
programs on the same media are analyzed differently from one linked product.

## Disallowed Or High-Risk Use Cases

These patterns should stop the rollout until reviewed:

- copying GPL code into a proprietary repository because "it was only a few
  functions";
- shipping GPL executables without source-delivery planning;
- assuming dynamic linking avoids GPL obligations by itself;
- statically linking LGPL code without a relinkability plan;
- treating `or later` language as administrative noise;
- overlooking GPL-3.0 installation-information duties in appliances or other
  controlled user products.

The recurring engineering mistake is to reduce copyleft to a notice file. GPL
and LGPL are architecture-shaping licenses. They affect how you distribute,
package, and sometimes even authenticate software updates.

## Review Checklist

- Record the exact identifier, including `only` versus `or later`.
- Separate internal use, SaaS, and distribution scenarios.
- Determine whether the product forms one combined work or separate programs.
- For LGPL, decide whether you are only using the library or also modifying
  it.
- For static linking, identify the relinkability strategy before release.
- Check Apache, patent, and device-lockdown interactions explicitly.

## Further Information

- GNU GPL FAQ: <https://www.gnu.org/licenses/gpl-faq.html>
- GNU GPL-2.0 text: <https://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
- GNU GPL-3.0 text: <https://www.gnu.org/licenses/gpl-3.0.en.html>
- GNU LGPL-2.1 text:
  <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html>
- GNU LGPL-3.0 text: <https://www.gnu.org/licenses/lgpl-3.0.en.html>
