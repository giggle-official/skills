---
name: hopsapi-minimax-h3
description: >
  Use when the user wants MiniMax-H3 video via HopsAPI (storyclaw-token-gateway): text-to-video,
  image-to-video / first-last frames, or omni reference. Resolutions 480p/768p (default 768p),
  duration 4–15s (default 5). Triggers: MiniMax-H3, MiniMax H3, hopsapi video, 文生视频, 首尾帧,
  全能参考, omni video, 768p.
version: "1.0.0"
license: MIT
author: giggle-official
homepage: https://github.com/giggle-official/skills
repository: https://github.com/giggle-official/skills
requires:
  bins: [python3]
  env: [HOPSAPI_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "🎞️",
      "requires": {
        "bins": ["python3"],
        "env": ["HOPSAPI_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "HOPSAPI_API_KEY",
      "installSpec": {
        "bins": ["python3"],
        "env": ["HOPSAPI_API_KEY"],
        "pip": ["requests"]
      }
    }
  }
---

# HopsAPI · MiniMax-H3 视频生成

**模型 ID:** `MiniMax-H3` · **脚本:** `scripts/generation_api.py`

本技能按 **storyclaw-token-gateway** 的 MiniMax H3 请求与计费规则实现，**不走 giggle.pro**。旧 skill `giggle-minimax-h3-gen` 保持不动。

- **主流程**：确认模式与参数 →（可选）优化提示词 → 配置 Key → 提交 Router 任务并轮询。
- **计费细则**：[references/billing.md](references/billing.md)

---

## Base URL 与接口

| 用途 | 环境变量 | 默认值 |
|------|----------|--------|
| API Base URL | `HOPSAPI_BASE_URL` | `https://hopsapi.com/v1` |
| 控制台（文件上传） | `HOPSAPI_CONSOLE_URL` | `https://hopsapi.com` |

鉴权请求头（二选一）：`Authorization: Bearer sk-...` 或 `x-api-key: sk-...`。

| 操作 | 方法 | 完整 URL（默认） |
|------|------|------------------|
| 创建视频任务 | `POST` | `https://hopsapi.com/v1/router/task/create` |
| 查询任务 | `GET` | `https://hopsapi.com/v1/router/tasks/{task_id}` |
| 停止任务 | `POST` | `https://hopsapi.com/v1/router/task/stop` |
| 远程 URL 转存 | `POST` | `https://hopsapi.com/api/file-url-upload` |
| 本地文件上传 | `POST` | `https://hopsapi.com/api/file-stream-upload` |

创建任务请求体核心字段：`task`（`Txt2Video` / `Img2Video` / `OmniVideo`）、`model`（`MiniMax-H3`）、`input`（`prompt` / `images` / `videos` / `audios` / `duration` / `resolution` 等）。白标站改 `HOPSAPI_BASE_URL` / `HOPSAPI_CONSOLE_URL` 即可，路径不变。

### 请求示例（HTTP）

以下均为 `POST https://hopsapi.com/v1/router/task/create`。本 skill 约束 `duration` 为 **4–15**；省略 `resolution` / `duration` 时网关默认 `768p` / `5`。

**公共请求头：**

```http
Authorization: Bearer sk-你的KEY
Content-Type: application/json
```

也可改用 `x-api-key: sk-你的KEY`。

#### 1. 文生视频（Txt2Video）

```bash
curl -s https://hopsapi.com/v1/router/task/create \
  -H "Authorization: Bearer sk-你的KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Txt2Video",
    "model": "MiniMax-H3",
    "input": {
      "prompt": "电影感的山间日出，云海缓慢流动",
      "duration": 5,
      "resolution": "768p"
    }
  }'
```

```json
{
  "task": "Txt2Video",
  "model": "MiniMax-H3",
  "input": {
    "prompt": "电影感的山间日出，云海缓慢流动",
    "duration": 5,
    "resolution": "768p"
  }
}
```

#### 2. 图生视频（Img2Video，恰好 1 张图）

```bash
curl -s https://hopsapi.com/v1/router/task/create \
  -H "Authorization: Bearer sk-你的KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Img2Video",
    "model": "MiniMax-H3",
    "input": {
      "prompt": "让画面中的云层缓慢流动，镜头平稳向前推进",
      "images": ["https://assets.example.com/input.png"],
      "duration": 5,
      "resolution": "480p"
    }
  }'
```

```json
{
  "task": "Img2Video",
  "model": "MiniMax-H3",
  "input": {
    "prompt": "让画面中的云层缓慢流动，镜头平稳向前推进",
    "images": ["https://assets.example.com/input.png"],
    "duration": 5,
    "resolution": "480p"
  }
}
```

#### 3. 首尾帧（Img2Video，恰好 2 张图：首 → 尾）

```bash
curl -s https://hopsapi.com/v1/router/task/create \
  -H "Authorization: Bearer sk-你的KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Img2Video",
    "model": "MiniMax-H3",
    "input": {
      "prompt": "镜头从清晨自然过渡到黄昏",
      "images": [
        "https://assets.example.com/first.png",
        "https://assets.example.com/last.png"
      ],
      "duration": 10,
      "resolution": "768p",
      "aspect_ratio": "16:9",
      "generate_audio": true
    }
  }'
```

```json
{
  "task": "Img2Video",
  "model": "MiniMax-H3",
  "input": {
    "prompt": "镜头从清晨自然过渡到黄昏",
    "images": [
      "https://assets.example.com/first.png",
      "https://assets.example.com/last.png"
    ],
    "duration": 10,
    "resolution": "768p",
    "aspect_ratio": "16:9",
    "generate_audio": true
  }
}
```

#### 4. 全能参考 · 仅图片（OmniVideo → 参考图计价）

前 5 张参考图免费；第 6 张起按成片秒加价。

```bash
curl -s https://hopsapi.com/v1/router/task/create \
  -H "Authorization: Bearer sk-你的KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "OmniVideo",
    "model": "MiniMax-H3",
    "input": {
      "prompt": "保持参考图片中人物的外观与服装",
      "images": [
        "https://assets.example.com/character-1.png",
        "https://assets.example.com/character-2.png"
      ],
      "duration": 8,
      "resolution": "480p"
    }
  }'
```

```json
{
  "task": "OmniVideo",
  "model": "MiniMax-H3",
  "input": {
    "prompt": "保持参考图片中人物的外观与服装",
    "images": [
      "https://assets.example.com/character-1.png",
      "https://assets.example.com/character-2.png"
    ],
    "duration": 8,
    "resolution": "480p"
  }
}
```

#### 5. 全能参考 · 含视频（OmniVideo → 参考视频计价，更贵）

**不要**传 `video_durations`；时长由平台探测。

```bash
curl -s https://hopsapi.com/v1/router/task/create \
  -H "Authorization: Bearer sk-你的KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "OmniVideo",
    "model": "MiniMax-H3",
    "input": {
      "prompt": "保持参考图片中人物的外观，沿用参考视频的运镜",
      "images": ["https://assets.example.com/character.png"],
      "videos": ["https://assets.example.com/camera-motion.mp4"],
      "duration": 15,
      "resolution": "768p"
    }
  }'
```

```json
{
  "task": "OmniVideo",
  "model": "MiniMax-H3",
  "input": {
    "prompt": "保持参考图片中人物的外观，沿用参考视频的运镜",
    "images": ["https://assets.example.com/character.png"],
    "videos": ["https://assets.example.com/camera-motion.mp4"],
    "duration": 15,
    "resolution": "768p"
  }
}
```

#### 6. 全能参考 · 含音频（音频不加价）

```json
{
  "task": "OmniVideo",
  "model": "MiniMax-H3",
  "input": {
    "prompt": "人物对口型演唱，节奏跟随参考音频",
    "images": ["https://assets.example.com/singer.png"],
    "audios": ["https://assets.example.com/vocal.mp3"],
    "duration": 8,
    "resolution": "768p"
  }
}
```

#### 7. 创建成功响应

```json
{ "code": 200, "message": "success", "task_id": "tsk_0f3c9a72b1e04d5f" }
```

#### 8. 查询任务

```bash
curl -s https://hopsapi.com/v1/router/tasks/tsk_0f3c9a72b1e04d5f \
  -H "Authorization: Bearer sk-你的KEY"
```

成功终态示例（`status: 2`）：

```json
{
  "task_id": "tsk_0f3c9a72b1e04d5f",
  "status": 2,
  "result": {
    "content": { "video_url": "https://static.example.com/video.mp4" },
    "resolution": "768p"
  },
  "cost": 12.34
}
```

也可能是 `results: [{ "urls": ["https://..."] }]`；脚本两种都解析。

| status | 含义 |
|--------|------|
| `0` | 排队 |
| `1` | 处理中 |
| `2` | 成功（已结算） |
| `3` | 失败（不扣费） |
| `4` | 已取消（不扣费） |

#### 9. 停止任务

```bash
curl -s https://hopsapi.com/v1/router/task/stop \
  -H "Authorization: Bearer sk-你的KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_id":"tsk_0f3c9a72b1e04d5f"}'
```

#### 10. 素材上传（本地无公网 URL 时）

远程转存：

```bash
curl -s https://hopsapi.com/api/file-url-upload \
  -H "Authorization: Bearer sk-你的KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://example.com/reference.png",
    "uploadPath": "images",
    "fileName": "reference.png"
  }'
```

本地文件流：

```bash
curl -s https://hopsapi.com/api/file-stream-upload \
  -H "Authorization: Bearer sk-你的KEY" \
  -F "file=@./ref.png" \
  -F "uploadPath=images" \
  -F "fileName=ref.png"
```

成功后取响应 `data.fileUrl`，再填入创建任务的 `images` / `videos` / `audios`。

---

## 平台约束（以网关为准）

| 项目 | 规则 |
|------|------|
| 模型 | 固定 `MiniMax-H3`（对外 public id；勿传上游内部模型名） |
| 渠道 | 仅**官方 API 中转**；Key 须在控制台勾选授权该模型 |
| 时长 | **4–15** 整数秒；省略默认 **5** |
| 分辨率 | **480p** / **768p**；省略默认 **768p**（大小写不敏感） |
| 画幅 | `16:9` / `9:16` / `1:1` / `4:3` / `3:4` / `21:9` / `auto`；**省略则不传** |
| 音频输出 | `generate_audio` 布尔；省略时上游按 **true** |
| 素材 | **仅公网 HTTPS URL**；本地 / Base64 须先上传（`--upload-file` / `--upload-url`） |
| 参考视频时长 | **不要**传 `video_durations`；平台建任务前探测，失败则 400 |
| 轮询 | 每 **3–5** 秒 `GET /v1/router/tasks/{task_id}` |

### 生成模式 ↔ `task`

| 模式 | `task` | 输入要求 |
|------|--------|----------|
| 文生视频 | `Txt2Video` | `prompt` 非空；images/videos/audios 为空 |
| 图生视频 | `Img2Video` | `images` **恰好 1** 个 URL |
| 首尾帧 | `Img2Video` | `images` **恰好 2** 个 URL（首、尾顺序） |
| 全能参考 | `OmniVideo` | images / videos / audios **至少一项**非空 |

全能参考上限：图片 ≤9、视频 ≤3、音频 ≤3。

### CLI `--mode` 映射

| `--mode` | 网关 `task` |
|----------|-------------|
| `text` | `Txt2Video` |
| `image` | `Img2Video`（`--images` 1～2 张，或 `--start-frame` + 可选 `--end-frame`） |
| `omni` | `OmniVideo` |

---

## ⚠️ Language Rule

**Match the user's input language exactly.** 用户中文 → 中文 prompt；英文 → 英文 prompt。只输出**一个**优化版本，不要双语对照。

---

## Step 1: 确认参数与提示词

用户未指定时再询问；已明确则跳过。

1. **模式**：文生 / 单图 / 首尾帧 / 全能参考（是否有参考视频——参考视频显著更贵，见计费文档）
2. **时长**：4–15s，默认 5
3. **分辨率**：480p（更便宜）或 768p（默认）
4. **比例**（可选）：不传则省略字段
5. **提示词**：短片建议主体 + 动作 + 环境 + 运镜；有参考图时写清「参考」还是「编辑」

提交前自检：

- [ ] `duration ∈ [4,15]` 整数
- [ ] `resolution ∈ {480p,768p}`
- [ ] 素材均为可访问 HTTPS URL
- [ ] image 模式恰好 1 或 2 张图；omni 未超上限
- [ ] 未自行填写 `video_durations`

---

## Step 2: API Key（一次性）

```bash
python3 scripts/generation_api.py --check-key
```

未配置时向用户索要 Key（控制台 → **API Keys** → 创建并勾选 **MiniMax-H3**），再执行：

```bash
python3 scripts/generation_api.py --setup --api-key <sk-...>
```

环境变量：`HOPSAPI_API_KEY`。可选覆盖：

- `HOPSAPI_BASE_URL`（默认 `https://hopsapi.com/v1`）
- `HOPSAPI_CONSOLE_URL`（默认 `https://hopsapi.com`，用于文件上传）

---

## Step 3: 提交并轮询

**先告知用户**：已提交、将主动轮询（约数分钟），并给出 `task_id`。默认脚本提交后自动轮询；任务完成后**主动**回传视频链接与 `cost`，无需用户催问。出错**不要盲目重试**，先报告错误。

### 文生视频

```bash
python3 scripts/generation_api.py \
  --mode text --prompt "<prompt>" \
  --duration 5 --resolution 768p
```

### 图生视频

```bash
python3 scripts/generation_api.py \
  --mode image --prompt "<prompt>" \
  --images "https://example.com/input.png" \
  --duration 5 --resolution 480p
```

### 首尾帧

```bash
python3 scripts/generation_api.py \
  --mode image --prompt "<prompt>" \
  --start-frame "https://example.com/first.png" \
  --end-frame "https://example.com/last.png" \
  --duration 10 --resolution 768p --aspect-ratio 16:9
```

### 全能参考（含视频时更贵）

```bash
python3 scripts/generation_api.py \
  --mode omni --prompt "<prompt>" \
  --images "https://example.com/character.png" \
  --videos "https://example.com/camera-motion.mp4" \
  --duration 15 --resolution 768p
```

### 本地 / 远程文件先转公网 URL

```bash
python3 scripts/generation_api.py --upload-file ./ref.png --upload-path images
python3 scripts/generation_api.py --upload-url "https://example.com/a.mp4" --upload-path videos
# 将返回的 fileUrl 再传入 --images / --videos / --audios
```

### 查询 / 续轮询 / 停止

```bash
python3 scripts/generation_api.py --query --task-id tsk_xxx
python3 scripts/generation_api.py --wait --task-id tsk_xxx
python3 scripts/generation_api.py --stop --task-id tsk_xxx
```

创建成功响应示例：

```json
{"code": 200, "message": "success", "task_id": "tsk_0f3c9a72b1e04d5f"}
```

| status | 含义 |
|--------|------|
| `0` | 排队 |
| `1` | 处理中 |
| `2` | 成功（已结算，可读视频与 `cost`） |
| `3` | 失败（不扣费） |
| `4` | 已取消（不扣费） |

成功终态可能为 `result.content.video_url` 或 `results[].urls`；脚本两种都解析。失败查询仍可能 HTTP 200 + `code=424`。

---

## Parameters

| Parameter | Default | Options |
|-----------|---------|---------|
| `--mode` | required | `text` / `image` / `omni` |
| `--prompt` | 文生必填 | 与用户语言一致 |
| `--model` | `MiniMax-H3` | 仅此值 |
| `--duration` | `5` | 4–15 |
| `--resolution` | `768p` | `480p` / `768p` |
| `--aspect-ratio` | 省略不传 | 见上表 |
| `--generate-audio` / `--no-generate-audio` | 省略=上游默认 true | 布尔 |
| `--images` / `--videos` / `--audios` | — | 公网 URL（可带 `url:` 前缀） |
| `--callback-url` | — | 可选 HTTPS 回调 |
| `--no-wait` | false | 只提交不轮询 |

---

## 计费速览

官方价 = 成片费 + 参考图附加费 + 参考视频附加费（再 × 账户系数 → 响应 `cost`）。

- 文生 / 图生 / 首尾帧：相对便宜（成片按秒；图生/首尾帧**无**参考图附加费）
- Omni 仅图：参考图模式；前 5 张免费，第 6 张起按成片秒加价
- Omni 含视频：参考视频模式，成片与输入视频单价都高；时长由平台探测封顶

完整公式与示例见 [references/billing.md](references/billing.md)。提交前若用户在意成本，优先建议：无参考视频、480p、更短时长、参考图 ≤5。

---

## 常见错误

| 现象 | 处理 |
|------|------|
| `Unsupported resolution '720p'` | 只用 480p / 768p |
| `duration` 不在 4–15 | 改 4–15 整数秒 |
| `images must contain 1 or 2` | Img2Video 只能 1 或 2 张 |
| Omni 素材全空 / 超上限 | 至少一项；图≤9 视频≤3 音频≤3 |
| 参考视频探测失败 | 换可 Range 访问的公网 mp4/mov，勿自报时长 |
| `401` / 未授权模型 | 重建 Key 并勾选 MiniMax-H3 |
| `402` | 控制台充值 |
| HTTP `424` 终态失败 | 不扣费；调整 prompt/素材后重新提交（勿盲目同参重试） |
