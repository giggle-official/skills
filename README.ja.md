# Giggle Official Skills

[English](./README.md) | [简体中文](./README.zh-CN.md) | 日本語 | [한국어](./README.ko.md) | [繁體中文](./README.zh-TW.md)

[Giggle.pro](https://giggle.pro/) をベースにした AI 生成スキルライブラリ。画像、動画、音楽、音声、ボイスクローン、脚本などをカバーしています。

## `npx skills add` でインストール

```bash
# GitHub リポジトリから全スキルを一覧表示
npx skills add giggle-official/skills --list --full-depth

# GitHub リポジトリから指定スキルをインストール
npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y

# GitHub リポジトリからすべてインストール
npx skills add giggle-official/skills

# ローカル開発（本リポジトリのディレクトリで実行）
npx skills add . --list --full-depth
```

## 特徴

- 🎨 **マルチモーダル AI**：画像、動画、音楽、音声、ボイスクローン、脚本の生成を一括で対応。
- 🎬 **動画制作**：文生動画、画像生動画、ショートフィルム、短編ドラマ、MV の全フローをサポート。
- 📝 **ストーリーと脚本**：姜文風のナラティブスタイルで、分場アウトラインと台本を生成。
- 🔐 **ローカル優先**：スキルはローカルで実行。API Key はシステム環境変数 `GIGGLE_API_KEY` から読み取り。

## 利用可能なスキル

| 名前 | 説明 | ドキュメント | インストールコマンド |
|------|------|------|----------|
| giggle-generation-image | 文生図と図生図。Seedream、Midjourney、Nano Banana に対応。アスペクト比と解像度をカスタマイズ可能。 | [SKILL.md](./skills/giggle-generation-image/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y` |
| giggle-generation-video | 文生動画と図生動画（初フレーム/終フレーム）。Grok、Sora2、Veo、Kling などに対応。モデル、長さ、アスペクト比をカスタマイズ可能。 | [SKILL.md](./skills/giggle-generation-video/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y` |
| giggle-generation-drama | ストーリーからショートフィルム、短編ドラマ、解説動画を生成。エピソード、解説、ショートフィルムの 3 モードに対応。 | [SKILL.md](./skills/giggle-generation-drama/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y` |
| giggle-generation-aimv | AI ミュージックビデオ（MV）。テキストプロンプトやカスタム歌詞から音楽を生成し、参考画像と組み合わせて歌詞動画を作成。 | [SKILL.md](./skills/giggle-generation-aimv/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y` |
| giggle-generation-music | テキスト説明、カスタム歌詞、またはインストゥルメンタルから AI 音楽を作成。簡易、カスタム、インストゥルメンタルの 3 モードに対応。 | [SKILL.md](./skills/giggle-generation-music/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y` |
| giggle-generation-speech | Giggle.pro の文転音でテキストを AI 音声に合成。複数の音色、感情、話速に対応。 | [SKILL.md](./skills/giggle-generation-speech/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y` |
| giggle-voice-clone | ボイスクローン。参考音声 URL から声をクローンし、その声でテキストを合成。 | [SKILL.md](./skills/giggle-voice-clone/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-voice-clone -y` |
| giggle-generation-scripts | 姜文風中国語脚本生成：あらすじ、人物紹介、分場アウトライン、台本と場面演出を含む分場脚本。 | [SKILL.md](./skills/giggle-generation-scripts/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y` |

## クイック検証

例：利用可能な TTS 音色を確認（`GIGGLE_API_KEY` の設定が必要）：

```bash
cd skills/giggle-generation-speech
python3 scripts/text_to_audio_api.py --list-voices
```

## Giggle API Key（必須）

[Giggle.pro](https://giggle.pro/) で API Key を取得し、システム環境変数に設定してください：

```bash
export GIGGLE_API_KEY=your_api_key
```

すべてのスキルはシステム環境変数から `GIGGLE_API_KEY` を読み取ります。

```yaml:skills-data
skills:
  - name: "短編ドラマ"
    value: "giggle-generation-drama"
    description: "ユーザーが動画の生成、ショートフィルムの撮影、または利用可能な動画スタイルの確認を希望する際に使用。トリガーワード：ショートフィルム、動画制作、AI動画、ストーリーからの動画生成、短編ドラマ、解説動画、映画風動画。"
    category: video
    version: "0.0.1"
  - name: "音楽MV"
    value: "giggle-generation-aimv"
    description: "ユーザーが AI ミュージックビデオ（MV）の作成を希望する際に使用。テキストプロンプトから音楽を生成するか、カスタム歌詞を使用。トリガーワード：MV生成、ミュージックビデオ、歌詞動画、AI MV、歌詞から動画生成。"
    category: video
    version: "0.0.1"
  - name: "画像生成"
    value: "giggle-generation-image"
    description: "文生図と図生図をサポート。ユーザーが画像の作成・生成を必要とする際に使用。(1) テキスト説明から生成、(2) 参考画像から生成、(3) モデル、アスペクト比、解像度のカスタマイズ。トリガーワード：画像生成、AIアート。"
    category: image
    version: "0.0.1"
  - name: "音楽生成"
    value: "giggle-generation-music"
    description: "ユーザーが音楽の作成、生成、作曲を希望する際に使用。テキスト説明、カスタム歌詞、インストゥルメンタル BGM のいずれにも対応。トリガーワード：音楽生成、作曲、AI音楽、BGM、歌詞付き音楽、beats 制作。"
    category: music
    version: "0.0.1"
  - name: "脚本生成"
    value: "giggle-generation-scripts"
    description: "姜文映画のナラティブ推進と台本の仕組みに基づき中国語脚本を生成。脚本生成、分場作成、台本、剧本修正などの意図の際に使用。あらすじ、人物紹介、分場アウトライン、台本と演技・演出を含む分場脚本を出力。時代背景、人物関係、衝突リズム、結末の調整に対応。"
    category: script
    version: "0.0.1"
  - name: "音声・吹替"
    value: "giggle-generation-speech"
    description: "ユーザーが音声生成、吹替、テキスト読み上げを希望する際に使用。Giggle.pro 文転音 API でテキストを AI 音声に合成。トリガーワード：音声生成、文転音、TTS、吹替、合成音声。"
    category: voice
    version: "0.0.1"
  - name: "ボイスクローン"
    value: "giggle-voice-clone"
    description: "ユーザーが音声サンプルから声をクローンする際に使用。参考音声 URL を voice-clone に渡し、その声でテキストを合成。トリガーワード：ボイスクローン、声のクローン、音声から声をクローン。"
    category: voice
    version: "0.0.1"
  - name: "動画生成"
    value: "giggle-generation-video"
    description: "文生動画と図生動画（初フレーム/終フレーム）をサポート。ユーザーが動画生成、ショート動画制作、文転動画を必要とする際に使用。(1) テキスト説明から動画生成、(2) 参考画像を初/終フレームとして動画生成、(3) モデル、アスペクト比、長さ、解像度のカスタマイズ。トリガーワード：動画生成、文生動画、図生動画、AI動画、text-to-video、image-to-video。"
    category: video
    version: "0.0.1"
```
