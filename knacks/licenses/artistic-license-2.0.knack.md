# Artistic License 2.0

Load this knack when a package from the Perl or language-tooling world is
under Artistic-2.0 and you need a practical answer about redistribution,
modification, and GPL compatibility. Artistic-2.0 is open source and often
usable in commercial settings, but it is not one of the ultra-short
permissive templates. This is engineering guidance, not legal advice.

## Mental Model

Artistic-2.0 tries to preserve both freedom to modify and clarity about what
is still the original standard version versus a modified version. It is often
described as a permissive or moderately reciprocal license, but the safest
engineering understanding is:

- you may use, modify, and redistribute the software;
- if you distribute modified versions, you must do so in one of the compliant
  ways the license describes;
- you must preserve licensing and attribution information; and
- the license cares about not confusing your modified version with the
  original standard version.

That identity-protection idea is more central here than in MIT or BSD review.

## What You May Usually Do

Typical allowed patterns include:

- internal use and modification;
- shipping unmodified versions;
- distributing modified versions if you clearly identify them and comply with
  the distribution options in the license; and
- combining Artistic-2.0 components into larger software distributions.

Artistic-2.0 is generally acceptable in commercial products. The important
thing is to preserve the distinction between original and modified versions and
to keep the license trail intact.

## Obligations That Matter

The license offers several compliant ways to distribute a modified version.
The specifics matter more than with MIT because Artistic-2.0 is not just "keep
the notice and do whatever." You need to follow one of the sanctioned
distribution paths and make sure users can get the original or the source in
the way the license expects.

Do not represent your modified fork as if it were the unchanged standard
version from the original author. Preserve notices. Keep packaging honest.

## Compatibility Picture

Artistic-2.0 is generally regarded as GPL-compatible. That helps in mixed free
software ecosystems. Still, GPL compatibility does not mean zero review.
Confirm the exact license version and the actual combination pattern.

In proprietary products, the main questions are usually not GPL interaction
but whether the team's redistribution packaging still makes the identity of
the modified version clear and whether the required source or notice materials
remain available.

## Disallowed Or High-Risk Use Cases

Treat these as red flags:

- distributing a modified version while presenting it as the upstream standard
  release;
- dropping required notices or source-availability paths;
- treating Artistic-2.0 as if it were identical to MIT just because both are
  commercially usable;
- bundling it into a product with separate asset licenses and assuming the
  code license covers the whole distribution.

The common mistake is not hostility from the license. It is underestimating
how much the license cares about version identity and transparent packaging.

## Common Scenario Triage

If you are shipping an unmodified upstream package, Artistic-2.0 is usually a
low-drama review. Keep the notices and preserve the upstream identity.

If you are shipping a locally modified fork, document how users will tell that
your build is not the standard upstream version and how they can obtain the
relevant source or original package information. That is where the license's
structure matters operationally.

For mixed-license distributions, keep the Artistic-2.0 code path visible
rather than burying it under a generic "third-party notices" label. The
license is commercially usable, but it still expects honest packaging.

## Review Checklist

- Confirm the package is Artistic-2.0, not Artistic-1.0 or a dual-license
  variant.
- If modified, document how the distributed version will be identified.
- Preserve the license and attribution trail.
- Check whether the distribution path satisfies the license's source or
  original-version access expectations.
- If combined with GPL ecosystems, verify the exact version and combination
  path.

## Further Information

- OSI Artistic-2.0 page:
  <https://opensource.org/license/artistic-2-0>
- SPDX Artistic-2.0 page:
  <https://spdx.org/licenses/Artistic-2.0.html>
- Perl licensing overview: <https://dev.perl.org/licenses/>
- GNU license list discussion of Artistic-2.0:
  <https://www.gnu.org/licenses/license-list.html>
- Choose a License overview of Artistic-2.0:
  <https://choosealicense.com/licenses/artistic-2.0/>
