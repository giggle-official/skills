# AI Director 中文版

从 skills 仓库根目录执行。

```sh
claude plugin marketplace add "$PWD/plugin/claude-plugin-cn"
claude plugin install ai-director-cn@giggle-claude-cn
```

Claude Code 在 `/mcp` 中选择 `giggle-director` 并连接。客户端会发现 OAuth 动态注册端点、自动注册并选择本机回调端口，再打开浏览器完成 Giggle 授权。已安装旧版时，请先更新插件，再重新连接。Claude 网页端、Desktop 和 Cowork 的远程连接器可单独添加下方 MCP 地址，并在 OAuth 客户端设置中选择自动注册。

在客户端打开 AI Director，按连接提示登录 Giggle。先让它「列出我可用的模型和可编辑画布，不生成内容」。付费生成先选画布和报价，确认后提交，通过原任务 ID 查询结果。

MCP 地址为 `https://director.ggltest.com/mcp`。中英文版本共用该测试环境，同一客户端启用一个版本即可。
