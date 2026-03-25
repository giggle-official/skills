# Giggle Official Skills

[English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md) | [한국어](./README.ko.md) | 繁體中文

基於 [Giggle.pro](https://giggle.pro/) 的 AI 生成技能庫，涵蓋圖像、影片、音樂、語音、聲音克隆、劇本等。

## 使用 `npx skills add` 安裝

```bash
# 從 GitHub 倉庫列出所有技能
npx skills add giggle-official/skills --list --full-depth

# 從 GitHub 倉庫安裝指定技能
npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y

# 從 GitHub 倉庫安裝全部
npx skills add giggle-official/skills

# 本地開發（在本倉庫目錄執行）
npx skills add . --list --full-depth
```

## 特色

- 🎨 **多模態 AI**：圖像、影片、音樂、語音、聲音克隆、劇本生成一站搞定。
- 🎬 **影片創作**：文生影片、圖生影片、短片、短劇、MV 全流程支援。
- 📝 **故事與劇本**：姜文式敘事風格，分場大綱與對白劇本生成。
- 🔐 **本地優先**：技能在本地執行，API Key 從系統環境變數 `GIGGLE_API_KEY` 讀取。

## 可用技能

| 名稱 | 說明 | 文件 | 安裝指令 |
|------|------|------|----------|
| giggle-generation-image | 文生圖與圖生圖。支援 Seedream、Midjourney、Nano Banana。可自訂畫幅比例與解析度。 | [SKILL.md](./skills/giggle-generation-image/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y` |
| giggle-generation-video | 支援文字轉影片與圖片轉影片（首幀/尾幀）。適合需要將文字或圖片轉成影片的使用者。 | [SKILL.md](./skills/giggle-generation-video/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y` |
| giggle-generation-drama | 適用於想生成影片、拍攝短片或查看可用影片風格的使用者。觸發詞：短片、製作影片、拍短片、AI 影片、依故事生成影片、短劇、旁白影片、電影感影片、可用影片風格 | [SKILL.md](./skills/giggle-generation-drama/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y` |
| giggle-generation-aimv | AI 音樂影片（MV）。根據文字描述或自訂歌詞生成音樂，再結合參考圖生成歌詞影片。 | [SKILL.md](./skills/giggle-generation-aimv/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y` |
| giggle-generation-music | 根據文字描述、自訂歌詞或純樂器建立 AI 音樂。支援簡化、自訂、純音樂三種模式。 | [SKILL.md](./skills/giggle-generation-music/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y` |
| giggle-generation-speech | 透過 Giggle.pro 文轉音，將文字合成為 AI 語音。支援多種音色、情緒與語速。 | [SKILL.md](./skills/giggle-generation-speech/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y` |
| giggle-voice-clone | 聲音克隆。從參考音訊 URL 克隆聲音，再用克隆音色合成文字。 | [SKILL.md](./skills/giggle-voice-clone/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-voice-clone -y` |
| giggle-generation-scripts | 姜文式中文劇本生成：故事梗概、人物小傳、分場大綱、含對白與場面調度的分場劇本。 | [SKILL.md](./skills/giggle-generation-scripts/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y` |

## 快速驗證

例如，查看可用 TTS 音色（需配置 `GIGGLE_API_KEY`）：

```bash
cd skills/giggle-generation-speech
python3 scripts/text_to_audio_api.py --list-voices
```

## Giggle API Key（必填）

前往 [Giggle.pro](https://giggle.pro/) 取得 API Key，並設定系統環境變數：

```bash
export GIGGLE_API_KEY=your_api_key
```

所有技能從系統環境變數讀取 `GIGGLE_API_KEY`。

```yaml:skills-data
skills:
  - name: "短片"
    value: "giggle-generation-drama"
    description: "適用於想生成影片、拍攝短片或查看可用影片風格的使用者。觸發詞：短片、製作影片、拍短片、AI 影片、依故事生成影片、短劇、旁白影片、電影感影片、可用影片風格"
    category: video
    version: "0.0.1"
  - name: "音樂MV"
    value: "giggle-generation-aimv"
    description: "當使用者希望建立 AI 音樂影片（MV）時使用此技能——包括根據文字提示生成音樂或使用自訂歌詞。觸發詞：生成 MV、音樂影片、為這首歌做影片、歌詞影片、建立 MV、AI 音樂影片、音樂+影片、根據歌詞生成影片。"
    category: video
    version: "0.0.1"
  - name: "圖片生成"
    value: "giggle-generation-image"
    description: "支援文生圖和圖生圖。當使用者需要建立或生成圖像時使用。使用情境：(1) 根據文字描述生成、(2) 使用參考圖生成、(3) 自訂模型、畫幅比例、解析度。觸發詞：生成圖片、畫畫、建立圖片、AI 藝術圖。"
    category: image
    version: "0.0.1"
  - name: "音樂生成"
    value: "giggle-generation-music"
    description: "當使用者希望建立、生成或創作音樂時使用此技能——無論是文字描述、自訂歌詞，還是純樂器背景音樂。觸發詞：生成音樂、寫歌、創作歌曲、製作音樂、做一首歌、AI 音樂、背景音樂、為我作曲、帶歌詞的音樂、純音樂、做 beats。"
    category: music
    version: "0.0.1"
  - name: "劇本生成"
    value: "giggle-generation-scripts"
    description: "基於姜文電影常見的敘事推進與對白機制生成中文劇本內容。用於使用者提出生成劇本、寫劇本、做分場、出對白稿、改劇本或同類意圖時，包括：根據題材輸出故事梗概、人物小傳、分場大綱、分場劇本（含對白、動作、場面調度提示），並可按使用者要求調整時代背景、人物關係、衝突節奏與結局走向。"
    category: script
    version: "0.0.1"
  - name: "配音"
    value: "giggle-generation-speech"
    description: "當使用者希望生成語音、配音或文字轉音訊時使用此技能。透過 Giggle.pro 文轉音 API 將文字合成為 AI 語音。觸發詞：生成語音、文轉音、文字轉語音、配音、TTS、朗讀這段文字、把這段文字讀出來、合成語音、我需要一段配音。"
    category: voice
    version: "0.0.1"
  - name: "聲音克隆"
    value: "giggle-voice-clone"
    description: "當使用者希望從音訊樣本克隆聲音時使用此技能。傳入參考音訊 URL 至 voice-clone，再用克隆音色合成文字。觸發詞：聲音克隆、復刻聲音、克隆聲音、克隆我的聲音、從音訊克隆聲音。"
    category: voice
    version: "0.0.1"
  - name: "影片生成"
    value: "giggle-generation-video"
    description: "支援文字轉影片與圖片轉影片（首幀/尾幀）。適合需要將文字或圖片轉成影片的使用者。"
    category: video
    version: "0.0.1"
```
