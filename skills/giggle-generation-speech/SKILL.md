---
name: giggle-generation-speech
description: "Use when the user wants to generate speech, voiceover, or text-to-audio. Converts text to AI voice via Giggle.pro TTS API. Keep the user informed until audio is ready: message before long waits, use Cron/sync poll so the user need not ask for progress. Triggers: generate speech, text-to-speech, TTS, voiceover, read this text aloud, synthesize speech."
version: "0.0.10"
license: MIT
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires": {
          "bins": ["python3"],
          "env": ["GIGGLE_API_KEY"],
          "pip": ["requests"]
        },
        "primaryEnv": "GIGGLE_API_KEY",
        "runtimeBehaviors": {
          "writes": ["~/.openclaw/skills/giggle-generation-speech/logs/"],
          "cron": "Registers polling job (30s interval) when user initiates speech generation"
        }
      }
  }
---

# Text-to-Audio

Synthesizes text into AI voice/voiceover via giggle.pro. Supports multiple voice tones, emotions, and speaking rates.

## ⚠️ Review Before Installing

**Please review the following before installing.** This skill will:

1. **Write** to `~/.openclaw/skills/giggle-generation-speech/logs/` – Task state files for Cron deduplication
2. **Register Cron** (30s interval) – Async polling when user initiates speech generation; removed when complete
3. **Forward raw stdout** – Script output (audio links, status) is passed to the user as-is

**Requirements**: `python3`, `GIGGLE_API_KEY` (system environment variable), pip packages: `requests`

---

**API Key**: Set system environment variable `GIGGLE_API_KEY`. The script will prompt if not configured.

> **No inline Python**: All commands must be executed via the `exec` tool. **Never** use heredoc inline code.

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

## Execution Flow (Phase 1 Submit + Phase 2 Cron + Phase 3 Sync Fallback)

Speech generation typically takes 10–30 seconds. Uses "fast submit + Cron poll + sync fallback" three-phase architecture.

> **Important**: **Never** pass `GIGGLE_API_KEY` in exec's `env` parameter. API Key is read from system environment variable.

---

## 持续输出进度（默认行为，无需用户写在提示词里）

用户**不必**在提示词里写「随时输出进度」「不要等我催才查」。执行本 skill 时应：

1. **Phase 1 提交后**已告知「结果将自动送达」—保持该预期；不要让用户以为必须主动追问。
2. **进入 Phase 3 同步等待前**，必须先发一条简短说明：正在等待合成完成（通常 10–30 秒，本阶段最长约 2 分钟），完成后立即转发音频链接，**请勿静默长时间无回复**。
3. **Phase 2 Cron**：处理中（stdout 为 JSON）时，**不要**完全消失；从第 2 次 JSON 轮询起，**每隔一次** Cron 触发可向用户发一句极简进度（如「语音仍在生成中」），避免数分钟无任何反馈；**终态**（非 JSON 或空 stdout 规则见下表）必须转发或按表移除 Cron。
4. **例外**：用户明确说「不用提醒进度」时，可仅在完成或失败时回复。

---

### Phase 0: Guide User to Select Voice and Emotion (required)

**Before submitting, you must guide the user to select voice and emotion. Do not use defaults.**

1. Run `--list-voices` to get available voices:

```bash
python3 scripts/text_to_audio_api.py --list-voices
```

2. Display the voice list to the user in a readable format (voice_id, name, style, gender, etc.) and guide them to pick one
3. Ask the user's preferred emotion (e.g. joy, sad, neutral, angry, surprise). Use neutral if no preference
4. Only after the user confirms voice and emotion, proceed to Phase 1 submit

---

### Phase 1: Submit Task (exec completes in ~10 seconds)

**First send a message to the user**: 语音任务已提交，通常 10–30 秒内完成；**将自动查询并在就绪后立即发送链接**，无需反复催促进度。

```bash
# Must specify user-selected voice and emotion
python3 scripts/text_to_audio_api.py \
  --text "The weather is nice today" \
  --voice-id "Calm_Woman" \
  --emotion "joy" \
  --speed 1.2 \
  --no-wait --json

# View available voices
python3 scripts/text_to_audio_api.py --list-voices
```

Response example:

```json
{"status": "started", "task_id": "xxx"}
```

**Immediately store task_id in memory** (`addMemory`):

```
giggle-generation-speech task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

---

### Phase 2: Register Cron (30 second interval)

Use the `cron` tool to register the polling job. **Strictly follow the parameter format**:

```json
{
  "action": "add",
  "job": {
    "name": "giggle-generation-speech-<first 8 chars of task_id>",
    "schedule": {
      "kind": "every",
      "everyMs": 30000
    },
    "payload": {
      "kind": "systemEvent",
      "text": "Speech task poll: exec python3 scripts/text_to_audio_api.py --query --task-id <full task_id>, handle stdout per Cron logic. If stdout is non-JSON plain text, forward to user and remove Cron. If stdout is JSON (still processing), keep Cron; from the 2nd JSON poll onward, alternate: every other poll send user one brief line (e.g. 语音仍在生成中). If stdout is empty, remove Cron immediately, do not send message."
    },
    "sessionTarget": "main"
  }
}
```

**Cron trigger handling** (based on exec stdout):

| stdout pattern | Action |
|----------------|--------|
| Non-empty plain text (not starting with `{`) | **Forward to user as-is**, **remove Cron** |
| stdout empty | Already pushed, **remove Cron immediately, do not send message** |
| JSON (starts with `{`, has `"status"` field) | Keep Cron; per「持续输出进度」, from 2nd JSON poll onward send a brief line every other poll |

---

### Phase 3: Sync Wait (optimistic path, fallback when Cron hasn't fired)

**Execute this step whether or not Cron registration succeeded.**

**Immediately before this exec**, send the user a short line: 正在同步等待合成结果（通常很快，最长约 2 分钟），请稍候。

```bash
python3 scripts/text_to_audio_api.py --query --task-id <task_id> --poll --max-wait 120
```

**Handling logic**:

- Returns plain text (speech ready/failed message) → **Forward to user as-is**, remove Cron
- stdout empty → Cron already pushed, remove Cron, do not send message
- exec timeout → Cron continues polling

---

## View Voice List

When the user wants to see available voices, run:

```bash
python3 scripts/text_to_audio_api.py --list-voices
```

The script calls `GET /api/v1/project/preset_tones` and displays voice_id, name, style, gender, age, language to the user.

---

## Link Return Rule

Audio links returned to the user must be **full signed URLs** (with Policy, Key-Pair-Id, Signature query params). **Do not strip** `response-content-disposition=attachment` when the API returns it. The script only normalizes `~` → `%7E`; forward URLs as-is otherwise.

---

## New Request vs Query Old Task

**When the user initiates a new speech generation request**, **must run Phase 1 to submit a new task**. Do not reuse old task_id from memory.

**For the in-flight task**, follow Phases 2–3 and「持续输出进度」—do not wait for the user to ask. **For an older task**, query that `task_id` when the user asks (or poll if they want updates).

---

## Parameter Reference

| Parameter | Required | Default | Description |
|-----------|----------|--------|-------------|
| `--text` | yes | - | Text to synthesize |
| `--voice-id` | yes | - | Voice ID; must get via `--list-voices` and guide user to choose |
| `--emotion` | yes | - | Emotion: joy, sad, neutral, angry, surprise, etc. Guide user to choose |
| `--speed` | no | 1 | Speaking rate multiplier |
| `--list-voices` | - | - | Get available voice list |
| `--query` | - | - | Query task status |
| `--task-id` | required for query | - | Task ID |
| `--poll` | no | - | Sync poll with `--query` |
| `--max-wait` | no | 120 | Max wait seconds |

---

## Interaction Guide

**Before each speech generation, complete this interaction**:

1. If the user did not provide text, ask: "Which text would you like to convert to speech?"
2. **Must guide user to select voice**: Run `--list-voices`, display list, have user choose. **Do not use default voice**
3. **Must guide user to select emotion**: Ask the user's preferred emotion (joy, sad, neutral, angry, surprise, etc.)
4. After user confirms text, voice, and emotion, run Phase 1 submit → Phase 2 register Cron → Phase 3 sync wait
