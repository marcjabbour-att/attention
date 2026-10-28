# Attention submission checklist

## Confirmed in this preparation

- Existing Attention Claude plugin: `https://github.com/attentiontech/attention`.
- Production MCP URL: `https://api.attention.tech/mcp`. An unauthenticated MCP initialize request returned HTTP 401 with an OAuth challenge on 2026-10-28.
- Public OAuth discovery and protected resource metadata are available. Both currently advertise only `mcp:read` and `mcp:write`.
- Attention website, contact page, privacy policy, and terms URLs in the package returned HTTP 200 on 2026-10-28.
- The package has five positive and three negative draft review cases, the counts required for an initial MCP review.
- The domain challenge path returned HTTP 404 on 2026-10-28; this is expected until the portal issues its token and Attention hosts it.
- The OpenAI source overlay builds into the recommended portable `plugin.json` and `mcp.json` format. The generated manifests inherit shared metadata and the MCP connection rather than maintaining duplicate configurations. Use the portal's upload validation as the authoritative package check.

## Attention engineering and account owner actions

1. Verify the Attention business identity in the OpenAI Platform organization and ensure the submitting user has Apps Management Write access.
2. In the OpenAI plugin portal, upload the ZIP, connect the MCP endpoint, and host the portal's exact domain challenge token at `https://api.attention.tech/.well-known/openai-apps-challenge` (or an allowed parent domain). Do not put the token in this package.
3. Decide whether to support OpenAI Enterprise workspace domain restrictions. Current OAuth discovery does not advertise `openid` or `email` or a UserInfo endpoint. OpenAI's guidance calls for those scopes, OIDC discovery, and a UserInfo response with verified email. This requires a server change and may matter for enterprise review.
4. Run the portal tool scan. Every live tool needs accurate `readOnlyHint`, `openWorldHint`, and `destructiveHint` annotations and annotation justifications. Check all 82 tools, especially writes, deletions, and API key management. The package cannot supply or override these server-side values.
5. Provide a seeded, fully featured demo account for reviewers, with login instructions and credentials entered privately in the portal. It must work from outside Attention's network without MFA or expiring verification codes.
6. Rerun the five positive and three negative cases against the demo account in ChatGPT and Codex. Update prompts and expected behavior to identify stable demo records and exact expected results. Record and provide the required reviewer-accessible video walkthrough URL in the portal or manifest.
7. Review Attention's privacy policy against every field returned by the MCP tools, including nested and debug fields. Remove unnecessary personal data, tokens, internal IDs, and logs from tool responses. Confirm support contact and terms are appropriate for this integration.
8. Resolve portal findings, submit for review, and publish only after approval.

## Packaging

From the repository root, run `python3 .openai-plugin/build.py` with Python 3.9 or later. This validates and creates `.openai-plugin/dist/attention-openai-<version>.zip`, inheriting the version from `.claude-plugin/plugin.json` (currently `1.1.0`). The ZIP contains the generated portable manifests, unchanged shared skills and license, and the OpenAI icon.

Only fields that differ for OpenAI are stored in `manifest-overlay.json`. Package identity, author, version, repository, license, and keywords come from `.claude-plugin/plugin.json`; the MCP URL and connection settings come from `.mcp.json`. The builder translates the HTTP transport name to `streamable-http` for the portable MCP format. All shared skill files and supporting resources are copied into the package.

The repository's `.openai-plugin/` directory is an authoring layout. It is not a recognized OpenAI plugin root; distribute the generated ZIP with `plugin.json`, `mcp.json`, and `skills/` at its root. To choose an output directory, pass `--output-dir <directory>` to the build command.

## Sources

- [OpenAI submission flow](https://developers.openai.com/plugins/deploy/submission)
- [OpenAI MCP review requirements](https://developers.openai.com/plugins/deploy/app-review)
- [OpenAI submission errors](https://developers.openai.com/plugins/deploy/submission-errors)
- [OpenAI authentication requirements](https://developers.openai.com/plugins/build/auth)
- [Attention MCP overview](https://docs.attention.com/mcp/overview)
