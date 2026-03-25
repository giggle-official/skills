---
name: giggle-generation-music
description: "Use when the user wants to create, generate, or compose music—whether from text description, custom lyrics, or instrumental background music. After submit, proactively poll task status every ~15–30s and message the user each time until completed/failed/timeout—do not wait for the user to ask for progress. Triggers: generate music, write a song, compose, create music, AI music, background music, instrumental, beats."
version: "0.0.10"
license: MIT
author: giggle-official
homepage: https://github.com/giggle-official/skills
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  openclaw:
    emoji: "📂"
    requires:
      bins: [python3]
      env: [GIGGLE_API_KEY]
      pip: [requests]
    primaryEnv: GIGGLE_API_KEY
---

# Giggle Music

**Source**: [giggle-official/skills](https://github.com/giggle-official/skills) · API: [giggle.pro](https://giggle.pro/)

Generates AI music via giggle.pro. Supports simplified and custom modes. Submit task → **agent proactively polls** with `--query` until done (see **Continuous progress updates**). No Cron.

**API Key**: Set system environment variable `GIGGLE_API_KEY`. Log in to [Giggle.pro](https://giggle.pro/) and obtain the API Key from account settings.

> **Important**: **Never** pass `GIGGLE_API_KEY` in exec's `env` parameter. API Key is read from system environment variable.

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

---

## Interaction Guide

### Mode Selection (priority: high to low)

| User input | Mode | Description |
|------------|------|-------------|
| User provides full **lyrics** | Custom mode (B) | Must be lyrics, not description |
| User requests instrumental/background music | Instrumental mode (C) | No vocals |
| Other cases (description, style, vocals, etc.) | **Simplified mode (A)** | Use user description as prompt; AI composes |

> **Key rule**: If the user does not provide lyrics, always use **simplified mode A**. Use the user's description exactly as `--prompt`; **do not add or rewrite**. E.g. user says "female voice, 1 min, ancient romance", use `--prompt "female voice, 1 min, ancient romance"` directly.

### Guidance when info is lacking

Only when the user input is very vague (e.g. "generate music" with no description), ask:

```
Question: "What type of music would you like to generate?"
Options: AI compose (describe style) / Use my lyrics / Instrumental
```

---

## Execution Flow: Submit and Query

Music generation is asynchronous (typically 1–3 minutes). **Submit** a task to get `task_id`, then **query** until the task reaches a terminal state.

---

## Continuous progress updates (default; user need not put this in their prompt)

Music generation usually takes **~1–3 minutes**. The user does **not** need to ask you to check progress.

1. **Right after submit**, say you submitted, give `task_id`, and expect ~1–3 minutes (longer if the service is busy).
2. **Poll proactively**: run `--query` about every **15–30 seconds** until terminal—**do not** wait for the user to ask.
3. **After each query**, report status; for `processing` JSON, paraphrase and say you will keep checking—**do not** go silent.
4. **When done**: forward full **signed audio** links on success; explain failures. If still non-terminal after **~25 minutes**, explain, give `task_id`, and suggest retry or follow-up.
5. **If the user explicitly opts out** of polling, submit once + `task_id`, then query only when they ask.

---

### Step 1: Submit Task

**First send a message to the user**: Music generation is submitted; you will poll on a schedule and report updates—no need to nag. Include `task_id` from the JSON response.

#### A: Simplified Mode
```bash
python3 scripts/giggle_music_api.py --prompt "user description"
```

#### B: Custom Mode
```bash
python3 scripts/giggle_music_api.py --custom \
  --prompt "lyrics content" \
  --style "pop, ballad" \
  --title "Song Title" \
  --vocal-gender female
```

#### C: Instrumental
```bash
python3 scripts/giggle_music_api.py --prompt "user description" --instrumental
```

Response example:
```json
{"status": "started", "task_id": "xxx"}
```

**Store task_id in memory** (`addMemory`):
```
giggle-generation-music task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

---

### Step 2: Query Until Done (default: proactive polling)

After each submit for the **current** task, **repeatedly** run (every ~15–30s until terminal or timeout), **without waiting for the user to ask**:

```bash
python3 scripts/giggle_music_api.py --query --task-id <task_id>
```

Between queries, use `sleep` in shell or separate invocations with delay—**do not go silent**; summarize each result to the user.

**Output handling**:

| stdout pattern | Action |
|----------------|--------|
| Plain text with music links (e.g. ready message) | Forward to user as-is; **stop** polling |
| Plain text with error | Forward to user as-is; **stop** polling |
| JSON `{"status": "processing", "task_id": "..."}` (non-terminal) | Tell user current status + that you will keep checking; **continue** polling |

If the user asks while you are polling, answer with the latest status (extra `--query` if needed).

**Link return rule**: Audio links in stdout must be **full signed URLs** (with Policy, Key-Pair-Id, Signature query params). **Do not strip** `response-content-disposition=attachment` when the API returns it; forward links as-is (script only encodes `~` → `%7E`).

---

## Recovery

**In-flight task**: use proactive polling as above.

When the user asks about **previous** music (older `task_id`):

1. **task_id in memory** → Run `--query --task-id xxx` directly. **Do not resubmit**; poll until done if they want continuous updates on that task.
2. **No task_id in memory** → Tell the user, ask if they want to regenerate

---

## Parameter Reference

| Parameter | Description |
|-----------|-------------|
| `--prompt` | Music description or lyrics (required in simplified mode) |
| `--custom` | Enable custom mode |
| `--style` | Music style (required in custom mode) |
| `--title` | Song title (required in custom mode) |
| `--instrumental` | Generate instrumental |
| `--vocal-gender` | Vocal gender: male / female (custom mode only) |
| `--query` | Query task status |
| `--task-id` | Task ID (use with --query) |
