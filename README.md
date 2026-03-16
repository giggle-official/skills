# Giggle Official Skills

English | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md) | [한국어](./README.ko.md) | [繁體中文](./README.zh-TW.md)

Central repository for AI generation skills powered by [Giggle.pro](https://giggle.pro/), including image, video, music, speech, scripts, and more.

## Install with `npx skills add`

```bash
# List skills from GitHub repository
npx skills add giggle-official/skills --list --full-depth

# Install a specific skill from GitHub repository
npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y

# Install from GitHub repository
npx skills add giggle-official/skills

# Local development (run in this repo directory)
npx skills add . --list --full-depth
```

## Highlights

- 🎨 **Multi-modal AI**: Image, video, music, speech, and script generation in one place.
- 🎬 **Video production**: Text-to-video, image-to-video, short films, drama, and MV workflows.
- 📝 **Story & script**: Jiang Wen–style screenplay generation with scene outlines and dialogue.
- 🔐 **Local-first**: Skills run on your machine; API key from system environment variable `GIGGLE_API_KEY`.

## Available skills

| Name | Description | Documentation | Run command |
|------|-------------|---------------|-------------|
| giggle-generation-image | Text-to-image and image-to-image. Supports Seedream, Midjourney, Nano Banana. Customize aspect ratio and resolution. | [SKILL.md](./skills/giggle-generation-image/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y` |
| giggle-generation-video | Text-to-video and image-to-video (start/end frame). Supports Grok, Sora2, Veo, Kling, etc. Customize model, duration, aspect ratio. | [SKILL.md](./skills/giggle-generation-video/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y` |
| giggle-generation-drama | Generate short films, drama, or narration videos from story. Supports episode, narration, and short-film modes. | [SKILL.md](./skills/giggle-generation-drama/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y` |
| giggle-generation-aimv | AI music videos (MV). Generate music from text prompts or custom lyrics, then create lyric videos with reference images. | [SKILL.md](./skills/giggle-generation-aimv/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y` |
| giggle-generation-music | Create AI music from text description, custom lyrics, or instrumental. Supports simplified, custom, and instrumental modes. | [SKILL.md](./skills/giggle-generation-music/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y` |
| giggle-generation-speech | Text-to-speech via Giggle.pro. Multiple voices, emotions, and speaking rates. | [SKILL.md](./skills/giggle-generation-speech/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y` |
| giggle-generation-scripts | Jiang Wen–style Chinese screenplay generation: synopsis, character bios, scene outlines, scene scripts with dialogue and staging. | [SKILL.md](./skills/giggle-generation-scripts/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y` |

## Quick verify

For example, list available TTS voices (requires `GIGGLE_API_KEY`):

```bash
cd skills/giggle-generation-speech
python3 scripts/text_to_audio_api.py --list-voices
```

## Giggle API Key (required)

Get your API key from [Giggle.pro](https://giggle.pro/) and set system environment variable:

```bash
export GIGGLE_API_KEY=your_api_key
```

All skills read `GIGGLE_API_KEY` from system environment.

```yaml:skills-data
skills:
  - name: giggle-generation-drama
    description: Use when the user wants to generate videos, shoot short films, or see available video styles. Triggers: short film, make video, shoot short, AI video, generate video from story, shoot video, I have a story idea, drama, narration video, cinematic video, what video styles are available.
    category: video
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y"
  - name: giggle-generation-aimv
    description: Use when the user wants to create AI music videos (MV)—including generating music from text prompts or using custom lyrics. Triggers: generate MV, music video, make video for this song, lyric video, create MV, AI music video, music+video, generate video from lyrics.
    category: video
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y"
  - name: giggle-generation-image
    description: Text-to-image and image-to-image. Use when the user needs to create or generate images. Use cases: (1) generate from text description, (2) generate from reference image, (3) customize model, aspect ratio, resolution. Triggers: generate image, draw, create image, AI art.
    category: image
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y"
  - name: giggle-generation-music
    description: Use when the user wants to create, generate, or compose music—whether text description, custom lyrics, or instrumental BGM. Triggers: generate music, write song, compose, make music, make a song, AI music, background music, compose for me, music with lyrics, instrumental, make beats.
    category: music
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y"
  - name: giggle-generation-scripts
    description: Jiang Wen–style Chinese screenplay generation based on common narrative pacing and dialogue mechanisms. For when the user asks to "generate screenplay", "write script", "create scenes", "output dialogue", "revise script", etc. Outputs synopsis, character bios, scene outlines, scene scripts with dialogue and staging. Can adjust era, character relations, conflict rhythm, and ending per user request.
    category: script
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y"
  - name: giggle-generation-speech
    description: Use when the user wants to generate speech, voice-over, or text-to-audio. Synthesizes text into AI speech via Giggle.pro TTS API. Triggers: generate speech, text-to-speech, TTS, voice-over, read this text, synthesize speech, I need voice-over.
    category: voice
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y"
  - name: giggle-generation-video
    description: Text-to-video and image-to-video (start/end frame). Use when the user needs to generate video, make short video, or text-to-video. Use cases: (1) generate video from text description, (2) generate video using reference image as start/end frame, (3) customize model, aspect ratio, duration, resolution. Triggers: generate video, text-to-video, image-to-video, AI video.
    category: video
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y"
```
