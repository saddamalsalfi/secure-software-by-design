# Files, uploads, and parsers

Read only when this domain intersects the scoped change. Every applicable control is mandatory; verify implementation and negative cases.

- **MUST** Constrain filenames and paths; prevent traversal, symlink escapes, unsafe extraction, arbitrary overwrite, and insecure temporary files. Prefer race-resistant filesystem APIs and verify confinement at the actual operation.
- **MUST** Limit file count, size, expanded archive size, compression ratio, parse complexity, and processing time. Check actual content as well as declared MIME/extension.
- **MUST** Store uploads outside executable/public application paths by default; generate server-controlled names; authorize downloads; serve with safe content types and dispositions. Use quarantine/scanning where justified, without treating scanning as proof of safety.
- **MUST** Sandbox risky document/media processing; use least-privileged workers and maintained parsers. Avoid parsing untrusted native object formats.

## Processing isolation
- **MUST** restrict parser network access, filesystem access, and resources. VERIFY failures do not leave executable, public, or unauthorized artifacts.
