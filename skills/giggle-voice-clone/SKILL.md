---
name: giggle-voice-clone
description: "Use when the user wants to clone a voice from an audio sample. Pass reference audio URL to voice-clone, then synthesizes text with that voice via Giggle.pro. Triggers: voice clone, clone my voice, 声音克隆, 复刻声音, 克隆声音, clone voice from audio."
version: "0.0.1"
license: MIT
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "🎙️",
      "requires": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "GIGGLE_API_KEY"
    }
  }
---


# Voice Clone

Clones a voice from a reference audio URL via giggle.pro. Flow: submit voice-clone with `file.url` directly → poll until completed. Returns full signed audio URLs.

**API Key**: Set system environment variable `GIGGLE_API_KEY`. The script will prompt if not configured.

> **No inline Python**: All commands must be executed via the `exec` tool. **Never** use heredoc inline code.

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

## Execution Flow

Voice cloning typically takes 1–3 minutes. The script submits voice-clone with `file.url` directly (no upload step), then polls for result.

> **Important**: **Never** pass `GIGGLE_API_KEY` in exec's `env` parameter. API Key is read from system environment variable.

---

### Step 1: Guide User to Provide Requirements

**Before running, you must collect:**

1. **Audio URL** – A publicly accessible URL of the reference audio (e.g. MP3, WAV). User provides a link to the sample they want to clone.
2. **voice_id** – **User-defined**. Must be unique per clone. Example: `my_voice_001`, `minimax_testasds_02`. If duplicate, API returns `voice clone voice id duplicate`.
3. **Text** – The text to synthesize with the cloned voice (e.g. "A gentle breeze sweeps across the soft grass...").

---

### Step 2: Run Full Flow

```bash
python3 scripts/voice_clone_api.py \
  --audio-url "https://example.com/voice_sample.mp3" \
  --text "A gentle breeze sweeps across the soft grass, carrying the fresh scent." \
  --voice-id "my_unique_voice_01" \
  --need-noise-reduction false \
  --need-volumn-normalization false
```

Optional parameters:
- `--need-noise-reduction` (default: false): Apply noise reduction to cloned audio
- `--need-volumn-normalization` (default: false): Apply volume normalization

---

### Step 3: Handle Output

**Success**: Script outputs the full signed audio URL(s). Forward to user as-is.

**Failure**:
- `voice clone voice id duplicate`: Guide user to choose a different voice_id
- Other errors: Report error message to user

---

## Link Return Rule

Audio links returned to the user must be **full signed URLs** (with Policy, Key-Pair-Id, Signature query params). Correct: `https://assets.giggle.pro/...?Policy=...&Key-Pair-Id=...&Signature=...`. The script handles this; keep URLs as-is when forwarding to user.

---

## Parameter Reference

| Parameter | Required | Default | Description |
|-----------|----------|--------|-------------|
| `--audio-url` | yes | - | Public URL of reference audio to clone |
| `--text` | yes | - | Text to synthesize with cloned voice |
| `--voice-id` | yes | - | User-defined unique voice identifier; must not duplicate existing |
| `--need-noise-reduction` | no | false | Apply noise reduction |
| `--need-volumn-normalization` | no | false | Apply volume normalization |
| `--max-wait` | no | 180 | Max wait seconds for clone task |

---

## Interaction Guide

**When the user initiates voice clone**:

1. Ask: "请提供要克隆的音频链接（需可公网访问）"
2. Ask: "请为这次克隆起一个唯一的 voice_id（如 my_voice_001），不能与已有克隆重复"
3. Ask: "请提供要合成的文本内容"
4. After user provides all three, run the script and forward the output

**If voice_id duplicate**: "该 voice_id 已被使用，请换一个唯一的名称后重试。"
