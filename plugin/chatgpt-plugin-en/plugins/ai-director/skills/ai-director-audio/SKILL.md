---
name: ai-director-audio
description: Use when the user asks for text-to-speech, music, or voice cloning in Giggle AI Director.
---

Follow the shared [canvas and generation workflow](../ai-director-canvas/SKILL.md). Read the live tool schema and `list_models` before selecting a model or parameters.

Use `generate_speech` for speech, `generate_music` for music, and the voice cloning tool that matches the selected provider (`clone_voice` or `clone_topview_voice`). Check the live schema for language, duration and reference requirements. Ask the user to confirm they have permission to use the reference voice before sending it for cloning. Provider utilities may return voice identifiers instead of canvas media. Report what the tool returns.
