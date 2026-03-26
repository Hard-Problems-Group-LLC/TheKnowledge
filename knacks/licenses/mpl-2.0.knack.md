# Mozilla Public License 2.0

Load this knack when code is under MPL-2.0 and the team needs to know whether
it behaves like a permissive license or a full-project copyleft license. The
short answer is: neither. MPL-2.0 is file-level copyleft. This is engineering
guidance, not legal advice.

## Mental Model

MPL-2.0 is designed to keep modifications to covered files open while allowing
the larger work around those files to remain under different terms. It sits
between permissive licenses and strong copyleft licenses in practical effect.

The core engineering rule is:

- if you modify an MPL-covered file and distribute that file, the file stays
  under MPL;
- separate files in a larger work can remain under other licenses; and
- the whole product does not automatically become GPL-style copyleft merely
  because one module is MPL-covered.

That file-level boundary is why MPL is attractive for browser code, SDKs,
platform components, and libraries that want reciprocal improvements without
forcing every adopter to open an entire product.

## What You May Usually Do

Common allowed cases:

- use MPL-covered code in commercial or proprietary products;
- distribute a larger mixed-license work;
- keep new files that are not covered by MPL under different licenses; and
- modify the MPL files so long as you keep those files under MPL and provide
  required source availability for them when distributing.

This makes MPL operationally much easier for many businesses than GPL, while
still protecting the openness of the covered files themselves.

## Obligations That Matter

If you distribute executable form of MPL-covered software, you need to make
the source for the MPL-covered files available under MPL-2.0. Preserve notices
and identify changes appropriately. Do not erase the license header trail.

MPL-2.0 also contains patent provisions and trademark limits. Like other
software licenses, it is not a trademark license.

One unique feature is the concept of "Incompatible With Secondary Licenses."
By default, MPL-2.0 can permit certain downstream relicensing paths to GPL,
LGPL, or AGPL as secondary licenses. If a file or notice marks the code as
incompatible with those secondary licenses, that escape hatch narrows.

## Compatibility Picture

MPL is often compatible with commercial products because the copyleft stays at
the file level. A larger work can include MPL files and proprietary files side
by side. That does not mean you can silently modify MPL files and close those
modified files.

The secondary-license mechanism is especially important when mixed with GPL
ecosystems. Some MPL-2.0 code can participate in GPL-family combinations more
smoothly than older weak-copyleft licenses because the license explicitly
planned for that path.

Still, do not assume all MPL code is automatically GPL-compatible in all
contexts. Check for any "Incompatible With Secondary Licenses" notice and
verify the actual combination pattern.

## Disallowed Or High-Risk Use Cases

Stop and review when you see:

- modified MPL files being distributed without offering their source;
- teams assuming that because the overall product is proprietary, the modified
  MPL files can also be kept closed;
- relicensing plans that ignore the secondary-license settings;
- aggressive file merging that turns clear file boundaries into one tangled
  derived file set;
- confusion between code under MPL and separate assets or documentation under
  other terms.

The main MPL failure mode is architectural drift. A codebase starts with neat
file boundaries, then refactors begin moving substantial MPL code into files
the team expects to keep proprietary. That is exactly the moment to pause.

## Common Scenario Triage

If your product merely bundles an MPL-covered library unchanged, the review is
usually straightforward: keep the notices, keep the source path for the MPL
files, and do not overstate ownership of the upstream code.

If your team intends to patch the MPL files directly, the question shifts from
"can we use this?" to "how will we publish or offer the modified covered
files?" That can still be perfectly workable, but it needs an explicit release
path.

If the plan is to move code back and forth across the file boundary between
MPL-covered modules and proprietary modules, stop and design the boundary
deliberately. MPL stays comfortable when the file line is clear. It becomes
messier when refactors blur where the covered work begins and ends.

## Review Checklist

- Identify which specific files are MPL-covered.
- Ask whether your changes modify those files or live entirely in new files.
- Confirm how you will publish or offer source for distributed MPL files.
- Check for any "Incompatible With Secondary Licenses" notice.
- Preserve headers, notices, and change history accurately.
- Treat patents and trademarks as separate review topics.

## Further Information

- Mozilla MPL-2.0 FAQ: <https://www.mozilla.org/en-US/MPL/2.0/FAQ/>
- MPL-2.0 text: <https://www.mozilla.org/en-US/MPL/2.0/>
- SPDX MPL-2.0 page: <https://spdx.org/licenses/MPL-2.0.html>
- Mozilla licensing policy overview:
  <https://www.mozilla.org/en-US/MPL/>
- GNU license list discussion of MPL-2.0:
  <https://www.gnu.org/licenses/license-list.html>
