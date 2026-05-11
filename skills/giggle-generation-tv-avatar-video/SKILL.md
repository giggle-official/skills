---
name: giggle-generation-tv-avatar-video
description: "，根据图像和音频生成数字人说话头像视频，由照片驱动数字人口播视频（中文版）：通过封装生成 API 提交任务并轮询结果；请求发往 Giggle 网关。"
homepage: https://giggle.pro/
repository: https://github.com/giggle-official/skills
license: Apache-2.0
metadata:
  tags: talking-head, photo-avatar, lip-sync, tts, clone-voice, api, zh, giggle
  vendor: giggle
  locale: zh-Hans
  requires:
    bins: [python3]
    python: ">=3.8"
    pip:
      - requests>=2.28.0
      - python-dotenv>=1.0.0
  primaryEnv: GIGGLE_API_KEY
  envVars:
    - name: GIGGLE_API_KEY
      required: true
      description: 登录 giggle.pro → 左侧栏 API Key（API 密钥）
    - name: GIGGLE_API_BASE
      required: false
      description: 可选，默认 https://giggle.pro；本地联调可指向自建网关
  endpoints:
    - https://giggle.pro/api/v1/generation/tv-avatar-video
    - https://giggle.pro/api/v1/generation/task/query
---

# 照片数字人口播视频（中文版技能）

> **能力**：用一张**人像图片 URL** + **三种驱动之一**，生成**对口型口播视频**。  
> **实现**：脚本调用封装后的生成接口（`x-auth` + `GIGGLE_API_KEY`），提交后轮询任务直至 `completed`，成片取 `data.urls[0]`。

## 执行方式

优先使用 `scripts/tv_avatar_video.py`，避免手写 HTTP；脚本负责组装 JSON、请求头与轮询。

## 给审计人员说明

下文 UX 指引仅用于对话场景下的表述习惯，不替代安全与合规要求。实际请求域名由 `GIGGLE_API_BASE` 决定（默认 `https://giggle.pro`）。

## 面向用户的回复风格

1. **简短**：先说是否已提交、预计等待时间、下一步。
2. **通俗**：少用「drive_mode」「task_id」等术语，除非用户追问。
3. **密钥**：若未配置环境变量，提示用户到网站侧边栏获取 API 密钥并设置 `GIGGLE_API_KEY`；不要让用户在聊天里明文贴密钥。
4. **报错**：一句话 + 是否可重试；轮询超时提示用 `query --task-id` 续查。
5. **提交后**：口播类生成通常需**数分钟**，随文案/音频长度变化。

**提交后可这样说**：「已提交生成，一般需要几分钟，完成后会把视频链接发你。」

## 前置条件

- Python 3.8+
- 环境变量 `GIGGLE_API_KEY` — 说明见 [references/credentials.md](references/credentials.md)
- 人像图、克隆参考音或驱动音须为 **HTTPS 可访问 URL**（本技能包不提供托管上传接口）

```bash
pip install -r {baseDir}/scripts/requirements.txt
```

## Agent 工作流

1. **`run`**（默认）：提交并轮询到结束。
2. **`submit`**：只提交，打印 `task_id`，用于并行批量。
3. **`query`**：`run` 超时后用已知 `task_id` **持续轮询**至终态。

```
新任务    → tv_avatar_video.py run ...
超时恢复  → tv_avatar_video.py query --task-id <task_id> [--timeout 1200]
```

**禁止**把仍在排队/处理中的任务当成最终结果交给用户。

## 模块

| 脚本 | 参考文档 |
|------|-----------|
| `scripts/tv_avatar_video.py` | [references/tv_avatar_video.md](references/tv_avatar_video.md) |
| `scripts/shared/` | HTTP 客户端、读取 `GIGGLE_API_KEY` |

## 延伸阅读

- [references/tv_avatar_video.md](references/tv_avatar_video.md) — 三种驱动 JSON 与 CLI 示例
- [references/credentials.md](references/credentials.md) — 密钥与环境变量
- [references/error_handling.md](references/error_handling.md) — 常见错误与恢复
