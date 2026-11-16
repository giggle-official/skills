---
name: ai-director-audio
description: 用户要求生成语音、音乐或克隆音色时使用。
---

遵循[画布和生成流程](../ai-director-canvas/SKILL.md)，先读取实时工具参数和 `list_models`。

语音用 `generate_speech`，音乐用 `generate_music`，音色克隆按供应商使用 `clone_voice` 或 `clone_topview_voice`。按工具实际参数核对语言、时长和参考音频。发送音频前确认用户有权使用参考音色。部分工具返回音色标识而非画布节点，以实际任务结果为准。
