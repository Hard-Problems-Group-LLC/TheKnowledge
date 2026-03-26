# MIT License

Load this knack when you are reviewing a dependency, template, snippet, or
starter project under the MIT License and need the practical engineering
answer to "what can we do with this, and what must we preserve?" This is
engineering guidance, not legal advice.

## Mental Model

MIT is the classic short permissive software license. In day-to-day review,
the important idea is that it gives broad permission to use, copy, modify,
merge, publish, distribute, sublicense, and sell the software so long as the
copyright notice and license text travel with substantial portions of the
software. It also disclaims warranty and liability.

If you are used to copyleft licenses, MIT is the opposite default posture.
It does not try to make downstream changes open. It does not require source
publication. It does not care whether your larger work is proprietary. The
basic trade is:

- the author gives you broad reuse rights;
- you keep the attribution and disclaimer intact; and
- you accept that the software comes with no warranty.

That simplicity is why MIT code appears in templates, SDKs, JavaScript
packages, small utilities, and internal starter code. It is easy to adopt and
usually easy to redistribute.

## What You May Usually Do

The common allowed cases are broad:

- copy the code into an internal or proprietary project;
- modify the code without publishing your changes;
- ship binaries or source in commercial products;
- combine MIT code with code under many other licenses; and
- relicensing your own additions under different terms so long as you do not
  remove the MIT notice from the MIT-covered portions.

In practice, engineers often read MIT as "almost no strings attached." That
is directionally right, but not exact. The surviving string is the notice
obligation, and ignoring it is still noncompliance.

## Obligations That Matter

The license notice must remain in copies or substantial portions of the
software. In a source distribution, that usually means leaving the header or
including the license file. In a binary distribution, that usually means
including third-party notices, license bundles, or another documented path
that travels with the product.

The warranty disclaimer matters too. It protects the upstream author and is
part of the license package you received. Do not strip it out when
consolidating notices.

MIT does not grant trademark rights. A common review mistake is to treat a
copyright license as permission to use the upstream product name, logo, or
brand identity in marketing. Those are separate issues.

MIT is also silent on patent grants in the way Apache-2.0 is not. Many teams
are comfortable with that, but if the patent position matters, MIT may be
less comforting than Apache-2.0.

## Compatibility Picture

MIT is broadly compatible with other open-source licenses because its
conditions are light and mainly preserved through attribution. It is commonly
combined with Apache-2.0, BSD-family licenses, MPL-2.0 larger works, and even
GPL-family distributions because the downstream distributor can usually
preserve the MIT notice while satisfying the stricter license on the overall
distribution.

What MIT does not do is erase the obligations of the other side. If MIT code
is combined into a GPL-covered program, the combined distribution still has to
honor GPL obligations for the overall work. The MIT part stays MIT-licensed,
but the act of distribution may be governed by the stricter combined-work
rules.

MIT is therefore best thought of as compatible upward into stricter systems,
not as a shield against them.

## Disallowed Or High-Risk Use Cases

These are the patterns that deserve a stop-and-check response:

- Removing the copyright notice or license text from copied MIT code.
- Shipping a binary product that bundles MIT code while forgetting to include
  third-party notices anywhere in the product materials.
- Assuming the license grants trademark or endorsement rights.
- Treating MIT as a patent-safe substitute for Apache-2.0 when patent
  retaliation or explicit patent grants are material to the deal.
- Copying MIT code from a repository that also contains assets, models, or
  documentation under different licenses and assuming the whole repository is
  uniformly MIT.

Another recurring problem is snippet laundering. A developer may copy MIT code
through a blog post, gist, or AI output and lose the original notice chain.
If the code is still substantial enough to be a protected portion of the
original work, the notice obligation did not disappear just because the copy
path got sloppy.

## Review Checklist

- Confirm the exact license text is MIT, not a variant with extra clauses.
- Identify where the copyright and license notice will live in shipped
  artifacts.
- Check whether the package also carries separate notices for fonts, docs,
  sample data, or trademarks.
- If patent comfort matters, compare Apache-2.0 before standardizing on MIT.
- If the code will be combined into a copyleft product, review the combined
  distribution obligations under that other license too.

## Further Information

- SPDX MIT page: <https://spdx.org/licenses/MIT.html>
- OSI MIT page: <https://opensource.org/license/MIT>
- Choose a License MIT summary:
  <https://choosealicense.com/licenses/mit/>
- Apache Software Foundation license compatibility page:
  <https://www.apache.org/licenses/GPL-compatibility>
- GNU license list discussion of permissive licenses:
  <https://www.gnu.org/licenses/license-list.html>
