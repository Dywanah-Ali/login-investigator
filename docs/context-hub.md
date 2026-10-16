# Context Hub setup for Codex

Context Hub `@aisuite/chub` version `0.1.4` is installed globally with npm.
Codex's user MCP configuration registers its `chub-mcp` executable as `chub`.
No installation is required in individual projects.

The global Codex `get-api-docs` skill prefers MCP and falls back to the shared
`chub` CLI. Telemetry and external feedback are disabled through
`CHUB_TELEMETRY=0` and `CHUB_FEEDBACK=0`.

Reload Codex after changing its MCP configuration. Because npm's global location
belongs to the active Node.js installation, changing or removing that Node.js
version may require reinstalling Context Hub and updating the MCP registration.
Moving or deleting this project does not affect the shared installation.

Verified on 16 October 2026 from a temporary directory outside this project:
MCP connection, discovery of five tools, documentation search and document fetch.
The global skill passed the validator. Claude configuration is managed separately.

Upstream: https://github.com/andrewyng/context-hub
