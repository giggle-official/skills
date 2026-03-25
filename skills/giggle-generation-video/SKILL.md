---
name: giggle-generation-video
description: "Supports text-to-video and image-to-video (start/end frame). Use when the user needs to generate video, create short videos, or convert text to video. After submit, proactively poll task status every ~15–30s and message the user each time until completed/failed/timeout—do not wait for the user to ask for progress. Use cases: (1) Generate video from text description, (2) Use reference images as start/end frame for image-to-video, (3) Customize model, aspect ratio, duration, resolution. Triggers: generate video, text-to-video, image-to-video, AI video."
version: "0.0.10"
license: MIT
author: giggle-official
homepage: https://github.com/giggle-official/skills
repository: https://github.com/giggle-official/skills
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "🎬",
      "requires": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "GIGGLE_API_KEY",
      "installSpec": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY"],
        "pip": ["requests"]
      }
    }
  }
---

# Giggle Video Generation

**Source**: [giggle-official/skills](https://github.com/giggle-official/skills) · API: [giggle.pro](https://giggle.pro/)

Generates AI videos via giggle.pro's Generation API. Supports text-to-video and image-to-video. Submit task → **agent proactively polls** with `--query` until done (see「持续输出进度」). No Cron, no file writes—all operations via exec.

---

## Installation Requirements

| Requirement | Value |
|-------------|-------|
| **Binary** | `python3` |
| **Environment** | `GIGGLE_API_KEY` (required; obtain from https://giggle.pro/) |
| **Pip** | `requests` |

Set `GIGGLE_API_KEY` before use. The script will prompt if not configured.

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

---

## Supported Models

| Model | Supported Durations (s) | Default | Description |
|-------|-------------------------|---------|-------------|
| grok | 6, 10 | 6 | Strong overall capability, recommended |
| grok-fast | 6, 10 | 6 | grok fast version |
| sora2 | 4, 8, 12 | 4 | OpenAI Sora 2 |
| sora2-pro | 4, 8, 12 | 4 | Sora 2 Pro |
| sora2-fast | 10, 15 | 10 | Sora 2 Fast |
| sora2-pro-fast | 10, 15 | 10 | Sora 2 Pro Fast |
| kling25 | 5, 10 | 5 | Kling video model |
| seedance15-pro | 4, 8, 12 | 4 | Seedance Pro (with audio) |
| seedance15-pro-no-audio | 4, 8, 12 | 4 | Seedance Pro (no audio) |
| veo31 | 4, 6, 8 | 4 | Google Veo 3.1 (with audio) |
| veo31-no-audio | 4, 6, 8 | 4 | Google Veo 3.1 (no audio) |
| minimax23 | 6 | 6 | MiniMax model |
| wan25 | 5, 10 | 0 | Wanxiang model |

**Note**: `--duration` must be chosen from the model's supported durations, otherwise the API will error.

---

## Frame Reference (Image-to-Video)

For image-to-video, `--start-frame` and `--end-frame` support three mutually exclusive formats:

| Method | Format | Example |
|--------|--------|---------|
| asset_id | `asset_id:<ID>` | `asset_id:lkllv0yv81` |
| url | `url:<URL>` | `url:https://example.com/img.jpg` |
| base64 | `base64:<DATA>` | `base64:iVBORw0KGgo...` |

Each frame parameter can only use one of these methods.

---

## Execution Flow: Submit and Query

Video generation is asynchronous (typically 60–300 seconds). **Submit** a task to get `task_id`, then **query** until the task reaches a terminal state. All commands run via `exec`; API key from system env.

---

## 持续输出进度（默认行为，无需用户写在提示词里）

用户**不必**再说「随时输出进度」「不要等我催才查」之类话；按本 skill 执行即视为默认要求：

1. **提交后立刻**用简短中文告知：已提交、`task_id`、预计等待量级（如 1–5 分钟或更长）。
2. **主动轮询**：提交成功后，**每隔约 15–30 秒**执行一次 `--query`（同一任务内持续执行，**不要**等用户追问「好了吗」再查）。
3. **每次查询后立刻**向用户发一条进度说明（例如：仍在处理中 / 排队中 / 第 N 次查询）；若 stdout 为 `processing` 等 JSON，用自然语言转述，勿静默。
4. **终态**：`completed` 则按下文规则转发完整视频链接；`failed` / `error` 则说明原因；若已超过合理上限（例如 **20 分钟**）仍非终态，说明情况并给出 `task_id`，建议用户稍后让你再查或重试。
5. **例外**：仅当用户**明确**表示「不用轮询」「我自己问进度」时，可改为只提交 + 告知 `task_id`，之后仅在用户询问时查询。

> 这样即使用户提示词里不写进度相关句子，也应持续汇报直到完成或明确失败/超时。

---

### Step 1: Submit Task

**First send a message to the user**: 已提交视频生成任务，将每隔一段时间自动查询进度并在有更新时告知，无需反复催促；并给出 `task_id`（在拿到 JSON 后）。

```bash
# Text-to-video (default grok-fast)
python3 scripts/generation_api.py \
  --prompt "Camera slowly pushes forward, person smiling in frame" \
  --model grok-fast --duration 6 \
  --aspect-ratio 16:9 --resolution 720p

# Image-to-video - use asset_id as start frame
python3 scripts/generation_api.py \
  --prompt "Person slowly turns around" \
  --start-frame "asset_id:lkllv0yv81" \
  --model grok-fast --duration 6 \
  --aspect-ratio 16:9 --resolution 720p

# Image-to-video - use URL as start frame
python3 scripts/generation_api.py \
  --prompt "Scenery from still to motion" \
  --start-frame "url:https://example.com/img.jpg" \
  --model grok-fast --duration 6

# Image-to-video - both start and end frame
python3 scripts/generation_api.py \
  --prompt "Scene transition" \
  --start-frame "asset_id:abc123" \
  --end-frame "url:https://example.com/end.jpg" \
  --model grok --duration 6
```

Response example:
```json
{"status": "started", "task_id": "55bf24ca-e92a-4d9b-a172-8f585a7c5969"}
```

**Store task_id in memory** (`addMemory`):
```
giggle-generation-video task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

---

### Step 2: Query Until Done (default: proactive polling)

After each submit for the **current** task, **repeatedly** run (every ~15–30s until terminal state or timeout), **without waiting for the user to ask**:

```bash
python3 scripts/generation_api.py --query --task-id <task_id>
```

Between queries, use a short `sleep` (e.g. 15–30 seconds) in the shell, or separate tool invocations with delay—**do not go silent**; summarize each result to the user.

**Output handling**:

| stdout pattern | Action |
|----------------|--------|
| Plain text with video links (视频已就绪) | Forward to user as-is; **stop** polling this task |
| Plain text with error | Forward to user as-is; **stop** polling this task |
| JSON `{"status": "processing", "task_id": "..."}` (or similar non-terminal) | Tell user current status + that you will check again shortly; **continue** polling per "持续输出进度" |

If the user asks about progress **while** you are already polling, answer with the latest known status (run an extra `--query` if needed).

**Link return rule**: Video links in results must be **full signed URLs** (with Policy, Key-Pair-Id, Signature query params). **Do not strip** `response-content-disposition=attachment` when the API returns it; forward as-is (script only encodes `~` → `%7E`).

---

## New Request vs Query Old Task

**When the user initiates a new video generation request**, **must run Step 1 to submit a new task**. Do not reuse old task_id from memory.

**For the in-flight task**, use proactive polling as above. **For an older task** (user refers to a previous video / previous `task_id`), query that `task_id` when they ask, or poll it if they want continuous updates on that specific task.

---

## Parameter Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--prompt` | required | Video description prompt |
| `--model` | grok | See "Supported Models" table |
| `--duration` | model default | Must choose from model's supported durations |
| `--aspect-ratio` | 16:9 | 16:9, 9:16, 1:1, 3:4, 4:3 |
| `--resolution` | 720p | 480p, 720p, 1080p |
| `--start-frame` | - | Image-to-video start frame: `asset_id:ID`, `url:URL`, or `base64:DATA` |
| `--end-frame` | - | Image-to-video end frame, same format as start |

Note: base64 parameter supports base64-encoded images. Pass the raw Base64 string directly, do not add the `data:image/xxx;base64,` prefix.

---

## Interaction Guide

**When the user request is vague, guide per the steps below. If the user has provided enough info, run the command directly.**

### Step 1: Model Selection (required)

Before generating, **must introduce available models** and let the user choose. Display the model list from "Supported Models" table. Wait for explicit user choice before continuing.

### Step 2: Video Duration

For the chosen model, show supported duration options. Default to the model's default duration.

### Step 3: Generation Mode

```
Question: "Do you need reference images as start/end frame?"
Options: No - text-to-video only / Yes - image-to-video (set start/end frame)
```

### Step 4: Aspect Ratio

```
Question: "What aspect ratio do you need?"
Options: 16:9 - Landscape (recommended) / 9:16 - Portrait / 1:1 - Square
```

### Step 5: Execute and Display

Follow the flow: send message → Step 1 submit → Step 2 **主动轮询查询**直至终态，每次查询后向用户说明进度。Forward exec stdout to the user as-is where appropriate (especially final links and errors).
