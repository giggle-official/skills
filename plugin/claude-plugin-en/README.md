# AI Director English

Run these commands from the skills repository root.

```sh
claude plugin marketplace add "$PWD/plugin/claude-plugin-en"
claude plugin install ai-director-en@giggle-claude-en
```

In Claude Code, use `/mcp` to connect. Pre-register `director-claude-code` with `http://localhost:8766/callback` or the exact callback the client sends. In Claude Desktop/Cowork, use the native plugin and connector controls. Register the actual callback separately for cloud connectors.

Open AI Director in the client and follow its Giggle OAuth prompt. Start by asking it to list available models and editable canvases without generating anything. For paid generation, select a canvas, review the estimate, confirm, then track the returned task ID.

Both language editions use the same staging MCP at `https://director.ggltest.com/mcp`. Enable one edition per client.
