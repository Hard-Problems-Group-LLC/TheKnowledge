# Software Bill Of Materials

Load this knack when a release, procurement review, incident response effort,
or dependency cleanup task needs an actual SBoM instead of a hand-wavy package
list. An SBoM is a structured inventory of software components and related
metadata. It is useful, but only when you understand how it was generated, how
complete it is, and what audit questions it can and cannot answer.

## Mental Model

An SBoM is not a magical truth file. It is a snapshot of what a tool or build
process could observe about a piece of software at a specific point in time.
Treat it as evidence with provenance, scope, and blind spots.

The practical model has four layers:

1. Inventory collection: package managers, lockfiles, container manifests,
   binary scanners, source scanners, build systems, and hand-maintained
   component declarations.
2. Normalization: identifiers such as package URLs, CPEs, SPDX identifiers,
   version strings, checksums, supplier fields, and dependency edges.
3. Attestation or transport: output in formats such as SPDX or CycloneDX,
   sometimes signed or bundled into release artifacts.
4. Audit use: license review, vulnerability matching, export or procurement
   review, incident response, and change tracking.

If you skip the provenance question and jump straight to audit conclusions, you
will overtrust the document.

## What Good SBoMs Usually Contain

At minimum, a useful SBoM tries to identify:

- component name and version;
- supplier, author, or publisher when known;
- dependency relationships;
- hashes or other identity material for artifacts;
- declared licenses or licensing expressions;
- package URLs, CPEs, or other machine-matchable identifiers;
- build or release context; and
- completeness notes when the generator knows the data is partial.

Modern formats differ in emphasis. SPDX grew out of license and compliance
exchange and is excellent for package identity, licensing, and relationships.
CycloneDX is widely used in security and supply-chain workflows and has strong
support for services, vulnerabilities, formulations, and related operational
metadata. Neither format saves you if the source data is wrong.

## How SBoMs Are Made

There is no single universal generation method. Real-world SBoMs usually come
from one or more of these approaches:

### Package-Manager Extraction

Tools read manifests and lockfiles such as `package-lock.json`, `poetry.lock`,
`Cargo.lock`, `go.sum`, or `pom.xml`. This is often the fastest way to get
high-confidence direct and transitive dependency data for managed ecosystems.
The weakness is that it may miss vendored code, build-time downloads, runtime
plug-ins, or manually copied source.

### Build-System Or Build-Pipeline Emission

The build itself emits component metadata as artifacts are resolved and
assembled. This can be more accurate for shipped outputs because it reflects
what the build actually used rather than what a manifest merely declared.
The weakness is that it depends on the build being reproducible and instrumented.

### Source And Repository Scanning

Scanners inspect source trees for package manifests, license files, vendored
code, and known fingerprints. This helps catch copied libraries or embedded
third-party code that a package manager never saw. The weakness is ambiguity:
source scanners can misidentify versions, overcount copied files, or miss
generated and fetched artifacts.

### Binary And Container Scanning

Tools inspect compiled artifacts, images, and deployed packages. This is
especially valuable when the build system is unavailable or the runtime image
contains more than the source repository suggests. The weakness is reduced
context: binary scanners may know that a library is present without knowing
why, how it was built, or whether the shipped version matches source control.

### Manual Augmentation

Good SBoM programs often need a human-maintained layer for items tools miss:
commercial components, private forks, firmware blobs, fonts, ML assets, or
embedded third-party code copied directly into the repo. Pure automation is
rarely complete.

## Why Multiple Generators Often Matter

The mature pattern is not "pick one scanner and trust it forever." It is:

- generate from the build or package manager for authoritative dependency
  resolution;
- scan the source tree or artifact for drift and copied code; and
- compare the results for gaps.

When two generators disagree, that is usually a useful audit event rather than
noise. One tool may have found a vendored library. Another may have found a
dependency that the final image no longer ships. Reconcile the difference
instead of averaging it away.

## What SBoM Auditing Actually Does

SBoM auditing is the work of interrogating the inventory, not just storing it.
The major audit modes are:

### License Audit

Match each component's declared or detected license to the organization's
policy. This is where you flag GPL-family, AGPL, SSPL, BUSL, custom EULAs, or
unknown licenses. A good audit also checks for package-level dual licensing,
missing license files, and component-specific exceptions.

This is where the knacks in `knacks/licenses/` become useful. The SBoM tells
you what licenses are present. The license knacks help you understand what
those licenses mean for the actual distribution or service model.

### Vulnerability Audit

Map components to vulnerability data through CPEs, package URLs, vendor
advisories, and ecosystem-specific identifiers. The hard part is not just
matching CVEs. It is confirming whether the affected component, version, build
option, and reachable code path actually apply to your shipped artifact.

This is why VEX and exploitability context matter. A raw SBoM can tell you
what might be present. It cannot, by itself, tell you whether a CVE is
reachable, exploitable, patched downstream, or irrelevant in your deployment.

### Provenance And Change Audit

Compare SBoMs over time. New component? Version drift? Supplier change?
Unexpected dependency added by a transitive update? These questions matter for
release review, procurement, and incident response.

### Completeness Audit

Ask what is missing:

- Are build-time dependencies absent?
- Are dynamically loaded plug-ins missing?
- Did the scanner omit private packages?
- Are container base-image components represented?
- Are non-code artifacts with separate licenses missing?

An SBoM with no completeness review can create false confidence.

## Common Failure Modes

- Treating an SBoM as complete because a tool produced a nice JSON file.
- Shipping an SBoM that reflects the source repo but not the final container
  or installer image.
- Ignoring vendored or copied third-party code because it bypassed package
  managers.
- Recording unknown or custom licenses without escalation.
- Expecting CVE feeds to match perfectly when identifiers are weak or absent.
- Failing to preserve the SBoM alongside the exact release artifact it
  describes.

Another frequent failure is version drift between build and audit. If the SBoM
was generated before the final dependency resolution, image layering, or
release signing step, the document may describe a build that never shipped.

## Practical Review Checklist

- Define the scope first: source tree, build output, container image,
  deployed service, or procurement target.
- Record how the SBoM was generated and by which toolchain.
- Prefer at least one generation path tied to the actual build output.
- Compare automated output with manual knowledge of vendored and commercial
  components.
- Normalize identifiers where possible: SPDX expressions, package URLs, CPEs,
  hashes, and supplier data.
- Store the SBoM with or near the release artifact it describes.
- Re-audit when the dependency graph, build system, or packaging model
  changes.

## Further Information

- CISA SBOM resources: <https://www.cisa.gov/sbom>
- NTIA SBOM minimum elements:
  <https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom>
- SPDX specification: <https://spdx.dev/specifications/>
- CycloneDX specification overview:
  <https://cyclonedx.org/specification/overview/>
- CISA SBOM consumption guide:
  <https://www.cisa.gov/resources-tools/resources/securing-software-supply-chain-recommended-practices-software-bill-materials-consumption>
