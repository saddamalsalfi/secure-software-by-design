# Dependencies, delivery, and infrastructure

Read only when this domain intersects the scoped change. Every applicable control is mandatory; verify implementation and negative cases.

- **MUST** Inventory direct/transitive dependencies, plugins, images, and external services. Verify supported versions and relevant official advisories for the exact versions in use; assess reachability and exposure.
- **MUST** Use lockfiles, trusted registries, integrity/provenance checks, controlled install scripts, and dependency-confusion defenses appropriate to the ecosystem. Produce an SBOM when warranted.
- **MUST** Protect CI/CD tokens, artifact integrity, branch/release permissions, and untrusted pull-request workflows. Prevent untrusted builds from receiving production secrets.
- **MUST** Apply least privilege to IAM, containers, orchestration, databases, networks, and service identities. Disable debug endpoints, default credentials, unnecessary services, and public storage access.
- **MUST** Review environment separation, metadata-service access, dangling DNS, signed updates, rollback safety, backups and restore verification, monitoring, and incident response.

## Package hallucination and build privacy
- **MUST** verify a new package's exact name, registry identity, existence, provenance, official project association, maintainer continuity/reputation, ownership changes, and release history before installation. Check slopsquatting, typosquatting, dependency confusion, and registry fallback.
- **MUST NOT** install solely because an LLM suggested a package. Existence, age, popularity, and successful installation do not establish trust. If provenance is unresolved, stop introduction of that dependency and use a verified alternative where possible.
- **MUST** run the registry helper on a reviewed list of newly added public packages; see verification-tools.md. Do not send private package names to public registries. Compare manifests and lockfiles to establish completeness; the helper does not extract dependencies or verify trust automatically.
- **MUST** prevent secrets/PII in CI debug logs, shell tracing, artifacts, fixtures, crash dumps, and LLM-assisted build contexts. Secret masking alone misses transformed or fragmented values.
- **MUST** use scoped short-lived build credentials where supported and isolate install scripts from production secrets. VERIFY outputs exclude sensitive fixtures and development credentials.

## Official registry references
Verified documentation on 2026-11-14:
- PyPI JSON API: https://docs.pypi.org/api/json/
- npm package metadata: https://github.com/npm/registry/blob/main/docs/responses/package-metadata.md
- Packagist API: https://packagist.org/apidoc

Registry timestamps have different meanings. PyPI's earliest surviving artifact upload is not proven project creation; deleted releases can change the apparent age. npm time.created identifies registry creation, not continuous trustworthy ownership. Do not substitute package-author-controlled version dates for registry creation. Mark unavailable timestamps unknown. No age threshold proves authenticity.
