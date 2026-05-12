# Photo-driven talking-head video (Giggle)

Uses Giggle’s wrapped **photo-driven talking-head** flow: portrait image URL + **TTS (voice ID / clone audio)** or **full-drive audio**, submit job, poll to completion, return the output URL.

Follows the [Agent Skills](https://agentskills.io/specification) idea—load `SKILL.md` in Cursor, Claude Code, etc.

## Feature summary

- Three mutually exclusive drives: **TTS + voice_over_id**, **TTS + clone_audio.url**, **drive_audio.url (lip-sync)**
- Subcommands: `run` (default), `submit`, `query`
- Auth: **`x-auth`** header; secret from **`GIGGLE_API_KEY`** (sign in at [giggle.pro](https://giggle.pro/), sidebar **API Key**)

## Quick start

From this directory:

```bash
export GIGGLE_API_KEY="<your-secret-key>"
pip install -r scripts/requirements.txt

python scripts/tv_avatar_video.py run \
  --image-url "https://example.com/portrait.jpg" \
  --tts-script "Welcome." \
  --voice-over-id "<voice_over_id>"
```

Optional override for self-hosted/local gateway:

```bash
export GIGGLE_API_BASE="http://localhost:8090"
```

Request payloads and CLI details live in [references/tv_avatar_video.md](references/tv_avatar_video.md); agent flow lives in [SKILL.md](SKILL.md).

## Layout

```
giggle-generation-tv-avatar-video/
├── SKILL.md
├── README.md
├── LICENSE.txt
├── references/
│   ├── tv_avatar_video.md
│   ├── credentials.md
│   ├── error_handling.md
│   └── voices_catalog.md
└── scripts/
    ├── tv_avatar_video.py
    ├── requirements.txt
    └── shared/
```

## License

[LICENSE.txt](LICENSE.txt)
