# AI Director 中文版

从 skills 仓库根目录执行。

```sh
codex plugin marketplace add "$PWD/plugin/chatgpt-plugin-cn"
codex plugin add ai-director-cn@giggle-chatgpt-cn
```

插件的可移植清单 `mcp.json` 只声明服务地址和传输类型，以兼容本机客户端的服务发现。MCP 服务通过 OAuth 保护，目前使用预注册客户端。

- **Codex / ChatGPT 桌面版 Codex**：如果插件没有弹出授权，按 [MCP 直连指南](https://director.ggltest.com/cli/guide#mcp) 配置 `director-local`、`director:mcp` 和 `http://127.0.0.1:8765/callback`，再执行 `codex mcp login giggle-director`。使用直连时只保留一条启用的连接，避免重复工具。
- **ChatGPT / Work 手动接入**：按 [ChatGPT 接入指南](https://director.ggltest.com/cli/guide#plugin) 添加自定义 MCP，选择 OAuth 自定义客户端 `director-chatgpt`、Token 端点身份验证方式 `none`、权限范围 `director:mcp` 和 PKCE S256。后端需登记客户端显示的完整 OAuth 回调。

在客户端打开 AI Director，按连接提示登录 Giggle。先让它「列出我可用的模型和可编辑画布，不生成内容」。付费生成先选画布和报价，确认后提交，通过原任务 ID 查询结果。

测试环境 MCP 地址为 `https://director.ggltest.com/mcp`。同一客户端启用一个语言版本即可。
