# Giggle Official Skills

[English](./README.md) | 简体中文 | [日本語](./README.ja.md) | [한국어](./README.ko.md) | [繁體中文](./README.zh-TW.md)

基于 [Giggle.pro](https://giggle.pro/) 的 AI 生成技能库，涵盖图像、视频、音乐、语音、声音克隆、剧本等。

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

- 🎨 **多模态 AI**：图像、视频、音乐、语音、声音克隆、剧本生成一站搞定。
- 🎬 **视频创作**：文生视频、图生视频、短片、短剧、MV 全流程支持。
- 📝 **故事与剧本**：姜文式叙事风格，分场大纲与对白剧本生成。
- 🔐 **本地优先**：技能在本地运行，API Key 从系统环境变量 `GIGGLE_API_KEY` 读取。

## 可用技能


| 名称                        | 说明                                                         | 文档                                                      | 安装命令                                                                                      |
| ------------------------- | ---------------------------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| giggle-generation-image   | 文生图与图生图。支持 Seedream、Midjourney、Nano Banana。可自定义画幅比例与分辨率。   | [SKILL.md](./skills/giggle-generation-image/SKILL.md)   | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y`   |
| giggle-generation-video   | 支持文生视频与图生视频（首帧/尾帧）。适合需要将文本或图片转为视频的用户。 | [SKILL.md](./skills/giggle-generation-video/SKILL.md)   | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y`   |
| giggle-seedance2-gen      | 通过 Giggle API 使用 Seedance 2.0（Pro/Fast）：文生视频、图生视频、多模态 omni；含 Seedance 提示词优化流程。触发词：Seedance、AI 视频、文生视频、图生视频。 | [SKILL.md](./skills/giggle-seedance2-gen/SKILL.md)      | `npx skills add giggle-official/skills --full-depth --skill giggle-seedance2-gen -y`      |
| giggle-generation-drama   | 适用于希望生成视频、拍摄短片或查看可用视频风格的用户。触发词：短片、制作视频、拍短片、AI 视频、根据故事生成视频、短剧、解说视频、电影感视频、可用视频风格 | [SKILL.md](./skills/giggle-generation-drama/SKILL.md)   | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y`   |
| giggle-generation-aimv    | AI 音乐视频（MV）。根据文字描述或自定义歌词生成音乐，再结合参考图生成歌词视频。                 | [SKILL.md](./skills/giggle-generation-aimv/SKILL.md)    | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y`    |
| giggle-generation-music   | 根据文字描述、自定义歌词或纯乐器创建 AI 音乐。支持简化、自定义、纯音乐三种模式。                 | [SKILL.md](./skills/giggle-generation-music/SKILL.md)   | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y`   |
| giggle-generation-speech  | 通过 Giggle.pro 文转音，将文本合成为 AI 语音。支持多种音色、情绪与语速。               | [SKILL.md](./skills/giggle-generation-speech/SKILL.md)  | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y`  |
| giggle-voice-clone        | 声音克隆。从参考音频 URL 克隆声音，再用克隆音色合成文本。                               | [SKILL.md](./skills/giggle-voice-clone/SKILL.md)        | `npx skills add giggle-official/skills --full-depth --skill giggle-voice-clone -y`        |
| giggle-generation-scripts | 姜文式中文剧本生成：故事梗概、人物小传、分场大纲、含对白与场面调度的分场剧本。                    | [SKILL.md](./skills/giggle-generation-scripts/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y` |


## 快速验证

例如，查看可用 TTS 音色（需配置 `GIGGLE_API_KEY`）：

```bash
cd skills/giggle-generation-speech
python3 scripts/text_to_audio_api.py --list-voices
```

## Giggle API Key（必填）

登录 [giggle.pro](https://giggle.pro/)，在**主页左侧边栏**打开 **「API 密钥」**（或 **API Key**）板块，创建或复制密钥，然后设置系统环境变量：

```bash
export GIGGLE_API_KEY=your_api_key
```

所有技能从系统环境变量读取 `GIGGLE_API_KEY`。

```yaml:skills-data
skills:
  - name: "短片"
    value: "giggle-generation-drama"
    description: "适用于希望生成视频、拍摄短片或查看可用视频风格的用户。触发词：短片、制作视频、拍短片、AI 视频、根据故事生成视频、短剧、解说视频、电影感视频、可用视频风格"
    category: video
    version: "0.0.1"
  - name: "音乐MV"
    value: "giggle-generation-aimv"
    description: "当用户希望创建 AI 音乐视频（MV）时使用此技能——包括根据文字提示生成音乐或使用自定义歌词。触发词：生成 MV、音乐视频、为这首歌做视频、歌词视频、创建 MV、AI 音乐视频、音乐+视频、根据歌词生成视频。"
    category: video
    version: "0.0.1"
  - name: "图片生成"
    value: "giggle-generation-image"
    description: "支持文生图和图生图。当用户需要创建或生成图像时使用。使用场景：(1) 根据文字描述生成，(2) 使用参考图生成，(3) 自定义模型、画幅比例、分辨率。触发词：生成图片、画画、创建图片、AI 艺术图。"
    category: image
    version: "0.0.1"
  - name: "音乐生成"
    value: "giggle-generation-music"
    description: "当用户希望创建、生成或创作音乐时使用此技能——无论是文字描述、自定义歌词，还是纯乐器背景音乐。触发词：生成音乐、写歌、创作歌曲、制作音乐、做一首歌、AI 音乐、背景音乐、为我作曲、带歌词的音乐、纯音乐、做 beats。"
    category: music
    version: "0.0.1"
  - name: "剧本生成"
    value: "giggle-generation-scripts"
    description: "基于姜文电影常见的叙事推进与对白机制生成中文剧本内容。用于用户提出生成剧本、写剧本、做分场、出对白稿、改剧本或同类意图时，包括：根据题材输出故事梗概、人物小传、分场大纲、分场剧本（含对白、动作、场面调度提示），并可按用户要求调整时代背景、人物关系、冲突节奏与结局走向。"
    category: script
    version: "0.0.1"
  - name: "配音"
    value: "giggle-generation-speech"
    description: "当用户希望生成语音、配音或文字转音频时使用此技能。通过 Giggle.pro 文转音 API 将文本合成为 AI 语音。触发词：生成语音、文转音、文字转语音、配音、TTS、朗读这段文字、把这段文字读出来、合成语音、我需要一段配音。"
    category: voice
    version: "0.0.1"
  - name: "声音克隆"
    value: "giggle-voice-clone"
    description: "当用户希望从音频样本克隆声音时使用此技能。传入参考音频 URL 至 voice-clone，再用克隆音色合成文本。触发词：声音克隆、复刻声音、克隆声音、克隆我的声音、从音频克隆声音。"
    category: voice
    version: "0.0.1"
  - name: "视频生成"
    value: "giggle-generation-video"
    description: "支持文生视频与图生视频（首帧/尾帧）。适合需要将文本或图片转为视频的用户。"
    category: video
    version: "0.0.1"
  - name: "视频生成（Seedance 2.0）"
    value: "giggle-seedance2-gen"
    description: "giggle.pro 上 Seedance 2.0 成片 + 提示词工程（references/prompts）。按 Seedance 范式优化提示词后仅走 API。触发词：生成视频、视频提示词、AI 视频、seedance、omni、多模态、短剧、广告视频、首帧图、角色参考。（用户口头的「即梦」习惯仍仅交付 giggle.pro。）"
    category: video
    version: "1.1.0"
  - name: "图片生成(gpt-image-2)"
    value: "giggle-gpt-image-2"
    description: "帮助用户生成适合 GPT-Image-2 的高质量提示词，并在生成提示词后直接调用 Giggle API 使用 `gpt-image-2-fast` 生成图片。"
    category: image
    version: "0.0.1"
```

