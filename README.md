# Secure Software by Design

[العربية](README.ar.md) · [Skill](skills/secure-software-by-design/SKILL.md) · [MIT License](LICENSE)

A portable [Agent Skill](https://agentskills.io/specification) for defensive software design, implementation, review, and verification. It routes agents to focused guidance for the trust boundaries that actually change, from a bounded fix to an architecture review or staged brownfield rollout.

## Install

Copy the **whole** `skills/secure-software-by-design/` directory into one discovery directory in the **target application**. Keep the folder name and its internal paths unchanged. Do not copy only `SKILL.md`.

| Agent | Place the skill under |
|---|---|
| [OpenAI Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) | `.agents/skills/` |
| [Claude Code](https://code.claude.com/docs/en/skills#choose-where-skills-load) | `.claude/skills/` |
| [GitHub Copilot](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) | `.github/skills/` or `.agents/skills/` on supported clients |
| [Cursor](https://cursor.com/docs/skills) | `.cursor/skills/` or `.agents/skills/` |

For a workspace shared by Codex, Cursor, and supported Copilot clients, use one copy under `.agents/skills/`. The table documents project paths, not every product tier or execution environment. If your agent lacks skill discovery, attach the directory or ask it to read `SKILL.md` and its relevant references explicitly.

Example (PowerShell, from the target application root; replace the source path):

```powershell
$skill = 'C:/path/to/checkout/skills/secure-software-by-design'
New-Item -ItemType Directory -Force -Path '.agents/skills' | Out-Null
Copy-Item -LiteralPath $skill -Destination '.agents/skills/' -Recurse
```

Use a fresh destination, or replace a previously installed copy after reviewing your local changes. Native skill discovery does not require MCP or Docker. The optional helpers use Python 3.10+; the diff helper also uses Git, and the registry checker uses HTTPS for reviewed public package names only.

## MCP and Docker

The optional read-only MCP server exposes the bundled guidance over stdio or Streamable HTTP. Use `list_guidelines` to browse topics and `get_guidelines` to read one. The server does not inspect a target repository or run the native verification scripts. See the [MCP and Docker guide](docs/distribution.md) for local setup, client configuration, and OCI distribution.

## Try it

```text
Use the secure-software-by-design skill to review the new record export.
Identify the access rule, verify permitted and denied flows with synthetic
fixtures, and report evidence, unverified checks, and remaining risks.
```

## Repository layout

```text
skills/secure-software-by-design/
  SKILL.md       # Portable entrypoint
  agents/        # Optional OpenAI discovery UI metadata
  assets/        # Skill icon
  references/    # Focused defensive guidance and tool documentation
  examples/      # Fictional sample report
  scripts/       # Diff scanner and public registry metadata checker
tests/           # Packaging, helper, and optional MCP integration tests
.github/         # Skill and MCP/Docker validation workflows
server.py        # Read-only MCP adapter
Dockerfile       # Build the optional MCP container
```

## Validate locally

From the repository root, with Git and Python 3.10 or later:

```sh
python -B -m unittest discover -s tests -v
```

The tests cover the packaged structure and local links, defensive helper behavior, synthetic Git diffs, and mocked registry responses. Passing tests do not demonstrate live registry access, integration with every agent runtime, or the security of a target application.

To exercise the MCP and Docker integration tests, follow the [verification steps](docs/distribution.md#verify-or-update).
