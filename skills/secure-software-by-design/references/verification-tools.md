# Deterministic verification helpers

Use Python 3.10+ standard library. In PowerShell use python instead of python3 if needed, and set the shell variables as appropriate. Resolve SKILL_ROOT to this installed skill folder and PROJECT to the authorized repository. Never execute repository scripts merely to inspect changes. These helpers do not install dependencies or execute application code.

## Added-line secret scan

```bash
python3 "$SKILL_ROOT/scripts/scan_diff_secrets.py" --repo "$PROJECT" --include-untracked
python3 "$SKILL_ROOT/scripts/scan_diff_secrets.py" --repo "$PROJECT" --base HEAD~1 --include-untracked
```

Default scans staged and unstaged diffs separately. --base compares the specified commit to working tree (not a merge-base). Explicitly choose the intended comparison and report it. --include-untracked includes nonignored regular UTF-8 files. New destinations of tracked renames are scanned as additions. Ignored files, historical commits, deleted lines, unchanged tracked content, and external secret stores are outside coverage. Binary/non-UTF-8/oversized inputs produce incomplete results. Empty diff is not a repository-wide scan.

JSON includes path, line, and rule, never matched values or snippets. Filenames themselves are metadata: inspect for sensitivity before forwarding reports to external systems. Heuristic entropy/key detectors produce false positives and false negatives. They do not validate live credentials, detect every secret format, or replace a mature secret scanner. Review candidates locally without printing their values. Never add blanket suppressions to obtain a clean result.

## Registry metadata check

Compare manifests AND lockfiles against the intended baseline; extract newly introduced package names, including newly resolved transitive dependencies. Review aliases, local/path/git dependencies and private registries separately. The helper intentionally does not infer or discover dependencies. MUST NOT report complete dependency coverage unless extraction has been verified.

Create a reviewed JSON list containing only public names:

```json
[
  {"ecosystem":"pypi","name":"requests"},
  {"ecosystem":"npm","name":"@types/node"},
  {"ecosystem":"packagist","name":"symfony/console"}
]
```

```bash
python3 "$SKILL_ROOT/scripts/verify_packages.py" public-packages.json --young-days 90
```

Only use registry requests when sending these package names is authorized. Do not transmit private package names. Requests go to fixed official HTTPS registry origins, reject redirects, omit authentication, disable inherited proxies, and use timeout/body-size limits. No packages are installed. Proxy-only environments may fail: report unknown rather than circumventing network controls.

Results: existence is exists/missing/unknown. Only HTTP 404 means missing; rate limits, timeouts, malformed responses, and identity mismatch are unknown. npm time.created is registry creation. PyPI earliest surviving upload is NOT proven creation; deleted releases can obscure age. Packagist package.time is emitted with that exact semantic label, not asserted to be authoritative creation. Missing dates are unknown and require review. Negative/future ages and recent timestamps trigger review. Existence, age, and exit 0 do NOT establish authenticity, provenance, maintainer reputation, safety, or exact-version integrity. Perform those checks separately using official project associations, ownership history, signatures/attestations where supported, and advisories for the exact version.

## Exit codes and interpretation

| Code | Secret scanner | Registry checker |
|---|---|---|
| 0 | No candidates in the stated scope | Packages exist with no date review flags; trust unassessed |
| 1 | Candidates require review | Missing package or timestamp review flag |
| 2 | Scan incomplete/error | Invalid input or at least one unknown result |

MUST inspect JSON and record limitations. A finding or unknown must not be silently converted to passed. Incomplete coverage takes precedence over candidate findings in exit status. An empty list of packages is invalid input; if there are no new packages, omit registry invocation and report that fact.

## Local regression suite (from the skill repository root)

```bash
python -B -m unittest discover -s tests -v
```

Tests use temporary Git repositories and mocked registry responses. They verify deterministic behavior, redaction, error handling, and date interpretation; they do not prove live registry availability. Do not copy fixture outcomes into project verification reports.
