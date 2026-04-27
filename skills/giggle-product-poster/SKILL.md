---
name: giggle-product-poster
description: "Generate professional product marketing posters using AI image-to-image generation. The user provides a product photo, and the skill creates a polished poster around it. Use when users ask to create product posters, marketing images, promotional graphics, e-commerce main images, brand event posters, or social media promotional images. Triggers on keywords like: poster, product image, marketing graphic, promotional banner, campaign poster, e-commerce image, social media post, generate poster, create poster, make a poster."
---

# Product Poster Generator (English)

Guided workflow for creating AI-generated product posters via giggle.pro image-to-image API.
**Always uses image-to-image mode** — the user's product photo is required as the reference image.

## Workflow

### Stage 1: Collect Requirements

Ask the user for these items (combine into one message):

1. **Product image** ⚠️ Required: local file path to the product photo (e.g. `/Users/xxx/product.jpg`)
2. **Product info**: product name + one-sentence key selling point
3. **Poster type**: E-commerce launch / Brand event / Social media promotion
4. **Visual style**: Clean minimal / Bold & vibrant / Luxury premium / Tech futuristic / Playful youthful
5. **Aspect ratio**: E-commerce portrait 3:4 / Square 1:1 / Mobile portrait 9:16 / Wide landscape 16:9

Optional:
- Brand color (hex or description, e.g. "brand blue #1E3A8A")

If the user hasn't provided a product image path, **do not proceed to generation** — ask for it first.

If the user has already provided enough context, skip questions and proceed directly to Stage 2.

### Stage 2: Compose Prompt & Generate

**Step 1: Build the prompt** using this BASE structure:

```
[POSTER TYPE] for [PRODUCT NAME]. [KEY SELLING POINT].
Style: [AESTHETIC], [COLOR PALETTE], [MOOD].
Visual: Keep the product as the hero element, [COMPOSITION — e.g. centered / rule-of-thirds], enhance with [BACKGROUND/SCENE — e.g. clean gradient / lifestyle scene / abstract elements].
Text layout: Main title "[PRODUCT NAME]", tagline "[SLOGAN]", clean typography with strong hierarchy.
Technical: Professional commercial photography quality, high contrast, sharp details, no watermark.
```

Read `references/prompt-templates.md` for type-specific templates, style keywords, and color palette references.

**Step 2: Choose model and aspect ratio**

| Poster Type | Recommended Model | Default Ratio |
|------------|-------------------|---------------|
| E-commerce launch | nano-banana-2 | 3:4 |
| Brand event | nano-banana-2 | 9:16 |
| Social media | nano-banana-2-fast | 9:16 |

Use `nano-banana-2` for best image-to-image fidelity. Use `nano-banana-2-fast` for quick previews.

**Step 3: Run generate_poster.py**

`generate_poster.py` handles base64 conversion, task submission, polling, and URL extraction in one call. It prints the final plain URL(s) to stdout.

```bash
SKILL_SCRIPTS="<absolute_path_to_skill>/scripts"

poster_url=$(python "$SKILL_SCRIPTS/generate_poster.py" \
  --image "<product_image_path>" \
  --prompt "<composed_prompt>" \
  --model nano-banana-2 \
  --aspect-ratio <ratio>)
```

**Step 4: Present results**

`$poster_url` is already a clean, complete URL. Present it to the user as plain text:

```
Poster generated ✨

$poster_url

Let me know if you'd like any adjustments!
```

**Critical URL constraints:**
- Output `$poster_url` verbatim — do NOT wrap it in markdown `[text](url)` syntax
- Do NOT truncate, ellipsize (`...`), or reformat the URL
- Do NOT use `[View image](url)` or any link-text wrapper
- The URL is a long signed AWS CloudFront link — it must remain complete and unmodified

## Environment Setup

Requires `GIGGLE_API_KEY` environment variable:
```bash
export GIGGLE_API_KEY=your_api_key
```

API key available at https://giggle.pro/ account settings.

## Script Reference

`scripts/generate_poster.py` — all-in-one poster generation script (recommended).
- `--image <path>` → local product image (handles base64 conversion internally)
- `--prompt <text>` → generation prompt
- `--model` → `nano-banana-2` (default), `nano-banana-2-fast`, `seedream45`, `midjourney`
- `--aspect-ratio` → `1:1`, `3:4`, `4:3`, `16:9`, `9:16`, `2:3`, `3:2`, `21:9`
- stdout: plain URL(s), one per line
- stderr: progress messages


## References

- **`references/prompt-templates.md`** — Type-specific prompt templates, style keywords, color palette guide.
