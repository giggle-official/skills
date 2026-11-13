# AI Director 中文版

从 skills 仓库根目录执行。

```sh
claude plugin marketplace add "$PWD/plugin/claude-plugin-cn"
claude plugin install ai-director-cn@giggle-claude-cn
```

Claude Code 在 `/mcp` 完成连接。后端需预注册 `director-claude-code`，默认回调为 `http://localhost:8766/callback`，以客户端实际值为准。Claude Desktop/Cowork 使用客户端插件和连接器入口，云端连接器需单独登记实际回调。

在客户端打开 AI Director，按连接提示登录 Giggle。先让它「列出我可用的模型和可编辑画布，不生成内容」。付费生成先选画布和报价，确认后提交，通过原任务 ID 查询结果。

MCP 地址为 `https://director.ggltest.com/mcp`。中英文版本共用该测试环境，同一客户端启用一个版本即可。
