# Giggle AI 导演 · DeepSeek Harness

将 Giggle AI Director 接到 DeepSeek Harness，复用同一套模型目录、画布、积分预估和生成工具。插件默认连接测试环境的 `https://director.ggltest.com/mcp`，支持 DeepSeek Harness `0.2.1-rc.5` 及其兼容版本。

## 安装

从 [Giggle skills 仓库](https://github.com/giggle-official/skills) 获取 `main`，在 DeepSeek Harness 的**创造模式**中，把当前工作区的 `plugin/deepseek-harness-plugin-cn` 绝对路径交给插件管理器的 `install_bundle`。也可以通过「插件 → 添加插件 → 安装第三方插件」选择该目录。若应用提示需要重启，请重启后再继续。

可以直接把下面这段发给 Harness：

> 请在当前工作区获取 https://github.com/giggle-official/skills 的 main 分支，用插件管理器的 install_bundle 安装 plugin/deepseek-harness-plugin-cn 的绝对路径。安装后用 giggle_connection_status（authorize=true）引导我完成 Giggle 账户授权，再开一个新会话，查询可用模型和当前团队的画布。请只查询，不发起付费生成。

本包可从检出的目录安装，也可以用 `npm pack` 生成安装用 tarball。无需发布到 npm，也没有构建脚本。安装时由 Harness 处理依赖和 profile。

## 授权和验证

1. 在新会话中用 `giggle_connection_status` 的 `authorize=true` 获取授权链接，在浏览器登录 Giggle 并确认。OAuth 使用本机回环回调，凭证由 Harness 的凭证存储保管。
2. 新开会话运行 `giggle_connection_status`，再让 Agent 调用 `mcp__giggle_director__list_models` 和 `mcp__giggle_director__list_canvases`。这两个工具只读。
3. 确认连接后，可以用自然语言提出生成需求。生成前先估价并确认，随后用原任务 ID 查询结果。

如需连接其他部署，在插件行配置设置 `mcpUrl` 为该环境的 HTTPS MCP 地址。该部署需启用 OAuth 动态注册并公开发现元数据。

建议提交信息为 `feat(plugins): add DeepSeek Harness bundle for Giggle AI Director`。
