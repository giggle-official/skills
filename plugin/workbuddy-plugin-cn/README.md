# Giggle AI Director · WorkBuddy

通过 WorkBuddy 云端 OAuth 连接 Giggle AI Director。连接后可以查询模型和画布，生成图片、视频或音频，并把结果写回 AI Director 画布。

## 打包和发布

使用 WorkBuddy 4.24.0 或更高版本。将以下文件打成一个 ZIP，使两个 JSON 文件位于压缩包根目录：

```sh
cd plugin/workbuddy-plugin-cn
zip -X /tmp/giggle-director-workbuddy.zip connector-meta.json mcp.json icon.svg skills/*/SKILL.md
```

1. 以连接器开发者身份在 [WorkBuddy 开放平台](https://open.workbuddy.cn/docs/connector) 提交 ZIP，选择 MCP 连接器。
2. 确认 Giggle 后端开放 OAuth 发现、`/oauth/register`、`/oauth/authorize`、`/oauth/token` 和 `/mcp`，并已部署支持 WorkBuddy 回调的版本。测试端点需要能从 WorkBuddy 云端通过 HTTPS 访问。
3. 审核通过并发布后，将 WorkBuddy 提供的安装页 HTTPS 地址填入 Web 的 `MCP_WORKBUDDY_PLUGIN_URL`。

默认端点是生产环境的 `https://giggle.pro/mcp`。部署到其他环境时，同时替换 `mcp.json` 中的 `url` 和 `connector-meta.json` 中的 `server_url`。WorkBuddy 动态生成 OAuth 客户端信息，插件包无需填写客户端 ID、密钥或回调地址。

## 验收

从已发布连接器的安装页打开 WorkBuddy，安装后点击「连接」，在浏览器完成 Giggle 授权。新建对话，先运行 `list_models` 和 `list_canvases` 验证可用性。生成前通过 `estimate_price` 确认费用，提交后用原任务 ID 查询结果。
