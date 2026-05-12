# Talking-head CLI (wrapped API)

Create a talking-head video from one portrait **URL** and **exactly one of three drives**. Script: `scripts/tv_avatar_video.py`.

**Note**: JSON below explains fields—prefer the CLI so the script builds the body and polls.

---

## 1) TTS + existing `voice_over_id`

`drive_mode`: **1**. Provide `tts_script` and `voice_over_id`; **do not** set `clone_audio`.

Example:

```json
{
  "drive_mode": 1,
  "image": { "url": "https://example.com/face.jpg" },
  "tts_script": "Welcome. This sample uses script-driven talking-head with catalog voice.",
  "voice_over_id": "zeeTdrCqbhpVKOucLtOKdhytM7rbJx5t",
  "mode_type": "1"
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
  "voice_speed": 1,
  "mode_type": "1"
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
  "drive_audio": { "url": "https://example.com/speech.mp3" },
  "mode_type": "1"
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
| `--mode-type` | Default `"1"` |
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
