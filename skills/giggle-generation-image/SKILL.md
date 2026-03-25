---
name: giggle-generation-image
description: "Supports text-to-image and image-to-image. Use when the user needs to create or generate images. After submit, proactively poll task status every ~15–30s and message the user each time until completed/failed/timeout—do not wait for the user to ask for progress. Use cases: (1) Generate from text description, (2) Use reference images, (3) Customize model, aspect ratio, resolution. Triggers: generate image, draw, create image, AI art."
version: "0.0.10"
license: MIT
author: giggle-official
homepage: https://github.com/giggle-official/skills
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "📂",
      "requires": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "GIGGLE_API_KEY"
    }
  }
---

# Giggle Image Generation (Multi-Model)

**Source**: [giggle-official/skills](https://github.com/giggle-official/skills) · API: [giggle.pro](https://giggle.pro/)

Generates AI images via giggle.pro's Generation API. Supports multiple models (Seedream, Midjourney, Nano Banana). Submit task → **agent proactively polls** with `--query` until done (see「持续输出进度」). No Cron.

**API Key**: Set system environment variable `GIGGLE_API_KEY`. The script will prompt if not configured.

> **No inline Python**: All commands must be executed via the `exec` tool. **Never** use `python3 << 'EOF'` or heredoc inline code.

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

## Supported Models

| Model | Description |
|-------|-------------|
| seedream45 | Seedream, realistic and creative |
| midjourney | Midjourney style |
| nano-banana-2 | Nano Banana 2 |
| nano-banana-2-fast | Nano Banana 2 fast |

---

## Execution Flow: Submit and Query

Image generation is asynchronous (typically 30–120 seconds). **Submit** a task to get `task_id`, then **query** until the task reaches a terminal state.

> **Important**: **Never** pass `GIGGLE_API_KEY` in exec's `env` parameter. API Key is read from system environment variable.

---

## 持续输出进度（默认行为，无需用户写在提示词里）

用户**不必**再说「随时输出进度」「不要等我催才查」；按本 skill 执行即默认要求：

1. **提交后立刻**简短告知：已提交、`task_id`、预计约 30 秒–2 分钟。
2. **主动轮询**：每隔约 **15–30 秒**执行一次 `--query`，**不要**等用户追问。
3. **每次查询后立刻**向用户说明进度；`processing`/`pending` 等用自然语言转述并说明会继续查询。
4. **终态**：成功则转发完整图片链接；失败则说明原因；超过合理上限（例如 **15 分钟**）仍非终态，说明情况并给出 `task_id`。
5. **例外**：用户**明确**说「不用轮询」「我自己问」时，可只提交 + 告知 `task_id`。

---

### Step 1: Submit Task

```bash
# Text-to-image (default seedream45)
python3 scripts/generation_api.py \
  --prompt "description" --aspect-ratio 16:9 \
  --model seedream45 --resolution 2K \
  --no-wait --json

# Text-to-image - Midjourney
python3 scripts/generation_api.py \
  --prompt "description" --model midjourney \
  --aspect-ratio 16:9 --resolution 2K \
  --no-wait --json

# Image-to-image - Reference URL
python3 scripts/generation_api.py \
  --prompt "Convert to oil painting style, keep composition" \
  --reference-images "https://example.com/photo.jpg" \
  --model nano-banana-2-fast \
  --no-wait --json

# Batch generate multiple images
python3 scripts/generation_api.py \
  --prompt "description" --generate-count 4 \
  --no-wait --json
```

Response example:
```json
{"status": "started", "task_id": "xxx"}
```

**Store task_id in memory** (`addMemory`):
```
giggle-generation-image task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

**Tell the user**: 图片任务已提交，将自动查询进度并在有结果时立即告知，无需反复问「好了吗」。

---

### Step 2: Query Until Done (default: proactive polling)

After each submit for the **current** task, **repeatedly** run (every ~15–30s until terminal or timeout), **without waiting for the user to ask**:

```bash
python3 scripts/generation_api.py --query --task-id <task_id>
```

**Behavior**:
- **completed**: Output image links for user → **stop** polling
- **failed/error**: Output error message → **stop** polling
- **processing/pending**: JSON in stdout → tell user status + 将继续查询 → **continue** polling

If the user asks while you are polling, answer with the latest status.

---

## New Request vs Query Old Task

**When the user initiates a new image generation request**, run submit to create a new task. Do not reuse old task_id from memory.

**For the in-flight task**, use proactive polling as above. **For a previous task**, query (and optionally poll) that `task_id` when the user asks or requests updates.

---

## Parameter Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--prompt` | required | Image description prompt |
| `--model` | seedream45 | seedream45, midjourney, nano-banana-2, nano-banana-2-fast |
| `--aspect-ratio` | 16:9 | 16:9, 9:16, 1:1, 3:4, 4:3, 2:3, 3:2, 21:9 |
| `--resolution` | 2K | Text-to-image: 1K, 2K, 4K (image-to-image partially supported) |
| `--generate-count` | 1 | Number of images to generate |
| `--reference-images` | - | Image-to-image reference; supports URL, base64, asset_id |
| `--watermark` | false | Add watermark (image-to-image) |

---

## Image-to-Image Reference: Three Input Methods

The image-to-image API's `reference_images` is an array of objects. Each element can be one of these three formats (can be mixed):

### Method 1: URL

```json
{
  "prompt": "A cute orange cat sitting on the windowsill in the sun, realistic style",
  "reference_images": [
    {
      "url": "https://assets.giggle.pro/private/example/image.jpg?Policy=EXAMPLE_POLICY&Key-Pair-Id=EXAMPLE_KEY_PAIR_ID&Signature=EXAMPLE_SIGNATURE"
    }
  ],
  "generate_count": 1,
  "model": "nano-banana-2-fast",
  "aspect_ratio": "16:9",
  "watermark": false
}
```

### Method 2: Base64

```json
{
  "prompt": "A cute orange cat sitting on the windowsill in the sun, realistic style",
  "reference_images": [
    {
      "base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    }
  ],
  "generate_count": 1,
  "model": "nano-banana-2-fast",
  "aspect_ratio": "16:9",
  "watermark": false
}
```

> Base64 format: Pass the raw Base64 string directly. Do not add the `data:image/xxx;base64,` prefix.

### Method 3: asset_id

```json
{
  "prompt": "A cute orange cat sitting on the windowsill in the sun, realistic style",
  "reference_images": [
    {
      "asset_id": "vvsdsfsdf"
    }
  ],
  "generate_count": 1,
  "model": "nano-banana-2-fast",
  "aspect_ratio": "16:9",
  "watermark": false
}
```

> For multiple reference images, add more objects to the `reference_images` array.

---

## Interaction Guide

**When the user request is vague, guide per the steps below. If the user has provided enough info, run the command directly.**

### Step 1: Model Selection

```
Question: "Which model would you like to use?"
Title: "Image Model"
Options:
- "seedream45 - Realistic & creative (recommended)"
- "midjourney - Artistic style"
- "nano-banana-2 - High quality"
- "nano-banana-2-fast - Fast generation"
multiSelect: false
```

### Step 2: Aspect Ratio

```
Question: "What aspect ratio do you need?"
Title: "Aspect Ratio"
Options:
- "16:9 - Landscape (wallpaper/cover) (recommended)"
- "9:16 - Portrait (mobile)"
- "1:1 - Square"
- "Other ratios"
multiSelect: false
```

### Step 3: Generation Mode

```
Question: "Do you need reference images?"
Title: "Generation Mode"
Options:
- "No - Text-to-image only"
- "Yes - Image-to-image (style transfer)"
multiSelect: false
```

### Step 4: Execute and Display

Submit task → store task_id → inform user → **主动轮询 `--query`** 直至终态，每次查询后向用户说明进度；终态时转发 stdout 中的链接或错误。

**Link return rule**: Image links in results must be **full signed URLs** (with Policy, Key-Pair-Id, Signature query params). **Do not strip or omit** `&response-content-disposition=attachment` when the API returns it — forward links **as-is** so downloads behave correctly. Correct: `https://assets.giggle.pro/...?Policy=...&Key-Pair-Id=...&Signature=...&response-content-disposition=attachment` (order of query params may vary). Wrong: unsigned URLs with only the base path, or URLs with `response-content-disposition=attachment` removed.
