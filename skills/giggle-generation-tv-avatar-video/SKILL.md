---
name: giggle-generation-tv-avatar-video
description: "Talking-head video from image + driving audio: submit tasks via the wrapped generation API and poll for results; requests go through the Giggle gateway."
homepage: https://giggle.pro/
repository: https://github.com/giggle-official/skills
license: Apache-2.0
metadata:
  tags: talking-head, photo-avatar, lip-sync, tts, clone-voice, api, en, giggle
  vendor: giggle
  locale: en
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
      description: After signing in at giggle.pro → API Key in the left sidebar
    - name: GIGGLE_API_BASE
      required: false
      description: Optional; default https://giggle.pro. Point at your own gateway for local integration.
  endpoints:
    - https://giggle.pro/api/v1/generation/tv-avatar-video
    - https://giggle.pro/api/v1/generation/task/query
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
- [references/credentials.md](references/credentials.md) — API key / env vars
- [references/error_handling.md](references/error_handling.md) — common failures and recovery
