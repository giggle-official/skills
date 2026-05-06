---
name: giggle-seedance2-gen
description: "Generate AI videos with Seedance 2.0 via Giggle API. Optimize user prompts using Seedance 2.0 prompt engineering, then call Giggle API to generate video. Triggers: generate video, AI video, seedance, giggle, image to video, text to video, video generation."
version: "1.0.0"
license: MIT
author: giggle-official
homepage: https://github.com/giggle-official/skills
repository: https://github.com/giggle-official/skills
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "🎬",
      "requires": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "GIGGLE_API_KEY",
      "installSpec": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY"],
        "pip": ["requests"]
      }
    }
  }
---

# Giggle Seedance 2.0 Video Generation

**Source**: [giggle-official/skills](https://github.com/giggle-official/skills) · **API:** giggle.pro · **Model:** Seedance 2.0 Pro / Fast · **Script:** `scripts/generation_api.py`

---

## ⚠️ Language Rule — MUST FOLLOW

**Match the user's input language exactly. Never translate. Never output a second language version.**

- User writes in Chinese → optimize in Chinese → pass Chinese prompt to API
- User writes in English → optimize in English → pass English prompt to API
- Output ONE version of the optimized prompt. No bilingual display. No "API submission version".

---

## Step 1: Prompt Optimization

Enhance the prompt in the **same language as user input**. Formula:

```
[Subject] + [Scene] + [Action/Motion] + [Camera] + [Time-segments if 8s+] + [Audio] + [Style]
```

### Chinese Examples (for Chinese user input)

**Text-to-video:**
```
Input:  "一只猫在玩"
Output: "一只毛茸茸的橘猫在温暖的午后阳光里用爪子拨弄悬挂的玩具鼠，
         镜头从中景缓缓推近到猫咪专注眼神的特写。
         背景：温馨的客厅，背景虚化。音效：轻柔室内环境音。电影质感，浅景深，24fps。"
```

**Image-to-video:**
```
Input:  "让这张照片动起来"
Output: "以参考图为首帧，画面中的人物缓缓将头转向镜头，展露温暖的笑容。
         镜头从中景缓缓推近至面部特写，光线柔和温暖。背景树叶轻轻摇曳。
         温暖黄金时段光线，胶片颗粒感。"
```

**Omni (multi-modal):**
```
"参考图作为人物形象，参考音频作为背景 BGM，视频节奏跟随音乐节拍。
 场景：[描述环境]。动作：[描述动作]。氛围：电影感，温暖基调。"
```
（若用户在对话中提供了多张参考图、多段参考视频或多条参考音频，优化提示词时需分别对应说明每条参考的用途，且提交任务时必须 **全部** 传入接口，不能只传第一条；同一选项可多参数或多次写该选项，由 CLI 合并。）

### English Examples (for English user input)

**Text-to-video:**
```
Input:  "a cat playing"
Output: "A fluffy orange cat playfully bats at a dangling toy in warm afternoon sunlight.
         Camera starts medium shot then slowly pushes in to close-up on the cat's focused eyes.
         Background: cozy living room with soft bokeh. Gentle ambient sounds. Cinematic, 24fps."
```

**Image-to-video:**
```
Input:  "make this photo move"
Output: "Starting from the reference image, the subject slowly turns toward the camera with a warm smile.
         Camera gently pushes in from medium to close-up. Soft golden-hour lighting.
         Background foliage sways gently. Warm golden-hour light, film grain."
```

**Omni (multi-modal):**
```
"Reference image as subject character. Reference audio as background music —
 sync video rhythm and cuts to the beat. Scene: [describe environment].
 Action: [what happens]. Mood: cinematic, warm."
```
(If the user provided multiple reference images, videos, or audio in the chat, describe each reference's role in the optimized prompt and pass **every** URL to the API — never submit only the first one. After each `--images` / `--audios` / `--videos` flag you can list multiple space-separated values, or repeat the same flag; the script merges all entries.)

### Camera Language

| 中文 | English | Effect |
|------|---------|--------|
| 慢推镜头 | Slow push in | Camera moves toward subject |
| 后拉镜头 | Pull back | Camera moves away |
| 环绕镜头 | Orbit shot | Camera circles subject |
| 跟随镜头 | Follow shot | Camera tracks subject |
| 希区柯克变焦 | Hitchcock zoom | Push+zoom for vertigo |
| 低角度仰拍 | Low angle | Empowering perspective |
| 鸟瞰 / 俯拍 | Bird's eye | Top-down overview |

### Style Modifiers

- 中文: `电影质感，浅景深，24fps` / `温暖黄金时段光线，胶片颗粒感` / `高对比度，霓虹色调`
- English: `Cinematic quality, shallow depth of field, 24fps` / `Warm golden-hour lighting, film grain`

### Time-Segmented (8s+ videos)

```
0–3s:   [opening shot, camera, subject intro]
3–6s:   [main action develops]
6–10s:  [climax or key moment]
10–15s: [resolution, outro]
```

---

## Step 2: API Key Setup (One-Time)

```bash
python3 scripts/generation_api.py --check-key
```

**已配置**则进入 Step 3；**未配置**则向用户索要 Key 后执行：

```bash
python3 scripts/generation_api.py --setup --api-key <key>
```

---

## Step 3: Generate Video

**Text-to-Video:**
```bash
python3 scripts/generation_api.py \
  --mode text --prompt "<optimized_prompt>" \
  --model seedance-2.0-pro --duration 5 --aspect-ratio 16:9 --resolution 720p
```

**Image-to-Video:**
```bash
python3 scripts/generation_api.py \
  --mode image --prompt "<optimized_prompt>" \
  --start-frame "url:<URL>" --model seedance-2.0-pro --duration 5
```

**Omni:**

- **多参考资源：** 从对话中 **收集用户给出的全部** 参考图 / 参考视频 / 参考音频 URL（含 `url:` 前缀），再一次性调用 CLI。同一选项后可跟 **多个** 空格分隔的参数（如 `--images "url:a" "url:b"`）；也可 **多次** 写同一选项（如两行 `--images`），脚本会合并为完整列表。禁止只取第一个链接就提交。
- **数量：** 图片总计最多 9 张（接口校验）；音视频按对话实际条数全部传入。

```bash
# 示例：多图 + 多音频 + 多参考视频（按实际数量增删参数）
python3 scripts/generation_api.py \
  --mode omni --prompt "<optimized_prompt>" \
  --images "url:<img1>" "url:<img2>" \
  --audios "url:<audio1>" "url:<audio2>" \
  --videos "url:<ref_video1>" "url:<ref_video2>" \
  --model seedance-2.0-pro --duration 5
```

若某类参考未提供，可省略对应选项（但至少保留 `--images`、`--audios`、`--videos` 之一）。

**提交后：** 脚本默认每约 10 秒轮询一次（最长约 10 分钟）；任务完成后**主动**将结果（含链接）推送给用户，无需等用户追问。

---

## Parameters

| Parameter | Default | Options |
|-----------|---------|---------|
| `--mode` | required | `text` / `image` / `omni` |
| `--prompt` | required | Max 10,000 chars — use user's input language |
| `--model` | `seedance-2.0-pro` | `seedance-2.0-pro` / `seedance-2.0-fast` |
| `--duration` | `5` | 4–15 seconds |
| `--aspect-ratio` | `16:9` | `16:9` / `9:16` / `1:1` / `3:4` / `4:3` |
| `--resolution` | `720p` | `480p` / `720p` |
| `--generating-count` | `1` | 1–4 |
| `--images` | — | **omni**：`url:` 或 `base64:`，可重复多个；最多 9 张 |
| `--audios` | — | **omni**：仅 `url:`，可重复多个 |
| `--videos` | — | **omni**：参考视频，仅 `url:`，可重复多个 |
