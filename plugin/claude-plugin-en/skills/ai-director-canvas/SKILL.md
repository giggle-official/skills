---
name: ai-director-canvas
description: Use when the user wants to pick or create an AI Director canvas, inspect models, estimate generation cost, or check a generation task.
---

Use the connected AI Director MCP tools. If authorization is needed, guide the user through Giggle sign-in in the client.

1. Use `list_models` to find currently available models and their parameter constraints. Use only models allowed for the user. Use the current tool schema to construct arguments.
2. Use `list_canvases` to find editable canvases in the current team. Reuse the user's selected canvas or ask where the result should go. Use `create_canvas` when the user wants a new canvas. Supply the selected `canvas_id` for canvas-bound generation.
3. Before submitting a billable operation, call `estimate_price` using the model and generation parameters. Tell the user the estimate and wait for confirmation. If the cost cannot be determined, report that and pause. For a read-only connection check, call `list_models` and `list_canvases` only.
4. Supply a unique `request_id` where the tool schema requires it. The caller does not need to supply a generation callback URL. Save the returned `task_id` and `canvas_id`. If the submission outcome is unknown and no task ID was received, reuse the original `request_id` and arguments on retry.
5. Call `get_task` with the returned task ID and read `data.request.state`. Stop on `completed` or `failed`, and ask the user to inspect `conflict` or `needs_review`. For `preparing`, `submitting`, `submitted`, `uncertain`, or a temporary query error, poll the same ID about every 5 seconds for up to 10 minutes, unless the user specifies a different wait. If the client cannot wait or the wait expires, report the last known state and task ID so polling can resume later. Once you have the task ID, use status checks to avoid submitting or charging again.
6. Report the canvas and resulting node IDs after completion. Provide the canvas link if a Web base URL is known, or the canvas ID otherwise. Report direct utility results, such as upload references or voice IDs, when no canvas node is returned.
