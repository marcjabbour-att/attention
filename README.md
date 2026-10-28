# Attention Plugin

Plugin for Claude Code, Grok Build, ChatGPT, and Codex that connects your assistant to [Attention](https://www.attention.com) — an AI-powered conversational intelligence platform that records calls, transcribes, and analyzes sales conversations.

## What's Included

This plugin provides:

- **MCP Server Connection** — Connects to Attention's remote MCP server at `https://api.attention.tech/mcp` with OAuth 2.0 authentication
- **Skills** — Agent skills for searching conversations and getting AI-powered insights

Claude and Grok use `.claude-plugin/plugin.json` with `.mcp.json`. ChatGPT and Codex use the portable `plugin.json` with `mcp.json`. Both packages share `skills/conversations/SKILL.md` and connect to the same production MCP endpoint.

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

Run `python3 scripts/build_openai_plugin.py` from this repository to create a ZIP under `dist/`. Upload that ZIP in the [OpenAI plugin portal](https://platform.openai.com/apps-manage), connect and scan the remote MCP server, and complete the review. The [OpenAI submission checklist](docs/OPENAI_SUBMISSION.md) records the remaining Attention account and server requirements. Public approval requires OpenAI review; building the ZIP alone does not publish the plugin.

## Available MCP Tools

Tools are discovered dynamically from the server at connection time. Run `/mcp` in Claude Code to see all available tools, or check the [Attention MCP Server Docs](https://docs.attention.com/mcp/overview) for the full reference.

## Plugin Structure

```
attention/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (name, version, metadata)
├── .mcp.json                # MCP server configuration (remote HTTP)
├── plugin.json              # OpenAI portable manifest and listing
├── mcp.json                 # OpenAI portable MCP configuration
├── assets/
│   └── attention-icon.png  # OpenAI listing icon
├── skills/
│   └── conversations/
│       └── SKILL.md         # Shared conversation skill
├── scripts/
│   └── build_openai_plugin.py
├── docs/
│   └── OPENAI_SUBMISSION.md
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
