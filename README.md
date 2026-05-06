# Giggle Official Skills

English | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md) | [한국어](./README.ko.md) | [繁體中文](./README.zh-TW.md)

Central repository for AI generation skills powered by [Giggle.pro](https://giggle.pro/), including image, video, music, speech, voice clone, scripts, and more.

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

- 🎨 **Multi-modal AI**: Image, video, music, speech, voice clone, and script generation in one place.
- 🎬 **Video production**: Text-to-video, image-to-video, short films, drama, and MV workflows.
- 📝 **Story & script**: Jiang Wen–style screenplay generation with scene outlines and dialogue.
- 🔐 **Local-first**: Skills run on your machine; API key from system environment variable `GIGGLE_API_KEY`.

## Available skills

| Name | Description | Documentation | Run command |
|------|-------------|---------------|-------------|
| giggle-generation-image | Text-to-image and image-to-image. Supports Seedream, Midjourney, Nano Banana. Customize aspect ratio and resolution. | [SKILL.md](./skills/giggle-generation-image/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y` |
| giggle-generation-video | Supports text-to-video and image-to-video conversion (start frame/end frame). Suitable for users who need to convert text to video or images to video. | [SKILL.md](./skills/giggle-generation-video/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y` |
| giggle-seedance2-gen | Seedance 2.0 Pro/Fast video via Giggle API: text-to-video, image-to-video, and omni (multi-modal), with prompt-optimization guidance. Triggers: Seedance, AI video, text/image to video. | [SKILL.md](./skills/giggle-seedance2-gen/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-seedance2-gen -y` |
| giggle-generation-drama | Used when users want to generate videos, shoot short films, or view available video styles. Triggers: Short film, Make video, Shoot short film, AI video, Generate video from story, Short drama, Narrated video, Cinematic video, Available video styles | [SKILL.md](./skills/giggle-generation-drama/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y` |
| giggle-generation-aimv | AI music videos (MV). Generate music from text prompts or custom lyrics, then create lyric videos with reference images. | [SKILL.md](./skills/giggle-generation-aimv/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y` |
| giggle-generation-music | Create AI music from text description, custom lyrics, or instrumental. Supports simplified, custom, and instrumental modes. | [SKILL.md](./skills/giggle-generation-music/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y` |
| giggle-generation-speech | Text-to-speech via Giggle.pro. Multiple voices, emotions, and speaking rates. | [SKILL.md](./skills/giggle-generation-speech/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y` |
| giggle-voice-clone | Clone voice from audio URL. Submit reference audio, get cloned voice, then synthesize text with it. | [SKILL.md](./skills/giggle-voice-clone/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-voice-clone -y` |
| giggle-generation-scripts | Jiang Wen–style Chinese screenplay generation: synopsis, character bios, scene outlines, scene scripts with dialogue and staging. | [SKILL.md](./skills/giggle-generation-scripts/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y` |

## Quick verify

For example, list available TTS voices (requires `GIGGLE_API_KEY`):

```bash
cd skills/giggle-generation-speech
python3 scripts/text_to_audio_api.py --list-voices
```

## Giggle API Key (required)

Log in to [giggle.pro](https://giggle.pro/). On the **main site**, open the **left sidebar** → **API Key** (**API 密钥**) to create or copy your key. Then set the system environment variable:

```bash
export GIGGLE_API_KEY=your_api_key
```

All skills read `GIGGLE_API_KEY` from system environment.

```yaml:skills-data
skills:
  - name: "Drama"
    value: "giggle-generation-drama"
    description: "Used when users want to generate videos, shoot short films, or view available video styles. Triggers: Short film, Make video, Shoot short film, AI video, Generate video from story, Short drama, Narrated video, Cinematic video, Available video styles"
    category: video
    version: "0.0.1"
  - name: "Music MV"
    value: "giggle-generation-aimv"
    description: "Use when the user wants to create AI music videos (MV)—including generating music from text prompts or using custom lyrics. Triggers: generate MV, music video, make video for this song, lyric video, create MV, AI music video, music+video, generate video from lyrics."
    category: video
    version: "0.0.1"
  - name: "Image generation"
    value: "giggle-generation-image"
    description: "Text-to-image and image-to-image. Use when the user needs to create or generate images. Use cases: (1) generate from text description, (2) generate from reference image, (3) customize model, aspect ratio, resolution. Triggers: generate image, draw, create image, AI art."
    category: image
    version: "0.0.1"
  - name: "Music generation"
    value: "giggle-generation-music"
    description: "Use when the user wants to create, generate, or compose music—whether text description, custom lyrics, or instrumental BGM. Triggers: generate music, write song, compose, make music, make a song, AI music, background music, compose for me, music with lyrics, instrumental, make beats."
    category: music
    version: "0.0.1"
  - name: "Script generation"
    value: "giggle-generation-scripts"
    description: "Jiang Wen–style Chinese screenplay generation based on common narrative pacing and dialogue mechanisms. For when the user asks to generate screenplay, write script, create scenes, output dialogue, revise script, etc. Outputs synopsis, character bios, scene outlines, scene scripts with dialogue and staging. Can adjust era, character relations, conflict rhythm, and ending per user request."
    category: script
    version: "0.0.1"
  - name: "Voice"
    value: "giggle-generation-speech"
    description: "Use when the user wants to generate speech, voice-over, or text-to-audio. Synthesizes text into AI speech via Giggle.pro TTS API. Triggers: generate speech, text-to-speech, TTS, voice-over, read this text, synthesize speech, I need voice-over."
    category: voice
    version: "0.0.1"
  - name: "Voice Clone"
    value: "giggle-voice-clone"
    description: "Use when the user wants to clone a voice from an audio sample. Pass reference audio URL to voice-clone, then synthesizes text with that voice via Giggle.pro. Triggers: voice clone, clone my voice, clone voice from audio."
    category: voice
    version: "0.0.1"
  - name: "Video generation"
    value: "giggle-generation-video"
    description: "Supports text-to-video and image-to-video conversion (start frame/end frame). Suitable for users who need to convert text to video or images to video."
    category: video
    version: "0.0.1"
  - name: "Video generation (Seedance 2.0)"
    value: "giggle-seedance2-gen"
    description: "Generate AI videos with Seedance 2.0 (Pro/Fast) via Giggle API: text-to-video, image-to-video, omni multi-modal. Optimize prompts in the user's language, then call the API. Triggers: generate video, AI video, seedance, image to video, text to video, video generation."
    category: video
    version: "1.0.0"
  - name: "Image Generation (gpt-image-2)"
    value: "giggle-gpt-image-2"
    description: "Helps users generate high-quality prompts suitable for GPT-Image-2, and directly calls the Giggle API to generate images using `gpt-image-2-fast` after the prompt is created."
    category: image
    version: "0.0.1"
```
