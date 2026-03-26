# Apache License 2.0

Load this knack when a dependency, SDK, or internal component is under
Apache License 2.0 and the review needs more than "it is permissive." Apache
2.0 is usually easy to adopt, but it carries a clearer patent story and a few
more notice mechanics than MIT. This is engineering guidance, not legal
advice.

## Mental Model

Apache-2.0 is a permissive license with explicit conditions around notices,
modified files, trademarks, and patents. The engineering shorthand is:

- you can use, modify, and redistribute the software, including in
  proprietary products;
- you must preserve required notices and mark significant changes in modified
  files; and
- you receive an explicit patent license from contributors, with termination
  if you initiate certain patent claims.

That patent clause is one reason many companies prefer Apache-2.0 over MIT for
foundational libraries. It is not "stricter copyleft." It is still
permissive. It just states more of the deal explicitly.

## What You May Usually Do

Typical allowed patterns include:

- using Apache-2.0 code internally without publication;
- shipping modified or unmodified binaries in proprietary products;
- combining the code with many other permissive or weak-copyleft components;
- sublicensing your own contributions under other terms where the Apache
  covered material still retains its Apache obligations; and
- offering commercial support or paid distribution.

Like MIT, Apache-2.0 does not require you to open your proprietary additions
merely because you used Apache-licensed code.

## Obligations That Actually Bite

The obligations people forget are usually these:

- include a copy of the license;
- preserve copyright, patent, trademark, and attribution notices from the
  source form where required;
- state significant changes in modified files; and
- handle any upstream `NOTICE` file correctly.

The `NOTICE` mechanism is easy to mishandle. It does not mean every upstream
README note becomes a legal requirement. It does mean that if the upstream
distribution carries a `NOTICE` file, relevant attribution notices from it
must remain in your distribution according to the license terms.

Apache-2.0 also does not grant trademark rights. The license lets you
redistribute code, not market your derivative as if it were the upstream
vendor's endorsed product.

## Patent Effects

The explicit patent license is one of Apache-2.0's most important features.
Contributors grant patent rights needed to use their contributions. But the
license also contains a patent-termination clause: if you bring patent
litigation claiming the work or a contribution infringes your patent, your
patent license under Apache-2.0 can terminate.

For engineering review, that means Apache-2.0 is often friendlier than MIT
for patent-sensitive adoption, but it also means patent disputes are not
orthogonal to license risk.

## Compatibility And Mixing

Apache-2.0 plays well with many permissive and some weak-copyleft licenses.
The most famous sharp edge is GPL compatibility. Apache's own compatibility
guidance states that Apache-2.0 is compatible with GPL version 3, but not with
GPL version 2 without the "or later" escape hatch. That matters because some
older projects remain GPL-2.0-only.

In practical terms:

- Apache-2.0 plus GPL-3.0 can often be distributed together under GPL-3.0
  combined-work terms while preserving Apache notices.
- Apache-2.0 plus GPL-2.0-only is a known stop sign.
- Apache-2.0 is commonly fine beside MIT, BSD, ISC, PostgreSQL, zlib,
  MPL-2.0 larger works, and many commercial codebases.

Always ask whether the relevant unit is mere aggregation, linking, or an
integrated combined work. Compatibility statements usually assume a combined
distribution, not two unrelated programs on the same disk image.

## Disallowed Or High-Risk Use Cases

Pause the review when you see any of these:

- distributing modified Apache files without marking significant changes;
- dropping upstream `NOTICE` content that should travel with the
  redistribution;
- assuming Apache-2.0 solves a GPL-2.0-only compatibility problem;
- using the upstream project name or logos as if the license granted
  trademark rights; or
- ignoring the patent-termination clause in a setting with active IP
  disputes.

Another subtle risk is relicensing confusion. You may license your own changes
or surrounding product under other terms, but you do not get to erase the
Apache-2.0 conditions from the Apache-covered material.

## Review Checklist

- Confirm the package is truly Apache-2.0 and not a custom enterprise add-on.
- Identify whether an upstream `NOTICE` file exists.
- Decide where license and notice materials will live in shipped artifacts.
- If modified files are redistributed, make sure the change markers are real.
- Check GPL interaction explicitly when the other side is GPL-2.0-only or
  unclear.
- Treat patents and trademarks as first-class review topics, not footnotes.

## Further Information

- Apache License 2.0 text:
  <https://www.apache.org/licenses/LICENSE-2.0>
- Apache GPL compatibility note:
  <https://www.apache.org/licenses/GPL-compatibility>
- Apache license and distribution FAQ:
  <https://www.apache.org/foundation/license-faq.html>
- SPDX Apache-2.0 page:
  <https://spdx.org/licenses/Apache-2.0.html>
- GNU license list discussion of Apache-2.0:
  <https://www.gnu.org/licenses/license-list.html>
