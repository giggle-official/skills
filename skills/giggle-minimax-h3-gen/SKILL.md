---
name: giggle-minimax-h3-gen
description: >
  Use when the user wants to generate AI video, optimize video prompts, or work with MiniMax-H3 on giggle.pro.
  Txt2Video / Img2Video (1–2 frames) / OmniVideo; billing aligned with gateway MiniMax-H3; host remains giggle.pro.
  480p/768p (default 768p), duration 4–15s (default 5). Triggers: MiniMax-H3, giggle, 文生视频, 首尾帧, 全能参考, omni.
version: "2.0.0"
license: MIT
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

# Giggle · MiniMax-H3 视频生成与提示词（合并版）

**Source**: [giggle-official/skills](https://github.com/giggle-official/skills) · **上游:** [giggle.pro](https://giggle.pro/) · **Script:** `scripts/generation_api.py`

本技能 = **giggle.pro 成片**（新计费/生成逻辑）+ **提示词工程资料库**（`references/`、`prompts/`）。

- **主流程**：优化提示词 → API Key → `Txt2Video` / `Img2Video` / `OmniVideo` 提交并轮询。
- **计费细则**：[references/billing.md](references/billing.md)
- **平台规格**：[references/platform-specs.md](references/platform-specs.md)

> 请求体与计价对齐 storyclaw-token-gateway MiniMax-H3；**HTTP 上游仍是 giggle.pro**（`x-auth` + `GIGGLE_API_KEY`），不是 hopsapi.com。

## 仓库内资源索引

| 路径 | 用途 |
|------|------|
| [references/billing.md](references/billing.md) | 成片费 / 参考图附加 / 参考视频附加 |
| [references/platform-specs.md](references/platform-specs.md) | 输入输出与模式限制 |
| [references/prompt-engineering.md](references/prompt-engineering.md) | 提示词工程规范 |
| [references/creative-strategy.md](references/creative-strategy.md) | 创意策略 |
| [references/production-pipeline.md](references/production-pipeline.md) | 长视频流水线 |
| [references/long-video-strategy.md](references/long-video-strategy.md) | 分段与衔接 |
| [references/examples.md](references/examples.md) | 场景示例 |
| [references/vocabulary.md](references/vocabulary.md) | 运镜词库 |
| [references/image-generation.md](references/image-generation.md) | 首帧 / 角色图 |
| [prompts/](prompts/) | 主题扩展包 |

---

## Base URL 与接口

| 用途 | 环境变量 | 默认值 |
|------|----------|--------|
| API Base URL | `GIGGLE_BASE_URL` | `https://giggle.pro/v1` |
| 站点根（上传等） | `GIGGLE_CONSOLE_URL` | `https://giggle.pro` |

鉴权：`x-auth: <GIGGLE_API_KEY>`（脚本同时带 `Authorization: Bearer` 兼容）。

| 操作 | 方法 | 完整 URL（默认） |
|------|------|------------------|
| 创建视频任务 | `POST` | `https://giggle.pro/v1/router/task/create` |
| 查询任务 | `GET` | `https://giggle.pro/v1/router/tasks/{task_id}` |
| 停止任务 | `POST` | `https://giggle.pro/v1/router/task/stop` |

### 请求示例（HTTP）

以下均为 `POST https://giggle.pro/v1/router/task/create`。`duration` **4–15**；省略 `resolution`/`duration` 时按 **768p / 5**。

**公共请求头：**

```http
x-auth: 你的GIGGLE_API_KEY
Content-Type: application/json
```

#### 1. 文生视频（Txt2Video）

```bash
curl -s https://giggle.pro/v1/router/task/create \
  -H "x-auth: 你的GIGGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Txt2Video",
    "model": "MiniMax-H3",
    "input": {
      "prompt": "电影感的山间日出，云海缓慢流动",
      "duration": 5,
      "resolution": "768p"
    }
  }'
```

```json
{
  "task": "Txt2Video",
  "model": "MiniMax-H3",
  "input": {
    "prompt": "电影感的山间日出，云海缓慢流动",
    "duration": 5,
    "resolution": "768p"
  }
}
```

#### 2. 图生视频（Img2Video，恰好 1 张图）

```bash
curl -s https://giggle.pro/v1/router/task/create \
  -H "x-auth: 你的GIGGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Img2Video",
    "model": "MiniMax-H3",
    "input": {
      "prompt": "让画面中的云层缓慢流动，镜头平稳向前推进",
      "images": ["https://assets.example.com/input.png"],
      "duration": 5,
      "resolution": "480p"
    }
  }'
```

```json
{
  "task": "Img2Video",
  "model": "MiniMax-H3",
  "input": {
    "prompt": "让画面中的云层缓慢流动，镜头平稳向前推进",
    "images": ["https://assets.example.com/input.png"],
    "duration": 5,
    "resolution": "480p"
  }
}
```

#### 3. 首尾帧（Img2Video，恰好 2 张：首 → 尾）

```bash
curl -s https://giggle.pro/v1/router/task/create \
  -H "x-auth: 你的GIGGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Img2Video",
    "model": "MiniMax-H3",
    "input": {
      "prompt": "镜头从清晨自然过渡到黄昏",
      "images": [
        "https://assets.example.com/first.png",
        "https://assets.example.com/last.png"
      ],
      "duration": 10,
      "resolution": "768p",
      "aspect_ratio": "16:9",
      "generate_audio": true
    }
  }'
```

```json
{
  "task": "Img2Video",
  "model": "MiniMax-H3",
  "input": {
    "prompt": "镜头从清晨自然过渡到黄昏",
    "images": [
      "https://assets.example.com/first.png",
      "https://assets.example.com/last.png"
    ],
    "duration": 10,
    "resolution": "768p",
    "aspect_ratio": "16:9",
    "generate_audio": true
  }
}
```

#### 4. 全能参考 · 仅图片（参考图计价）

```bash
curl -s https://giggle.pro/v1/router/task/create \
  -H "x-auth: 你的GIGGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "OmniVideo",
    "model": "MiniMax-H3",
    "input": {
      "prompt": "保持参考图片中人物的外观与服装",
      "images": [
        "https://assets.example.com/character-1.png",
        "https://assets.example.com/character-2.png"
      ],
      "duration": 8,
      "resolution": "480p"
    }
  }'
```

#### 5. 全能参考 · 含视频（参考视频计价，更贵；勿传 video_durations）

```bash
curl -s https://giggle.pro/v1/router/task/create \
  -H "x-auth: 你的GIGGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "OmniVideo",
    "model": "MiniMax-H3",
    "input": {
      "prompt": "保持参考图片中人物的外观，沿用参考视频的运镜",
      "images": ["https://assets.example.com/character.png"],
      "videos": ["https://assets.example.com/camera-motion.mp4"],
      "duration": 15,
      "resolution": "768p"
    }
  }'
```

#### 6. 全能参考 · 含音频（音频不加价）

```json
{
  "task": "OmniVideo",
  "model": "MiniMax-H3",
  "input": {
    "prompt": "人物对口型演唱，节奏跟随参考音频",
    "images": ["https://assets.example.com/singer.png"],
    "audios": ["https://assets.example.com/vocal.mp3"],
    "duration": 8,
    "resolution": "768p"
  }
}
```

#### 7. 创建成功 / 查询

```json
{ "code": 200, "message": "success", "task_id": "tsk_0f3c9a72b1e04d5f" }
```

```bash
curl -s https://giggle.pro/v1/router/tasks/tsk_0f3c9a72b1e04d5f \
  -H "x-auth: 你的GIGGLE_API_KEY"
```

| status | 含义 |
|--------|------|
| `0` | 排队 |
| `1` | 处理中 |
| `2` | 成功（已结算） |
| `3` | 失败（不扣费） |
| `4` | 已取消（不扣费） |

---

## ⚠️ 平台与 API 约束

| 项目 | 规则 |
|------|------|
| 上游 | **giggle.pro**（非 hopsapi.com） |
| 模型 | 固定 `MiniMax-H3` |
| 时长 | **4–15** 秒，默认 **5** |
| 分辨率 | **480p** / **768p**，默认 **768p** |
| 画幅 | `16:9` / `9:16` / `1:1` / `4:3` / `3:4` / `21:9` / `auto`；省略则不传 |
| 素材 | **仅公网 HTTPS URL**（可用 `url:` 前缀；勿再传 base64） |
| 参考视频 | **不要**传 `video_durations` |
| omni | 图 ≤9、视频 ≤3、音频 ≤3 |

### `@引用` → CLI

| 提示词 | CLI |
|--------|-----|
| `@图片N` | `--images "https://..."` |
| `@视频N` | `--videos "https://..."` |
| `@音频N` | `--audios "https://..."` |

---

## ⚠️ Language Rule — MUST FOLLOW

**Match the user's input language exactly. Never translate. Never output a second language version.**

- User writes in Chinese → optimize in Chinese → pass Chinese prompt to API
- User writes in English → optimize in English → pass English prompt to API
- Output **ONE** version of the optimized prompt. No bilingual display. No "API submission version".

（资料库中大量中文范例：仅借鉴**结构与章法**，输出语言仍以上述规则为准。）

---

## Step 1: 提示词优化（必须完成后才能进入 Step 2）

用户输入往往描述不准确。**必须先走完以下完整优化流程，生成高质量 prompt，用户确认后再提交 API。**

完整规范见 [references/prompt-engineering.md](references/prompt-engineering.md)，以下为 SKILL.md 内联的执行摘要。

---

### MiniMax-H3 核心能力速查

| # | 能力 | 提示词核心模式 |
|---|------|---------------|
| 1 | **一致性控制** | `[角色]@图片N + [动作/剧情] + [场景]@图片N` |
| 2 | **运镜/动作复刻** | `参考@视频1的[运镜/动作/节奏] + [主体]@图片N` |
| 3 | **创意/特效复刻** | `参考@视频1的[特效/转场] + 将[元素]替换为@图片N` |
| 4 | **剧情补全** | `[分镜脚本] + [演绎方式] + [音效/台词]` |
| 5 | **视频延长** | `将@视频1延长Xs + [新增内容]` |
| 6 | **声音控制** | `[画面] + 音色参考@视频1 + "台词"` |
| 7 | **一镜到底** | `一镜到底 + @图片1@图片2... + 全程不切镜头` |
| 8 | **视频编辑** | `将@视频1中的[A]换成@图片1 + [修改说明]` |
| 9 | **音乐卡点** | `@图片1...@图片N + 参考@视频1的画面节奏/卡点` |
| 10 | **情绪演绎** | `[角色] + [情绪变化描述] + [运镜配合]` |

各能力详细示例见 [references/examples.md](references/examples.md)。

---

### Phase 0：判断内容类型（最关键的一步）

| 场景 | 路径 | 核心任务 |
|------|------|---------|
| ≤15秒 | 路径A | 帮用户找到一个**有传播力的单一视觉 hook**；参考 [creative-strategy.md](references/creative-strategy.md) 爆款模式库 |
| >15秒 | 路径B | 走完整前期流水线：角色设计 → 角色卡图提示词 → 分镜脚本 → 首帧图提示词 → 逐镜头视频提示词；参考 [production-pipeline.md](references/production-pipeline.md) |

### Phase 1：获取用户创意

用户描述想要生成的内容。

### Phase 2：确认关键参数（已明确可跳过）

1. **时长**：短片 4–8s / 中 9–12s / 长 13–15s / 超长 >15s（单次 API 仅 4–15）
2. **比例**：横 16:9 / 竖 9:16 / 方 1:1
3. **素材**：纯文本 / 有图片 / 有图+视频 / 全模态
4. **补充偏好**（可选）：情绪氛围、镜头风格、用途场景

### Phase 3：生成优化提示词（≤15秒输出 2–3 个版本，>15秒按流水线输出）

**提示词结构速查：**

| 场景 | 推荐结构 |
|------|---------|
| ≤12秒 | `[风格总纲]，[主体]，[动作]，[环境/光影]，[运镜]，[音效]` |
| 13–15秒 | 时间戳分镜法（0-3s / 4-8s / 9-12s / 13-15s 逐段描述） |
| 短剧对白 | 画面 + 台词（角色/情绪标注）+ 音效分离 |
| 史诗大制作 | 品质锚定 + 大气连贯声明 + 逐段 + 光影三层 + 收束句 |

**运镜三级速查：**
- **基础动作**：Pan / Dolly / Zoom / Crane / Orbit / Tracking
- **修饰词**：Smooth / Slow / Fast / Cinematic / Dreamy / Handheld / Aerial
- **组合技**：一次最多 2–3 个，用 `+` 连接；"雾粒粘镜"等镜头质感词可大幅提升沉浸感

**图片风格匹配（生成角色参考图 / 首帧图时）：**

| 题材 | 推荐生图风格 |
|------|------------|
| 仙侠 / 修真 | 3D国漫渲染、中国仙侠概念设计 |
| 古风 / 历史 | 中国风工笔画、水墨画 |
| 赛博朋克 / 科幻 | 未来科幻写实CG、概念设计 |
| 现实 / 人物 | 电影摄影写实、人像摄影 |
| 美食 / 产品 | 美食广告摄影、商业摄影 |
| 动漫（日） | 赛璐璐风格 |
| 动漫（国） | 3D国漫渲染 |

角色参考图格式：`9:16竖版构图。[风格锚定]角色设定图，[构图视角]，角色居中。[面部7要素]。[发型]。[服装逐件+新旧状态]。[道具]。[体态气质]。[光影]。禁止：任何文字、字幕、LOGO、水印`

首帧图格式：`[画幅比]。[风格锚定]，[构图+角色位置]。[角色状态+关键辨识特征]。[环境细节]。[光影层次]。[色调氛围]。禁止：任何文字、字幕、LOGO、水印`

**@引用编号分配规则：**
1. **公共素材**（角色参考图等跨版本共用）从 `@图片1` 开始依次编号
2. **版本独立素材**（各版本首帧图、尾帧图）在公共素材编号之后递增
3. 每个素材标注用途，写清楚是"参考"（借鉴风格/动作）还是"编辑"（在原素材上修改）

**多模态组合技巧：**
- 有首帧图 + 想参考视频动作 → `@图片1为首帧，参考@视频1的打斗动作`
- 融合多个视频 → `在@视频1和@视频2之间加一个场景，内容为xxx`
- 没有音频素材 → 直接参考视频里的声音，无需单独上传音频
- 连续动作 → `角色从跳跃直接过渡到翻滚，保持动作连贯流畅`
- 多素材时务必检查各 @对象有没有标清楚，别把图、视频、角色搞混

**≤15秒输出格式（完整模式）：**

```
## 视频提示词

**主题**：[一句话概括]
**时长**：[X秒]  |  **比例**：[16:9 / 9:16 / 1:1]

### 公共参考素材（如有）
- @图片1：[用途说明 + 图片生成提示词]

---

### 版本一：[版本标题]
#### 提示词
[完整提示词]
#### 参考素材
- 首帧 @图片N：[描述 + 图片生成提示词]

---

### 版本二：[版本标题]
[同上结构]

---

### 提示词解析
[各版本设计意图差异]
```

>15秒输出格式见 [references/long-video-strategy.md](references/long-video-strategy.md)（含全局锁定语句、统一负面提示词、分段模板）。

**深度资源索引：**

| 需求 | 参考文件 |
|------|---------|
| 爆款概念、前 2 秒钩子 | [creative-strategy.md](references/creative-strategy.md) |
| 长片分段、衔接、流水线 | [production-pipeline.md](references/production-pipeline.md)、[long-video-strategy.md](references/long-video-strategy.md) |
| 运镜词汇、画质锚定词 | [vocabulary.md](references/vocabulary.md) |
| 多模态场景样板 | [examples.md](references/examples.md) |
| 角色参考图 / 首帧图规范 | [image-generation.md](references/image-generation.md) |
| 主题扩展包、短剧全案 | [prompts/](prompts/) |

### Phase 4：用户确认

用户选定版本（可要求调整：风格/色调/运镜/台词/时长），确认最终版本后进入 Step 2。

---

### Giggle 覆盖规则（优先于 prompt-engineering.md）

1. **语言**：严格遵守 Language Rule。用户中文 → 中文 prompt；用户英文 → 英文 prompt。"Output ONE version" 指禁止双语对照输出，不限制版本数量。
2. **平台**：references 中的通用提示词方法，以本文件 MiniMax-H3 的 Giggle 约束（时长 4–15s、图片 ≤9 张、仅公网 URL、@引用命名等）为准。
3. **多模态引用**：若用户提供了多张图片/视频/音频，优化提示词时须逐条说明各参考用途，Step 3 提交时必须全部传入 CLI，不能只取第一条。

---

### Step 1 交付物

- 用户已选定的**一条**优化 prompt（与用户语言一致，已通过质量自检）
- Omni：提示词中每条参考均有对应 URL，编号映射（`@图片N` 等）已完成
- 超长视频：已按 [long-video-strategy.md](references/long-video-strategy.md) 确定分段数量和衔接点

---

## Step 2: API Key Setup (One-Time)

```bash
python3 scripts/generation_api.py --check-key
```

**已配置**则进入 Step 3；**未配置**则向用户索要 Key 后执行：

```bash
python3 scripts/generation_api.py --setup --api-key <key>
```

环境变量：`GIGGLE_API_KEY`。可选：`GIGGLE_BASE_URL`（默认 `https://giggle.pro/v1`）。

---

## Step 3: Generate Video

提交后脚本默认轮询；完成后**主动**回传视频链接与费用。出错勿盲目重试。

**文生：**
```bash
python3 scripts/generation_api.py \
  --mode text --prompt "<optimized_prompt>" \
  --duration 5 --resolution 768p
```

**图生：**
```bash
python3 scripts/generation_api.py \
  --mode image --prompt "<optimized_prompt>" \
  --images "https://example.com/input.png" --duration 5 --resolution 480p
```

**首尾帧：**
```bash
python3 scripts/generation_api.py \
  --mode image --prompt "<optimized_prompt>" \
  --start-frame "https://example.com/first.png" \
  --end-frame "https://example.com/last.png" \
  --duration 10 --aspect-ratio 16:9
```

**全能参考：** 收集用户给出的**全部**参考 URL 再提交；图 ≤9、视频 ≤3、音频 ≤3。

```bash
python3 scripts/generation_api.py \
  --mode omni --prompt "<optimized_prompt>" \
  --images "https://example.com/char.png" \
  --videos "https://example.com/motion.mp4" \
  --duration 15 --resolution 768p
```

```bash
python3 scripts/generation_api.py --query --task-id tsk_xxx
python3 scripts/generation_api.py --wait --task-id tsk_xxx
```

---

## Parameters

| Parameter | Default | Options |
|-----------|---------|---------|
| `--mode` | required | `text` / `image` / `omni` → `Txt2Video` / `Img2Video` / `OmniVideo` |
| `--prompt` | 文生必填 | 与用户语言一致 |
| `--model` | `MiniMax-H3` | 仅此值 |
| `--duration` | `5` | 4–15 |
| `--resolution` | `768p` | `480p` / `768p` |
| `--aspect-ratio` | 省略不传 | `16:9` / `9:16` / `1:1` / `4:3` / `3:4` / `21:9` / `auto` |
| `--images` / `--videos` / `--audios` | — | 公网 URL（可带 `url:`） |
| `--start-frame` / `--end-frame` | — | image 模式首/尾帧 |

---

## 质量自检（提交前）

### 提示词质量（Phase 3 生成后检查）

- [ ] @引用编号与素材清单一一对应，公共素材优先编号
- [ ] 总文件数 ≤ 12；omni 图片 ≤ 9
- [ ] 未包含写实真人面部素材
- [ ] 13–15秒视频已使用时间戳分镜
- [ ] 台词已用引号包裹并标注角色和情绪

### API 提交（Step 3 执行前检查）

- [ ] 提示词语言与用户输入语言一致
- [ ] `duration ∈ [4,15]`
- [ ] `resolution ∈ {480p,768p}`
- [ ] 素材均为公网 URL；未传 `video_durations` / base64
- [ ] 用户提供的参考 URL **全部**出现在 CLI 中

---

## 常见错误排查

| 错误 / 现象 | 解决方法 |
|------------|---------|
| `401` / Key 无效 | `--setup --api-key <新key>` |
| images 超限 / 数量不对 | Img2Video 须 1 或 2 张；omni ≤9 |
| `duration` 不合法 | 使用 4–15 整数 |
| 参考视频探测失败 | 换可访问的公网 mp4/mov，勿自报时长 |
| 720p 等分辨率 | 只用 480p / 768p |
| 生成与提示词差异大 | 精简提示词；见 references/examples.md |
