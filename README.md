# Attention Plugin

Plugin for Claude Code, Grok Build, ChatGPT, and Codex that connects your assistant to [Attention](https://www.attention.com) — an AI-powered conversational intelligence platform that records calls, transcribes, and analyzes sales conversations.

## What's Included

This plugin provides:

- **MCP Server Connection** — Connects to Attention's remote MCP server at `https://api.attention.tech/mcp` with OAuth 2.0 authentication
- **Skills** — Agent skills for searching conversations and getting AI-powered insights

Claude and Grok use `.claude-plugin/plugin.json` with `.mcp.json`. The OpenAI build reuses their package metadata, version, MCP connection, and `skills/` directory. Only OpenAI-specific metadata, assets, documentation, and build tooling live in `.openai-plugin/`.

## Installation

### Claude Code: official marketplace

```
/plugin install attention
```

### Claude Code: local testing

```bash
claude --plugin-dir ./path/to/attention
```

Then authenticate:

```
/mcp
```

Select "attention" and complete the OAuth flow in your browser.

### Grok Build

In Grok Build, open `/plugin`, search for **Attention**, and install. On first connect, sign in with your Attention account to complete the OAuth flow in your browser.

Grok Build reads the same plugin files as Claude Code (`.claude-plugin/plugin.json`, `.mcp.json`, `skills/`), so there's nothing extra to configure.

### ChatGPT and Codex

Build the portable package with Python 3.9 or later:

```bash
python3 .openai-plugin/build.py
```

This creates `.openai-plugin/dist/attention-openai-<version>.zip`, using the version from `.claude-plugin/plugin.json`. The ZIP contains root-level `plugin.json` and `mcp.json`, the unchanged shared skills and license, and the OpenAI icon. The builder converts the shared MCP transport from `http` to the portable name `streamable-http`; its endpoint and other connection settings come from `.mcp.json`.

`.openai-plugin/` is the source overlay, not an installable plugin root: [OpenAI's package format](https://developers.openai.com/plugins/build/plugins) requires the generated manifests at the package root. Build the ZIP instead of uploading this repository or the overlay folder directly.

For public distribution, upload the generated ZIP in the [OpenAI plugin portal](https://platform.openai.com/apps-manage), connect and scan the remote MCP server, and complete the review. The [OpenAI submission checklist](.openai-plugin/SUBMISSION.md) records the remaining Attention account and server requirements. Building the ZIP alone does not publish or install the plugin.

## Available MCP Tools

Tools are discovered dynamically from the server at connection time. Run `/mcp` in Claude Code to see all available tools, or check the [Attention MCP Server Docs](https://docs.attention.com/mcp/overview) for the full reference.

## Plugin Structure

```
attention/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (name, version, metadata)
├── .mcp.json                # MCP server configuration (remote HTTP)
├── .openai-plugin/
│   ├── manifest-overlay.json # OpenAI presentation and review metadata
│   ├── assets/
│   │   └── attention-icon.png
│   ├── build.py              # Generates the portable ZIP from shared sources
│   └── SUBMISSION.md
├── skills/
│   └── conversations/
│       └── SKILL.md         # Shared conversation skill
└── README.md
```

## Testing

1. **Local testing with `--plugin-dir`**:
   ```bash
   claude --plugin-dir ./attention
   ```

2. **Verify plugin loaded**:
   ```
   /help
   ```
   You should see `attention:conversations` in the skills list.

3. **Authenticate**:
   ```
   /mcp
   ```
   Select "attention" and complete OAuth in your browser.

4. **Test tools**:
   ```
   Search for conversations from last week
   ```

5. **Validate plugin structure**:
   ```bash
   claude plugin validate ./attention
   ```

6. **Build the OpenAI package**:
   ```bash
   python3 .openai-plugin/build.py
   ```
   Inspect the generated ZIP for `plugin.json`, `mcp.json`, `skills/conversations/SKILL.md`, `assets/attention-icon.png`, and `LICENSE`. After connecting the package in ChatGPT or Codex, complete Attention OAuth and try `Search for conversations from last week`. Authenticated tool discovery and calls require an Attention account.

## Server Details

| Property | Value |
|----------|-------|
| Server URL | `https://api.attention.tech/mcp` |
| Transport | Streamable HTTP (stateless) |
| Authentication | OAuth 2.0 with PKCE |
| Scopes | `mcp:read`, `mcp:write` |
| OAuth Discovery | `https://api.attention.tech/.well-known/oauth-authorization-server` |

The plugin only talks to `api.attention.tech`. It needs no API key and reads no local files or environment variables: you sign in with your Attention account and the agent acts as that account (scopes `mcp:read`, `mcp:write`).

## Documentation

- [Attention MCP Server Docs](https://docs.attention.com/mcp/overview)
- [Claude Code Plugins Docs](https://code.claude.com/docs/en/plugins)
- [xAI Plugin Marketplace](https://github.com/xai-org/plugin-marketplace)
- [MCP Specification](https://modelcontextprotocol.io/)
