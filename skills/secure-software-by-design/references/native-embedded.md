# Runtime, native, mobile, and embedded concerns

Read only when this domain intersects the scoped change. Every applicable control is mandatory; verify implementation and negative cases.

- **MUST** For memory-unsafe code, review bounds, lifetimes, ownership, integer arithmetic, format strings, type confusion, and use-after-free; use compiler hardening, sanitizers, and fuzzing where practical.
- **MUST** Restrict OS capabilities, filesystem permissions, process privileges, IPC, dynamic library search paths, and sandbox escape opportunities.
- **MUST** For mobile/desktop, review secure local storage, deep links, exported components, IPC, update validation, and credential handling. Do not rely on obscurity or client-side checks to enforce server authorization.
- **MUST** For embedded/firmware, review secure update/boot where supported, debug interfaces, device identity, physical-access assumptions, and recovery paths. Document platform limitations explicitly.
