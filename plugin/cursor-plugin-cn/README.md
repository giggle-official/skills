# Giggle AI Director 中文版 · Cursor

在 Cursor 通过 Giggle AI Director 查询模型和画布，生成图片、视频和音频，并把结果保存到画布。

## 本地安装

1. 获取 [giggle-official/skills](https://github.com/giggle-official/skills) 仓库的 `main` 分支，找到 `plugin/cursor-plugin-cn`。
2. 将目录复制到 `~/.cursor/plugins/local/giggle-ai-director-cn`。复制后，清单应位于 `~/.cursor/plugins/local/giggle-ai-director-cn/.cursor-plugin/plugin.json`。已安装时直接更新这个目录。
3. 在 Cursor 执行 **Developer: Reload Window** 或重启。打开 **Customize → Plugins** 确认插件已加载。
4. 打开 **Customize → MCPs**，启用 `giggle-director`，按界面提示完成 Giggle 账户授权。
5. 在新对话中查询可用模型和当前团队的画布，确认连接。首次检查只需 `list_models` 和 `list_canvases`。

[Cursor 官方本地插件安装说明](https://cursor.com/docs/plugins#test-plugins-locally)

## 服务地址与授权

默认的 MCP 地址是测试环境的 `https://director.ggltest.com/mcp`。使用其他环境时，修改本地插件副本中的 `mcp.json` 并重载 Cursor。

Cursor 使用服务端公布的 OAuth 动态注册地址完成授权。部署方需要启用 MCP，确保 `/oauth/register` 可达，并运行支持 Cursor 回调的后端版本。
