---
name: ai-director-canvas
description: 用户要求选择或创建 AI Director 画布、查询模型、预估生成费用或查询任务时使用。
---

1. 通过客户端原生连接入口完成 Giggle OAuth 授权。连接检查只调用 `list_models` 和 `list_canvases`。
2. 按工具的说明给 `list_models` 传入 `model_type`，文生图用 `Txt2Img`，图生图用 `Img2Img`，文生视频用 `Txt2Video`，图生视频用 `Img2Video`，全能参考视频用 `OmniVideo`。先用 `allowed_use=true` 的模型，目录的 `ratio` 对应请求的 `aspect_ratio`，`durations` 是 `duration` 允许的秒数。固定模型工具遵循自己的参数说明。若用户指定值超出范围，展示可选值请用户选择，再按实际参数估价。通过 `list_canvases` 选择当前团队可编辑画布。仅在用户要求时调用 `create_canvas`，将选定的 `canvas_id` 用于生成。
3. 付费提交前用 `estimate_price` 按实际参数报价，告知用户费用并等待确认。无法确定费用时暂停提交。
4. 工具需要 `request_id` 时为本次提交生成唯一标识。生成工具调用无需提供回调地址。保存返回的 `task_id` 和 `canvas_id`。如果提交结果未知且尚未拿到任务 ID，重试时复用原 `request_id` 和参数。
5. 拿到任务 ID 后调用 `get_task`，按 `data.request.state` 判断结果。遇到 `completed` 或 `failed` 时结束，遇到 `conflict` 或 `needs_review` 时提示用户检查。遇到 `preparing`、`submitting`、`submitted`、`uncertain` 或短暂查询故障时，每 5 秒左右查询同一 ID，默认最多等待 10 分钟，用户指定等待时间时以该时间为准。客户端无法等待或达到等待上限时，报告最近状态和任务 ID，之后可继续查询原任务。拿到任务 ID 后只查询状态，避免重复提交或扣费。
6. 完成后报告目标画布、节点和任务结果。已有 Web 地址时提供画布链接，否则提供画布 ID。对只返回上传引用或音色 ID 的工具，报告相应结果。
