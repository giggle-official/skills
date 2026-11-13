---
name: ai-director-video
description: Use when the user asks to generate video, animate images, use multimodal references, control motion, or make an avatar video in Giggle AI Director.
---

Follow the shared [canvas and generation workflow](../ai-director-canvas/SKILL.md). Read the live tool schema and `list_models` before selecting a model or parameters.

Choose among `generate_video`, `generate_video_from_image`, `generate_omni_video`, `generate_motion_control_video`, `generate_avatar_video`, and `generate_topview_avatar_video`. Match the tool and model to the requested references, duration, resolution, audio and frame constraints. Use first/last frames only when the model advertises support. Supply accessible reference URLs or asset IDs as allowed by the tool schema. Use `upload_file` only if the target provider requires a separate upload.
