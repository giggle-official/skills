# AI Director English

Run these commands from the skills repository root.

```sh
codex plugin marketplace add "$PWD/plugin/chatgpt-plugin-en"
codex plugin add ai-director-en@giggle-chatgpt-en
```

For ChatGPT desktop Work, package the portable files from `plugins/ai-director`: `plugin.json`, `mcp.json`, `skills/`, and `assets/`. Local Codex uses `director-local` with `http://127.0.0.1:8765/callback`. Work uses `director-chatgpt`; register the exact callback shown by the client.

Open AI Director in the client and follow its Giggle OAuth prompt. Start by asking it to list available models and editable canvases without generating anything. For paid generation, select a canvas, review the estimate, confirm, then track the returned task ID.

Both language editions use the same staging MCP at `https://director.ggltest.com/mcp`. Enable one edition per client.
