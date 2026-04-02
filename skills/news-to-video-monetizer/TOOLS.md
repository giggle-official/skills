# TOOLS.md - 环境配置备忘

## X2C API

- Base URL: `https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api`
- 认证: Header `X-API-Key: <your_api_key>`
- 文档: 见 `~/.openclaw/skills/storyclaw-x2c-ai-director/references/X2C-OPEN-API.md`

## DailyHot API

- 地址: `http://localhost:6688`
- 启动: `cd ~/.openclaw/skills/dailyhot-api && bash scripts/ensure_running.sh`
- 停止: `cd ~/.openclaw/skills/dailyhot-api && bash scripts/stop.sh`

## 霸总甜宠分类 ID

- Category UUID: `4eb7e8ca-1510-4e5a-83e2-c12a9e033a78`
- 其他分类可通过 `distribution/categories` API 查询

## 已知限制

- 微博和快手的 DailyHot 接口偶尔返回 500 错误（不影响整体采集）
- 视频渲染在 shot 阶段偶尔失败，属于 X2C 上游问题，重试通常成功
- ffmpeg 未安装时无法本地处理视频（本 agent 不需要，视频在云端）
