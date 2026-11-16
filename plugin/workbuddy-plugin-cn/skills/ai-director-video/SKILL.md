---
name: ai-director-video
description: 用户要求生成视频、首尾帧、多模态参考、动作控制或数字人视频时使用。
---

遵循[画布和生成流程](../ai-director-canvas/SKILL.md)，先读取实时工具参数和 `list_models`。

按输入选择 `generate_video`、`generate_video_from_image`、`generate_omni_video`、`generate_motion_control_video`、`generate_avatar_video` 或 `generate_topview_avatar_video`。按模型实际支持范围核对时长、分辨率、声音和参考素材。只有模型支持时才使用首尾帧。
