---
name: ai-director-image
description: Use when the user asks to generate or edit images, use image references, or extract an avatar subject in Giggle AI Director.
---

Follow the shared [canvas and generation workflow](../ai-director-canvas/SKILL.md). Read the live tool schema and `list_models` before selecting a model or parameters.

Use `generate_image` for text-to-image, `generate_image_from_image` for edits or multiple references, and `extract_avatar_subject` for subject extraction. Select a model whose advertised capabilities cover the request. Check aspect ratio, size, output count, and reference count against the model and tool schemas. Supply an existing asset ID or an accessible URL when the tool schema accepts one. Use `upload_file` only if the target provider requires a separate upload.
