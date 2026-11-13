# AI Director English

Run these commands from the skills repository root.

```sh
codex plugin marketplace add "$PWD/plugin/chatgpt-plugin-en"
codex plugin add ai-director-en@giggle-chatgpt-en
```

The portable `mcp.json` declares the server URL and transport for local client discovery. The MCP server uses OAuth with pre-registered clients.

- **Codex / Codex in ChatGPT desktop**: If the plugin does not prompt for authorization, follow the [direct MCP guide](https://director.ggltest.com/cli/guide#mcp) to configure `director-local`, `director:mcp`, and `http://127.0.0.1:8765/callback`, then run `codex mcp login giggle-director`. Keep one connection enabled to avoid duplicate tools.
- **ChatGPT / Work manual setup**: Follow the [ChatGPT setup guide](https://director.ggltest.com/cli/guide#plugin) to add a custom MCP server. Use the OAuth client `director-chatgpt`, token endpoint auth method `none`, scope `director:mcp`, and PKCE S256. Register the exact callback URL shown by the client.

Open AI Director in the client and follow its Giggle OAuth prompt. Start by asking it to list available models and editable canvases without generating anything. For paid generation, select a canvas, review the estimate, confirm, then track the returned task ID.

Both language editions use the same staging MCP at `https://director.ggltest.com/mcp`. Enable one edition per client.
