---
name: giggle-gpt-image-2
description: Generates high-quality text-to-image and image-to-image prompts optimized for GPT-Image-2. Use when a user wants to create image generation prompts, write AI art prompts, or generate visual content with GPT-Image-2 / DALL-E — including product posters, portrait photography, city promotional images, character design, UI mockups, illustration style transfer, comics/stickers, social media covers, sci-fi concept art, advertising creatives, and any other image generation needs. Triggers on: "生成图片", "写提示词", "prompt", "AI 画图", "图生图", "write me a prompt", "generate an image", "create a poster", "text to image".
---

# GPT-Image-2 Prompt & Generation Assistant

Helps users generate high-quality prompts for GPT-Image-2, then directly calls the Giggle API using `gpt-image-2-fast` to generate images.

## Workflow

### Step 1: Understand the Request

Quickly extract the following key information (skip what is already provided; ask only 1–2 follow-up questions for the most critical missing pieces):
- **Subject / Content**: What to draw? What are the core elements?
- **Use Case**: Poster / portrait / UI / social media cover / character design, etc. (see categories below)
- **Style Preference**: Realistic / illustration / cyberpunk / Chinese ink / cinematic, etc.
- **Aspect Ratio**: 9:16 portrait / 16:9 landscape / 1:1 square (default: 9:16)
- **Image-to-Image**: Is there a reference image? (If yes, specify which aspects to preserve)

If the user has already provided enough information, proceed directly to the next steps without asking again.

### Step 2: Match Scene Type and Load Reference Examples

Match the user's request to one of the categories below, then read the corresponding file for inspiration from original cases:

| Scene Type | Reference File | Key Styles |
|-----------|---------------|-----------|
| Portrait / Photography | [references/examples-portrait.md](references/examples-portrait.md) | Film look, Korean idol, influencer shots, CCD aesthetic (18 cases) |
| Poster / Illustration | [references/examples-poster.md](references/examples-poster.md) | City promo, science infographic, dark epic, watercolor illustration (46 cases) |
| Character Design | [references/examples-character.md](references/examples-character.md) | Game characters, anime character sheets, emoji/sticker series (9 cases) |
| UI / Social Media Mockup | [references/examples-ui-social.md](references/examples-ui-social.md) | TikTok screenshots, UI design systems, social feeds (25 cases) |
| Creative Mix | [references/examples-community.md](references/examples-community.md) | Style transfer, game screenshots, historical crossover (15 cases) |

**Universal Prompt Templates** (slot-based structural frameworks): [references/prompt-templates.md](references/prompt-templates.md)

### Step 3: Build the Prompt

Assemble using the following structure (adjust emphasis based on scene type):

**Portrait / Photography:**
```
[Capture medium + style] [Lighting atmosphere] [Subject description: age/appearance/outfit] [Pose/expression] [Background scene] [Technical specs] [Negative prompts]
```

**Poster / Illustration:**
```
[Style definition] [Composition: S-curve / diagonal / symmetry] [Hero visual subject] [Background scene + landmarks] [Color palette] [Typography / text] [Aspect ratio] [Quality modifiers]
```

**Character Design:**
```
[World-setting + character role] [Appearance + outfit + equipment] [Multi-view notes] [Color reference] [Detail requirements] [Background / layout]
```

**UI / Mockup:**
```
[Platform name + interface type] [Content details: text / username / content] [UI element description] [Character in scene] [Aspect ratio]
```

### Step 4: Output the Final Prompt First

Finalize the prompt before calling the Giggle API.

Output format:

**1. Final Prompt (ready to copy)**
Wrap in a code block:
```
[complete prompt]
```

**2. Brief Notes** (3 lines max)
- Structure / style used
- Key optimizations
- Whether this will be text-to-image or image-to-image

### Step 5: Call the Giggle API to Generate the Image

After generating the prompt, continue to image generation — do not stop at the prompt stage.

#### 5.1 Mode Selection

- **No reference image**: Call text-to-image endpoint `POST /api/v1/generation/text-to-image`
- **Has reference image**: Call image-to-image endpoint `POST /api/v1/generation/image-to-image`
- Model is fixed: `gpt-image-2-fast`

#### 5.2 Reference Image Input Rules

- Prefer user-provided **local file paths**
- Also supports **remote image URLs**
- For local paths, the script `scripts/generate_gpt_image.py` handles base64 conversion automatically
- For URLs, pass directly as `reference_images[].url`

#### 5.3 Run the Script

Use the bundled script:

```bash
python scripts/generate_gpt_image.py \
  --prompt "<final prompt>" \
  --aspect-ratio <ratio> \
  --output-format kv
```

With a reference image:

```bash
python scripts/generate_gpt_image.py \
  --prompt "<final prompt>" \
  --aspect-ratio <ratio> \
  --reference-image "<local path or remote URL>" \
  --output-format kv
```

Optional arguments:
- `--count`: Number of images to generate, default `1`
- `--timeout`: Maximum wait time in seconds, default `300`
- `--output-format`: `kv` / `json` / `plain`, default `kv`

#### 5.4 Response to User

The script automatically:
- Reads `GIGGLE_API_KEY`
- Submits the task
- Polls `/api/v1/generation/task/query`
- Extracts result image URLs from `data.urls` per the query API spec
- Falls back to other nested URL fields for backwards compatibility
- Outputs results using fixed key names to reduce the chance of LLMs missing links:

```text
RESULT_STATUS=success
RESULT_PRIMARY_URL=https://...
RESULT_URL_COUNT=1
RESULT_URL_1=https://...
```

When replying to the user:
- Briefly state whether text-to-image or image-to-image was used
- Provide the final prompt
- Use `RESULT_PRIMARY_URL` as the primary result
- **Return the image URL as-is**

Important requirements:
- Do not wrap the URL in a markdown link
- Do not truncate the URL
- Do not remove signature parameters
- Do not rewrite success results as "click here to view"

## Core Techniques

**Quality Boosters (add as needed):**
- Photographic feel: `35mm film`, `film grain`, `cinematic`, `photorealistic`, `8K`
- Illustration feel: `high detail`, `masterpiece`, `professional illustration`
- Composition control: `--ar 9:16`, `9:16 vertical`, `16:9 horizontal`

**Language Tips:**
- Chinese prompts work better for Chinese aesthetic styles and Chinese typography
- English prompts work better for Western portraits and cinematic quality
- When mixing: use Chinese for the subject description, English for technical terms

**Image-to-Image (Reference Images):**
- Style reference: `in the style of [reference image]`, `maintain the color palette`
- Subject reference: `same person`, `consistent facial features`
- Partial edits: describe what to preserve first, then specify what to change
- If the user says "keep the subject, change only the background/outfit/material/lighting," put the "preserve" items in the first half of the prompt

**Negative Prompts (add as appropriate):**
```
no watermark, no text, no plastic skin, no over-sharpening, no blur, no deformed hands
```

## Runtime Environment

Requires system environment variable:

```bash
export GIGGLE_API_KEY=your_api_key
```

Giggle API Key is available at https://giggle.pro/developer.

## Reference Resources

Detailed prompt examples are organized in `references/examples-portrait.md`, `references/examples-poster.md`, `references/examples-character.md`, `references/examples-ui-social.md`, and `references/examples-community.md`. Consult the relevant category file when you need inspiration.
