# Permissive Short-Notice Licenses

Load this knack when a component uses one of the short permissive licenses
that are easy to conflate in practice: BSD-2-Clause, BSD-3-Clause, ISC,
PostgreSQL, or zlib. These licenses are all business-friendly by design, but
they are not identical. The main review task is to keep the exact notice and
endorsement conditions straight. This is engineering guidance, not legal
advice.

## Licenses Covered

This knack covers:

- BSD-2-Clause;
- BSD-3-Clause;
- ISC;
- PostgreSQL License; and
- zlib License.

All five are permissive. None of them are copyleft. None of them generally
force source publication of your own code merely because you used the
licensed component.

## Family Mental Model

These licenses mostly follow the same commercial posture:

- broad rights to use, modify, and redistribute;
- minimal continuing conditions centered on notices;
- no general obligation to disclose source;
- no trademark grant; and
- an "as is" disclaimer.

The differences are in the fine print:

- BSD-3-Clause adds a non-endorsement clause absent from BSD-2-Clause.
- ISC is even shorter but functionally similar to BSD/MIT in most review
  settings.
- PostgreSQL is BSD-like and commonly treated as very low-friction.
- zlib adds a meaningful anti-misrepresentation and altered-source marking
  requirement.

The engineering error is to flatten them into "MIT-like, who cares." They are
close, but the review still needs the exact license text.

## What You May Usually Do

For all of these licenses, the common allowed cases are broad:

- use the code internally;
- ship compiled products that include it;
- modify the code without publishing your modifications;
- combine it with proprietary code; and
- sell products or services built around it.

That is why these licenses are common in infrastructure libraries, networking
stacks, packaging tools, embedded software, and database ecosystems.

## Obligations By License Shape

BSD-2-Clause is mostly about keeping the copyright notice, conditions, and
disclaimer in source and binary redistributions.

BSD-3-Clause adds the important no-endorsement rule: you may not use the
copyright holder's or contributors' names to endorse or promote derived
products without prior permission. That matters in product pages, app stores,
and sales material.

ISC is similar in spirit to MIT or simplified BSD. Preserve the notice and
disclaimer. It is short, but not optional.

The PostgreSQL License is a BSD-like permissive license widely treated as
commercially easy to consume. The same notice-preservation and no-warranty
discipline still applies.

zlib deserves more attention than it often gets. Beyond notice retention, it
requires that altered source versions be plainly marked and that you not
misrepresent the origin of the software. If you are shipping modified source
or embedding code into a library bundle, make sure the provenance trail stays
honest.

## Compatibility Picture

These licenses are usually highly compatible with other permissive licenses
and are often incorporated into stronger copyleft distributions because their
notice obligations can usually be preserved alongside the stricter combined-
work terms of the other license.

From an engineering standpoint, they are often easier to combine than Apache-
2.0 because they generally lack the extra patent machinery. The flip side is
that they also provide less explicit patent protection.

The main compatibility question is therefore not "can we combine them?" but
"what other license on the product imposes stricter terms once we do?"

## Disallowed Or High-Risk Use Cases

Watch for these cases:

- removing or collapsing the required notice text during vendor bundling;
- implying endorsement under BSD-3-Clause because a project name appears in
  marketing;
- modifying zlib-covered source without marking it as altered;
- treating a repository's code license as if it also covered bundled fonts,
  images, firmware blobs, or model weights;
- assuming all "BSD-like" code has the same exact obligations.

The most common practical failure is sloppy notice aggregation. Short licenses
look ignorable, so teams forget them during binary packaging. That is still a
license issue even if the rest of the stack is more complicated.

## Review Checklist

- Record the exact SPDX identifier, not just "BSD-like."
- Check whether the license has a non-endorsement clause.
- Keep notice files intact in source and binary redistribution paths.
- Mark altered zlib-covered source clearly.
- Treat patents, trademarks, and bundled non-code assets as separate review
  topics.
- If the overall product is copyleft, analyze the stricter combined-work
  obligations separately from these permissive components.

## Further Information

- SPDX BSD-2-Clause page:
  <https://spdx.org/licenses/BSD-2-Clause.html>
- SPDX BSD-3-Clause page:
  <https://spdx.org/licenses/BSD-3-Clause.html>
- SPDX ISC page: <https://spdx.org/licenses/ISC.html>
- PostgreSQL licensing overview:
  <https://www.postgresql.org/about/licence/>
- SPDX zlib page: <https://spdx.org/licenses/Zlib.html>
