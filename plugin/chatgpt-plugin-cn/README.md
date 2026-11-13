# AI Director 中文版

从 skills 仓库根目录执行。

```sh
codex plugin marketplace add "$PWD/plugin/chatgpt-plugin-cn"
codex plugin add ai-director-cn@giggle-chatgpt-cn
```

ChatGPT 桌面 Work 可将 `plugins/ai-director` 下的 `plugin.json`、`mcp.json`、`skills/` 和 `assets/` 打包上传。Work 使用 `director-chatgpt`，后端需登记客户端显示的完整 OAuth 回调。Codex 使用 `director-local` 和 `http://127.0.0.1:8765/callback`。

在客户端打开 AI Director，按连接提示登录 Giggle。先让它「列出我可用的模型和可编辑画布，不生成内容」。付费生成先选画布和报价，确认后提交，通过原任务 ID 查询结果。

测试环境 MCP 地址为 `https://director.ggltest.com/mcp`。同一客户端启用一个语言版本即可。

## 2026-11-13 本地联调变更记录

- 中文版两份 MCP 清单统一到本机服务和 `director-local`，与已安装的本地副本一致。
- 发现接口和前端授权页返回 200；未认证 MCP 返回 401 并提供发现头。
- 使用现有授权只读调用 list_models / list_canvases，返回 57 条模型记录、2 个画布；未重新执行浏览器登录、未生成内容。
- 建议提交信息：`fix(plugin): point Chinese plugin to local MCP for testing`。
