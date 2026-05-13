---
name: giggle-generation-tv-avatar-video
description: "Talking-head video from image + driving audio: submit tasks via the wrapped generation API and poll for results; requests go through the Giggle gateway."
homepage: https://giggle.pro/
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

# Photo-driven talking-head video

> **Capability**: One **portrait image URL** plus **one of three drives** yields a **lip-sync talking-head video**.  
> **How it works**: The script calls the wrapped API (`x-auth` + `GIGGLE_API_KEY`), submits, then polls until `completed`; use `data.urls[0]` as the delivered video URL.

## How to run

Prefer `scripts/tv_avatar_video.py` instead of raw HTTP calls; it builds JSON, headers, and polling.

## For reviewers / auditors

The UX guidance below is for conversational wording only—not a substitute for security or compliance policies. Actual request host comes from `GIGGLE_API_BASE` (default `https://giggle.pro`).

## Tone when replying to end users

1. **Brief**: Say whether submission succeeded, rough wait time, and next step first.
2. **Plain language**: Avoid `drive_mode` / `task_id` unless the user asks.
3. **Secrets**: If env vars are missing, tell them to get an API Key from the site sidebar and set `GIGGLE_API_KEY`; never ask them to paste keys in chat.
4. **Errors**: One sentence + whether retrying makes sense; on poll timeouts, mention `query --task-id`.
5. **After submit**: These jobs commonly take **several minutes**, depending on copy/audio length.

**Example line after submit**: “Your render is queued; it usually takes a few minutes. I’ll send the video link when it’s ready.”

## Preset voice list（预设声音列表）

- Refer to bundled voices as the **preset voice list**（预设声音列表）。Do **not** call them 「系统声音」or “system voices” in user-facing wording.
- When the user asks to **view or list the preset voice list**（查看 / 罗列预设声音列表）: open [references/voices_catalog.md](references/voices_catalog.md) and **list the voices defined there**—each numbered block has display **name**, **`voiceoverId`** (pass as API `voice_over_id` where applicable), **tags**, and EN/ZH descriptions. Prefer showing **name + `voiceoverId`** for every entry when they want the full catalogue; shorten or filter only if they ask.

## Content limits (gateway)

Summary — full tables in [references/tv_avatar_video.md](references/tv_avatar_video.md):

- **`drive_mode = 1`**: Non-empty **`tts_script`**; exactly one of **`voice_over_id`** or **`clone_audio`** (preset vs clone—not **`drive_audio`**). Copy ≤ **2700** characters; synthesized speech ≤ **180** seconds (server-checked). Optional pauses: `<break time="Xs"/>` with **X ∈ [0.1, 99.9]** and one decimal max (example: `欢迎来到<break time="1.0s"/>giggle`).
- **`drive_mode = 2`**: **`drive_audio`** clip ≤ **120** seconds.

## Prerequisites

- Python 3.8+
- `GIGGLE_API_KEY` — see [references/credentials.md](references/credentials.md)
- Portrait image, clone reference audio, or drive audio must all be **public HTTPS URLs** (this skill bundle does not provide upload hosting)

```bash
pip install -r {baseDir}/scripts/requirements.txt
```

## Agent workflow

1. **`run`** (default): Submit and poll to completion.
2. **`submit`**: Submit only, print `task_id`—useful for parallel batches.
3. **`query`**: After **`run`** times out, keep polling from a known `task_id`.

```
New jobs     → tv_avatar_video.py run ...
After timeout → tv_avatar_video.py query --task-id <task_id> [--timeout 1200]
```

**Do not** treat queued / processing tasks as final outputs for users.

## Modules

| Script | Docs |
|--------|------|
| `scripts/tv_avatar_video.py` | [references/tv_avatar_video.md](references/tv_avatar_video.md) |
| `scripts/shared/` | HTTP client, reads `GIGGLE_API_KEY` |

## See also

- [references/tv_avatar_video.md](references/tv_avatar_video.md) — three drive modes + JSON + CLI samples
- [references/voices_catalog.md](references/voices_catalog.md) — preset voice list（预设声音列表）with `voiceoverId` values
- [references/credentials.md](references/credentials.md) — API key / env vars
- [references/error_handling.md](references/error_handling.md) — common failures and recovery
