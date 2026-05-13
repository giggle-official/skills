# Talking-head CLI (wrapped API)

Create a talking-head video from one portrait **URL** and **exactly one of three drives**. Script: `scripts/tv_avatar_video.py`.

**Note**: JSON below explains fields—prefer the CLI so the script builds the body and polls.

## Gateway constraints

These limits come from the generation gateway; the CLI checks **non-empty `tts_script`**, **character cap**, and **`<break>`** syntax only (not audio duration or TTS playback length).

### `drive_mode = 1` (TTS)

| Rule | Detail |
|------|--------|
| `tts_script` | Required; must be **non-empty** after trim. |
| Voice source | Choose **exactly one**: **`voice_over_id`** (preset voice) **or** **`clone_audio.url`** (clone reference). Do **not** set both; do **not** use `drive_audio` in this mode (full clip lip-sync is **`drive_mode = 2`** only). |
| Copy length | At most **2700** characters. |
| Spoken duration | Total synthesized speech must be **≤ 180 seconds** (enforced server-side; trim copy or breaks if the job fails). |
| Pause tags | Insert `<break time="Xs"/>` where `X` is **0.1–99.9** seconds with **at most one decimal place** (e.g. `1.0`, `10`). Example: `欢迎来到<break time="1.0s"/>giggle` — roughly **1 second** silence after “to”, then continue with “giggle”. |

### `drive_mode = 2` (`drive_audio`)

| Rule | Detail |
|------|--------|
| Clip duration | **`drive_audio`** URL must point to audio **≤ 120 seconds** long (confirm before submit; the CLI does not probe remote duration). |

---

## 1) TTS + existing `voice_over_id`

`drive_mode`: **1**. Provide `tts_script` and `voice_over_id`; **do not** set `clone_audio`.

Example:

```json
{
  "drive_mode": 1,
  "image": { "url": "https://example.com/face.jpg" },
  "tts_script": "Welcome. This sample uses script-driven talking-head with catalog voice.",
  "voice_over_id": "zeeTdrCqbhpVKOucLtOKdhytM7rbJx5t"
}
```

CLI:

```bash
python scripts/tv_avatar_video.py run \
  --image-url "https://example.com/face.jpg" \
  --tts-script "Welcome. This sample uses script-driven talking-head with catalog voice." \
  --voice-over-id "zeeTdrCqbhpVKOucLtOKdhytM7rbJx5t"
```

---

## 2) TTS + `clone_audio` (reference / clone tone)

`drive_mode`: **1**. Provide `tts_script` and `clone_audio.url`; **do not** set `voice_over_id`. Optional `voice_speed` (example uses `1`).

Example:

```json
{
  "drive_mode": 1,
  "image": { "url": "https://example.com/face.jpg" },
  "tts_script": "Welcome. This sample uses script-driven talking-head with cloned reference audio.",
  "clone_audio": { "url": "https://example.com/reference_voice.mp3" },
  "voice_speed": 1
}
```

CLI:

```bash
python scripts/tv_avatar_video.py run \
  --image-url "https://example.com/face.jpg" \
  --tts-script "Welcome. This sample uses script-driven talking-head with cloned reference audio." \
  --clone-audio-url "https://example.com/reference_voice.mp3" \
  --voice-speed 1
```

---

## 3) Full audio drive (lip-sync)

`drive_mode`: **2**. Use `drive_audio.url`; **do not** combine with `tts_script` / `voice_over_id` / `clone_audio`.

Example:

```json
{
  "drive_mode": 2,
  "image": { "url": "https://example.com/face.jpg" },
  "drive_audio": { "url": "https://example.com/speech.mp3" }
}
```

CLI:

```bash
python scripts/tv_avatar_video.py run \
  --image-url "https://example.com/face.jpg" \
  --drive-audio-url "https://example.com/speech.mp3"
```

---

## Submit and query

**Submit** (successful example):

```json
{
  "code": 200,
  "msg": "success",
  "uuid": "...",
  "data": { "task_id": "53e147de-7f61-4bef-b13d-78e401aa32b2" }
}
```

**Query** (while running: fields depend on gateway; when finished):

```json
{
  "code": 200,
  "msg": "success",
  "uuid": "...",
  "data": {
    "task_id": "...",
    "urls": ["https://example.com/result.mp4"],
    "status": "completed",
    "err_msg": ""
  }
}
```

Output URL: **`data.urls[0]`**. The script prints that URL on stdout once `status == completed`.

---

## Subcommands

| Command | Meaning |
|---------|---------|
| `run` | Submit and poll to completion |
| `submit` | Submit only; print `task_id` on stdout |
| `query` | Resume polling by `task_id` (recovery after timeouts) |

### Common flags

| Flag | Meaning |
|------|---------|
| `--image-url` | Portrait URL (required) |
| `--timeout` / `--interval` | Max poll time / interval (seconds) |
| `--output PATH` | Download the rendered URL locally |
| `--json` | Print last query response JSON in full |
| `-q` | Quiet progress |
| `--base-url` | Per-invocation override of `GIGGLE_API_BASE` |

### `query`

```bash
python scripts/tv_avatar_video.py query --task-id "<task_id>" --timeout 1200
```

---

## Batch example

```bash
T1=$(python scripts/tv_avatar_video.py submit \
  --image-url "https://example.com/a.jpg" \
  --tts-script "Paragraph one" \
  --voice-over-id "<id>" -q)
T2=$(python scripts/tv_avatar_video.py submit \
  --image-url "https://example.com/b.jpg" \
  --tts-script "Paragraph two" \
  --voice-over-id "<id>" -q)

python scripts/tv_avatar_video.py query --task-id "$T1"
python scripts/tv_avatar_video.py query --task-id "$T2"
```
