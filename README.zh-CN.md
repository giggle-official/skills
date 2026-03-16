# Giggle Official Skills

[English](./README.md) | 简体中文

基于 [Giggle.pro](https://giggle.pro/) 的 AI 生成技能库，涵盖图像、视频、音乐、语音、剧本等。

## 使用 `npx skills add` 安装

```bash
# 从 GitHub 仓库列出所有技能
npx skills add giggle-official/skills --list --full-depth

# 从 GitHub 仓库安装指定技能
npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y

# 从 GitHub 仓库安装全部
npx skills add giggle-official/skills

# 本地开发（在本仓库目录执行）
npx skills add . --list --full-depth
```

## 特色

- 🎨 **多模态 AI**：图像、视频、音乐、语音、剧本生成一站搞定。
- 🎬 **视频创作**：文生视频、图生视频、短片、短剧、MV 全流程支持。
- 📝 **故事与剧本**：姜文式叙事风格，分场大纲与对白剧本生成。
- 🔐 **本地优先**：技能在本地运行，API Key 从系统环境变量 `GIGGLE_API_KEY` 读取。

## 可用技能

| 名称 | 说明 | 文档 | 安装命令 |
|------|------|------|----------|
| giggle-generation-image | 文生图与图生图。支持 Seedream、Midjourney、Nano Banana。可自定义画幅比例与分辨率。 | [SKILL.md](./skills/giggle-generation-image/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y` |
| giggle-generation-video | 文生视频与图生视频（首帧/尾帧）。支持 Grok、Sora2、Veo、Kling 等。可自定义模型、时长、画幅比例。 | [SKILL.md](./skills/giggle-generation-video/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y` |
| giggle-generation-drama | 根据故事生成短片、短剧或解说视频。支持剧集、解说、短片三种模式。 | [SKILL.md](./skills/giggle-generation-drama/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y` |
| giggle-generation-aimv | AI 音乐视频（MV）。根据文字描述或自定义歌词生成音乐，再结合参考图生成歌词视频。 | [SKILL.md](./skills/giggle-generation-aimv/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y` |
| giggle-generation-music | 根据文字描述、自定义歌词或纯乐器创建 AI 音乐。支持简化、自定义、纯音乐三种模式。 | [SKILL.md](./skills/giggle-generation-music/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y` |
| giggle-generation-speech | 通过 Giggle.pro 文转音，将文本合成为 AI 语音。支持多种音色、情绪与语速。 | [SKILL.md](./skills/giggle-generation-speech/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y` |
| giggle-generation-scripts | 姜文式中文剧本生成：故事梗概、人物小传、分场大纲、含对白与场面调度的分场剧本。 | [SKILL.md](./skills/giggle-generation-scripts/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y` |

## 快速验证

例如，查看可用 TTS 音色（需配置 `GIGGLE_API_KEY`）：

```bash
cd skills/giggle-generation-speech
python3 scripts/text_to_audio_api.py --list-voices
```

## Giggle API Key（必填）

前往 [Giggle.pro](https://giggle.pro/) 获取 API Key，并设置系统环境变量：

```bash
export GIGGLE_API_KEY=your_api_key
```

所有技能从系统环境变量读取 `GIGGLE_API_KEY`。

```yaml:skills-data
skills:
  - name: giggle-generation-drama
    description: 当用户希望生成视频、拍摄短片或查看可用视频风格时使用此技能。触发词：短片、制作视频、拍短片、AI视频、根据故事生成视频、拍视频、我有故事想法、短剧、解说视频、电影感视频、有哪些视频风格。
    category: video
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y"
  - name: giggle-generation-aimv
    description: 当用户希望创建 AI 音乐视频（MV）时使用此技能——包括根据文字提示生成音乐或使用自定义歌词。触发词：生成 MV、音乐视频、为这首歌做视频、歌词视频、创建 MV、AI 音乐视频、音乐+视频、根据歌词生成视频。
    category: video
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y"
  - name: giggle-generation-image
    description: 支持文生图和图生图。当用户需要创建或生成图像时使用。使用场景：(1) 根据文字描述生成，(2) 使用参考图生成，(3) 自定义模型、画幅比例、分辨率。触发词：生成图片、画画、创建图片、AI 艺术图
    category: image
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y"
  - name: giggle-generation-music
    description: 当用户希望创建、生成或创作音乐时使用此技能——无论是文字描述、自定义歌词，还是纯乐器背景音乐。触发词：生成音乐、写歌、创作歌曲、制作音乐、做一首歌、AI 音乐、背景音乐、为我作曲、带歌词的音乐、纯音乐、做 beats。
    category: music
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y"
  - name: giggle-generation-scripts
    description: 基于姜文电影常见的叙事推进与对白机制生成中文剧本内容。用于用户提出"生成剧本""写剧本""做分场""出对白稿""改剧本"或同类意图时，包括：根据题材输出故事梗概、人物小传、分场大纲、分场剧本（含对白、动作、场面调度提示），并可按用户要求调整时代背景、人物关系、冲突节奏与结局走向。
    category: script
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y"
  - name: giggle-generation-speech
    description: 当用户希望生成语音、配音或文字转音频时使用此技能。通过 Giggle.pro 文转音 API 将文本合成为 AI 语音。触发词：生成语音、文转音、文字转语音、配音、TTS、朗读这段文字、把这段文字读出来、合成语音、我需要一段配音。
    category: voice
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y"
  - name: giggle-generation-video
    description: 支持文生视频和图生视频（首帧/尾帧）。当用户需要生成视频、制作短视频、文字转视频时使用。使用场景：(1) 根据文字描述生成视频，(2) 使用参考图作为首帧/尾帧生成视频，(3) 自定义模型、画幅比例、时长、分辨率。触发词：生成视频、文生视频、图生视频、AI 视频、text-to-video、image-to-video。
    category: video
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y"
```
