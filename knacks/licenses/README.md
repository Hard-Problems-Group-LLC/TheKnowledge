# Licenses

Load this area when a change, dependency, SBoM review, or distribution plan
turns into a license question. The goal here is not to replace counsel. It is
to help an engineer or agent recognize the major license families, the high-
risk incompatibilities, and the distribution or service models that need
deliberate review before code is copied, linked, bundled, or shipped.

This library covers a practical top twenty set of software licenses and
license families that show up often in modern engineering, commercial due
diligence, or supply-chain review:

- `mit-license.knack.md`: MIT License.
- `apache-license-2.0.knack.md`: Apache License 2.0.
- `permissive-short-notice-licenses.knack.md`: BSD-2-Clause,
  BSD-3-Clause, ISC, PostgreSQL, and zlib.
- `gpl-lgpl-v2-v3.knack.md`: GPL-2.0, GPL-3.0, LGPL-2.1, and LGPL-3.0.
- `agpl-3.0.knack.md`: GNU Affero GPL v3.
- `mpl-2.0.knack.md`: Mozilla Public License 2.0.
- `epl-2.0.knack.md`: Eclipse Public License 2.0.
- `cddl-1.0.knack.md`: Common Development and Distribution License 1.0.
- `eupl-1.2.knack.md`: European Union Public Licence 1.2.
- `artistic-license-2.0.knack.md`: Artistic License 2.0.
- `boost-software-license-1.0.knack.md`: Boost Software License 1.0.
- `source-available-business-licenses.knack.md`: BUSL-1.1 and SSPL-1.0.

How to use these knacks:

- Start with the license on the component you actually plan to consume, not
  with a vague family label.
- Separate use cases. Internal use, SaaS, distribution of binaries, shipping
  source, static linking, dynamic linking, embedding assets, and offering a
  managed service do not carry the same obligations.
- Distinguish code licenses from trademark and patent questions. Many
  permissive licenses are easy on copyright conditions but still do not grant
  trademark rights, and some add patent termination rules.
- Treat incompatibility warnings as engineering stop signs, not as hints to
  improvise around legal text.
- Escalate early when a document says "not open source," "service trigger,"
  "secondary license," or "GPL-incompatible."

Common license-review questions:

- Are we merely running this internally, or are we distributing it?
- Are we combining the licensed code with our own code into one program or
  product image?
- Is the dependency itself copyleft, or does it only apply at the file level?
- Does the license impose patent retaliation, notice, source-offer, or
  relinkability obligations?
- Is the component actually open source, or only source-available?
- If we expose modified software over a network, does the license treat that
  as a trigger?

For software-bill-of-materials generation and review, pair this area with
`knacks/auditing/Software-Bill-of-Materials.knack.md`.
