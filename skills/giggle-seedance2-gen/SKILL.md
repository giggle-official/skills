---
name: giggle-seedance2-gen
description: >
  Seedance 2.0 video via giggle.pro API plus prompt engineering: optimize prompts with Seedance patterns, then call giggle.pro only.
  Triggers: generate video, AI video, seedance, giggle, 视频提示词, image to video, text to video, omni, 多模态, 短剧, 广告视频, 首帧图, 角色参考.
  (User may say 即梦 as generic Seedance habit; delivery stays giggle.pro.)
version: "1.1.0"
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

# Giggle · Seedance 2.0 视频生成与提示词（合并版）

**Source**: [giggle-official/skills](https://github.com/giggle-official/skills) · **API:** [giggle.pro](https://giggle.pro/) · **Script:** `scripts/generation_api.py`

本技能 = **Giggle API 成片**（`scripts/generation_api.py`）+ **Seedance 2.0 提示词工程资料库**（`references/`、`prompts/`）。

- **主流程**：优化提示词 → API Key → 用 `text` / `image` / `omni` 提交并轮询结果。
- **深度写法**：创意钩子、分镜模板、长视频流水线、词表与范例见资源索引。

## 仓库内资源索引

| 路径 | 用途 |
|------|------|
| [references/creative-strategy.md](references/creative-strategy.md) | 写什么、≤15s 与长片策略 |
| [references/production-pipeline.md](references/production-pipeline.md) | 长视频前期流水线 |
| [references/long-video-strategy.md](references/long-video-strategy.md) | 分段、延长、衔接 |
| [references/examples.md](references/examples.md) | 场景与多模态示例 |
| [references/vocabulary.md](references/vocabulary.md) | 运镜、画质、大气效果词库 |
| [references/image-generation.md](references/image-generation.md) | 角色参考图 / 首帧图（前置生图提示词） |
| [references/platform-specs.md](references/platform-specs.md) | Seedance 通用输入习惯（**API 与限额以 giggle.pro / SKILL 为准**） |
| [prompts/](prompts/) | 主题扩展包、OpenClaw 全案短文 |
| [references/seedance-prompt-skill-legacy-SKILL.md](references/seedance-prompt-skill-legacy-SKILL.md) | 原「纯提示词」技能全文备份 |

---

## ⚠️ 平台与 API 约束（以 Giggle 为准）

资料库为通用 Seedance 提示词最佳实践；**视频与多模态成片仅通过 giggle.pro 提交**。实际调用本仓库脚本时遵守下表：

| 项目 | Giggle（本脚本） |
|------|------------------|
| 语言 | 与**用户输入语言一致**（见下节 Language Rule）；资料里中文模板可套用结构 |
| 时长 | **4–15** 秒整数，`--duration` |
| 画幅 / 清晰度 | `--aspect-ratio`、`--resolution` |
| omni 图片 | 最多 **9** 张，`url:` 或 `base64:` |
| 参考音 / 视频 | 仅 `url:`，`--audios`、`--videos` |
| 提示词里的 `@图片N` / `@视频N` | **仅编号习惯**；必须通过 CLI 传入**对应真实 URL**，且**全部**引用都要传 |

若资料写「混合素材 ≤12 个」与 Giggle 限制冲突，**取更严一侧**（尤其图片 ≤9）。

### `@引用` → Giggle CLI（omni）

| 提示词习惯 | 映射到 |
|------------|--------|
| `@图片1` … `@图片N` | `--images "url:..."`（按编号顺序，可多参数或多次 `--images`，脚本会合并） |
| `@视频1` … | `--videos "url:..."` |
| `@音频1` … | `--audios "url:..."` |

---

## ⚠️ Language Rule — MUST FOLLOW

**Match the user's input language exactly. Never translate. Never output a second language version.**

- User writes in Chinese → optimize in Chinese → pass Chinese prompt to API  
- User writes in English → optimize in English → pass English prompt to API  
- Output **ONE** version of the optimized prompt. No bilingual display. No "API submission version".

（资料库中大量中文范例：仅借鉴**结构与章法**，输出语言仍以上述规则为准。）

---

## Step 1: Prompt Optimization

### 1.1 快速公式（默认）

Enhance the prompt in the **same language as user input**. Formula:

```
[Subject] + [Scene] + [Action/Motion] + [Camera] + [Time-segments if 8s+] + [Audio] + [Style]
```

需要更强钩子、时间戳分镜、史诗片头品质锚定、一镜到底、卡点等时，在**不违反 Language Rule** 前提下查阅 `references/` 中对应文档，把技法压缩进**一条**终稿提示词。

### 1.2 深度模式（可选速查）

| 需求 | 建议先读 |
|------|----------|
| 爆款短镜、前 2 秒 | [creative-strategy.md](references/creative-strategy.md) |
| 长片、分镜、拆段 | [production-pipeline.md](references/production-pipeline.md)、[long-video-strategy.md](references/long-video-strategy.md) |
| 运镜 / 画质词汇 | [vocabulary.md](references/vocabulary.md) |
| 多模态叙事样板 | [examples.md](references/examples.md) |
| 先要角色图 / 首帧 | [image-generation.md](references/image-generation.md) |
| 主题脑洞扩展 | [prompts/](prompts/) |

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
| 鸟瞰 / 俯拍 | Bird's-eye view | Top-down overview |

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

### Step 1 交付物

- **一条**已优化、与用户语言一致的 `prompt`。
- Omni：提示词中提到的每条参考，均能在 CLI 找到对应 URL；编号习惯（`@图片N` 等）已由代理映射完毕。

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

---

## 质量自检（提交前）

- [ ] 提示词语言与用户一致；仅一个版本
- [ ] `duration ∈ [4,15]`
- [ ] omni：图片 ≤9；每条音/视频以 `url:` 开头
- [ ] 用户提供的参考 URL **全部**出现在 CLI 中
- [ ] 超长叙事已按 [long-video-strategy.md](references/long-video-strategy.md) 思路拆段或多任务，未假定单次超出 API 时长
