---
name: giggle-gpt-image-2
description: Generates high-quality text-to-image and image-to-image prompts optimized for GPT-Image-2. Use when a user wants to create image generation prompts, write AI art prompts, or generate visual content with GPT-Image-2 / DALL-E — including product posters, portrait photography, city promotional images, character design, UI mockups, illustration style transfer, comics/stickers, social media covers, sci-fi concept art, advertising creatives, and any other image generation needs. Triggers on: "生成图片", "写提示词", "prompt", "AI 画图", "图生图", "write me a prompt", "generate an image", "create a poster", "text to image".
---

# GPT-Image-2 提示词与生成助手

帮助用户生成适合 GPT-Image-2 的高质量提示词，并在生成提示词后直接调用 Giggle API 使用 `gpt-image-2-fast` 生成图片。

## 工作流程

### Step 1：理解需求

快速提取以下关键信息（已有的跳过，不够时追问 1-2 个最关键的问题）：
- **主题内容**：画什么？有什么核心元素？
- **用途场景**：海报/人像/UI/社媒封面/角色设计等（见下方分类）
- **风格偏好**：写实/插画/赛博朋克/国风/电影感等
- **比例要求**：9:16 竖版 / 16:9 横版 / 1:1 方形（默认 9:16）
- **图生图**：是否有参考图？（若有，说明参考图的哪些方面保留）

若用户已经提供了足够信息，直接进入后续步骤，不要重复追问。

### Step 2：匹配场景类型，读取对应示例

根据用户需求匹配以下类型，读取对应文件中的原始案例获取灵感：

| 场景类型 | 参考文件 | 关键玩法 |
|---------|---------|---------|
| 人像/摄影 | [references/examples-portrait.md](references/examples-portrait.md) | 胶片风、韩系偶像、网红照、CCD 画风（18条） |
| 海报/插画 | [references/examples-poster.md](references/examples-poster.md) | 城市宣传、科普百科、暗黑史诗、水彩插画（46条） |
| 角色设计 | [references/examples-character.md](references/examples-character.md) | 游戏角色、动漫人设、表情包系列（9条） |
| UI/社媒样机 | [references/examples-ui-social.md](references/examples-ui-social.md) | 抖音截图、UI 设计系统、朋友圈（25条） |
| 创意混搭 | [references/examples-community.md](references/examples-community.md) | 风格迁移、游戏截图、古今穿越（15条） |

**通用提示词模板**（可填槽的结构框架）：[references/prompt-templates.md](references/prompt-templates.md)

### Step 3：构建提示词

按以下结构组装（根据场景灵活调整侧重）：

**人像/摄影类：**
```
[拍摄介质+风格] [光线氛围] [主体描述：年龄/外貌/服装] [姿态/表情] [背景场景] [技术规格] [负面提示]
```

**海报/插画类：**
```
[风格定义] [构图方式：S型/对角线/对称] [主视觉主体] [背景场景+地标] [色彩体系] [排版文字] [比例] [质量词]
```

**角色设计类：**
```
[世界观+角色定位] [外形+服装+装备] [多视图说明] [配色参考] [细节要求] [背景/排版]
```

**UI/样机类：**
```
[平台名称+界面类型] [内容细节：文字/用户名/内容] [UI 元素描述] [画面人物] [比例]
```

### Step 4：先输出最终提示词

先整理出最终 prompt，作为真正调用 Giggle API 的输入。

输出格式：

**1. 最终提示词（可直接复制）**
用代码块包裹：
```
[完整提示词]
```

**2. 简要说明**（3 行内）
- 采用了哪种结构/风格
- 关键优化点
- 当前将走文生图还是图生图

### Step 5：调用 Giggle API 生成图片

生成 prompt 后，必须继续执行图片生成，不要停在提示词阶段。

#### 5.1 模式判断

- **无参考图**：调用文生图接口 `POST /api/v1/generation/text-to-image`
- **有参考图**：调用图生图接口 `POST /api/v1/generation/image-to-image`
- 模型固定：`gpt-image-2-fast`

#### 5.2 参考图输入规则

- 优先接受用户提供的**本地文件路径**
- 也支持**远程图片 URL**
- 若是本地路径，交给 `scripts/generate_gpt_image.py` 自动转 base64
- 若是 URL，交给脚本直接作为 `reference_images[].url`

#### 5.3 执行脚本

使用本 skill 自带脚本：

```bash
python scripts/generate_gpt_image.py \
  --prompt "<最终提示词>" \
  --aspect-ratio <比例> \
  --output-format kv
```

如有参考图：

```bash
python scripts/generate_gpt_image.py \
  --prompt "<最终提示词>" \
  --aspect-ratio <比例> \
  --reference-image "<本地路径或远程 URL>" \
  --output-format kv
```

可选参数：
- `--count`：生成数量，默认 `1`
- `--timeout`：最长等待秒数，默认 `300`
- `--output-format`：`kv` / `json` / `plain`，默认 `kv`

#### 5.4 返回给用户的内容

脚本会自动：
- 读取 `GIGGLE_API_KEY`
- 提交任务
- 轮询 `/api/v1/generation/task/query`
- 按查询接口文档从 `data.urls` 提取结果图片 URL
- 为兼容历史返回结构，若存在其他嵌套 URL 字段也会兜底提取
- 默认用固定键名输出结果，降低 LLM 漏掉链接的概率：

```text
RESULT_STATUS=success
RESULT_PRIMARY_URL=https://...
RESULT_URL_COUNT=1
RESULT_URL_1=https://...
```

最终回复用户时：
- 简短说明当前走的是文生图还是图生图
- 给出最终 prompt
- 优先取 `RESULT_PRIMARY_URL`
- **原样返回图片 URL**

重要要求：
- 不要把 URL 包成 markdown 链接
- 不要截断 URL
- 不要删除签名参数
- 不要把成功结果改写成“点击这里查看”

## 核心技巧

**质量提升词（按需添加）：**
- 摄影感：`35mm film`, `film grain`, `cinematic`, `photorealistic`, `8K`
- 插画感：`high detail`, `masterpiece`, `professional illustration`
- 构图控制：`--ar 9:16`, `9:16 vertical`, `16:9 horizontal`

**中文提示词技巧：**
- 中文提示词对中式美学、汉字排版效果更好
- 英文提示词对西方人像、电影质感更精准
- 混用时，主体用中文描述，技术词用英文

**图生图（参考图）：**
- 风格参考：`in the style of [参考图]`, `maintain the color palette`
- 人物参考：`same person`, `consistent facial features`
- 局部修改：先描述保留部分，再说明要改动的内容
- 若用户明确说“保留主体，只改背景/服装/材质/灯光”，要把“保留项”写进 prompt 前半段

**负面提示词（适当添加）：**
```
no watermark, no text, no plastic skin, no over-sharpening, no blur, no deformed hands
```

## 运行环境

需要系统环境变量：

```bash
export GIGGLE_API_KEY=your_api_key
```

Giggle API Key 可在 https://giggle.pro/developer 获取。

## 参考资源

详细提示词示例分布在 `references/examples-portrait.md`、`references/examples-poster.md`、`references/examples-character.md`、`references/examples-ui-social.md`、`references/examples-community.md`。需要灵感时直接查阅对应分类。
