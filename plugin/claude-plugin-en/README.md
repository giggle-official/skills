# AI Director English

Run these commands from the skills repository root.

```sh
claude plugin marketplace add "$PWD/plugin/claude-plugin-en"
claude plugin install ai-director-en@giggle-claude-en
```

In Claude Code, open `/mcp` and connect `giggle-director`. Claude Code discovers the OAuth registration endpoint, registers a client and selects a local callback port before opening Giggle authorization in your browser. Update an older plugin before reconnecting. To connect from Claude on the web, Claude Desktop, or Cowork, add the remote MCP URL below as a custom connector and choose automatic registration in the OAuth client settings.

Open AI Director in the client and follow its Giggle OAuth prompt. Start by asking it to list available models and editable canvases without generating anything. For paid generation, select a canvas, review the estimate, confirm, then track the returned task ID.

Both language editions use the same staging MCP at `https://director.ggltest.com/mcp`. Enable one edition per client.
