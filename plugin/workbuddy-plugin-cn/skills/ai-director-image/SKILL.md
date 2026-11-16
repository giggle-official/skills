---
name: ai-director-image
description: 用户要求文生图、图生图、参考图编辑或主体抽取时使用。
---

遵循[画布和生成流程](../ai-director-canvas/SKILL.md)，先读取实时工具参数和 `list_models`。

文生图用 `generate_image`，图生图和多图参考用 `generate_image_from_image`，主体抽取用 `extract_avatar_subject`。按模型实际支持范围核对比例、尺寸、张数和参考图数量。工具支持时使用可访问的 URL 或已有素材 ID。
