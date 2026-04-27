---
name: giggle-generation-drama
description: "Use this feature when users want to generate videos, shoot short films, or view available video styles. Triggering keywords: short film, make video, shoot short film, short video, AI video, generate video from story, short drama, narrated video, cinematic video, available video styles."
version: "0.0.11"
license: MIT
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw":
      {
        "emoji": "📂",
        "requires": {
          "bins": ["python3"],
          "env": ["GIGGLE_API_KEY"],
          "pip": ["requests"]
        },
        "primaryEnv": "GIGGLE_API_KEY"
      }
  }
---

## ⚠️ Review Before Installing

**Please review before installing.** This skill will:

1. **Network** – Calls Giggle.pro API for video generation

**Requirements**: `python3`, `GIGGLE_API_KEY` (system environment variable), pip packages: `requests`

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

---

## Required Setup Before First Use

Before performing any operation, confirm the user has configured the API Key to avoid workflow failure due to auth errors.

- **API Key**: Log in to [Giggle.pro](https://giggle.pro/). On the **main site**, open the **left sidebar** and go to **API Key** (**API 密钥**) — create or copy your key there. **Do not** rely on vague “account settings” alone; the sidebar **API Key** block is the intended entry point.
- **Configuration**: Set system environment variable `GIGGLE_API_KEY`
  - `export GIGGLE_API_KEY=your_api_key`

**Verification steps**:

1. Confirm the user has configured `GIGGLE_API_KEY` in system environment.
2. If not configured, **guide the user**:
   > Open [giggle.pro](https://giggle.pro/) while logged in → **left sidebar** → **API Key** / **API 密钥** → create or copy your key, then run `export GIGGLE_API_KEY=your_api_key` in the terminal.
3. Wait for the user to configure before continuing the workflow.

## Generation Modes

Supports three modes. **Ask the user to select a mode before starting the workflow**. If not specified, default to **Episodes mode** (`director`).

| Mode | project_type | Description |
|------|--------------|-------------|
| **Episodes** | `director` | AI-directed short drama with storyboards and shot language |
| **Narration** | `narration` | Narration-focused video |
| **Short Film** | `short-film` | Story and visuals balanced; cinematic short film |

## Main Workflow: execute_workflow

Use `execute_workflow` to run the full workflow: submit + poll + auto-pay (if needed) + wait for completion. Call once and wait for return.

**Inside the function (for your mental model):** submit task → poll about every 3 seconds → detect pending payment and auto-pay if needed → wait for completion (max ~1 hour) → return video download link or error.

### Continuous progress updates (blocking workflow)

`execute_workflow` **blocks**: submit, pay if needed, and poll (~every 3s) are all **inside** the Python call (up to **~1 hour**). You cannot send per-poll chat between ticks.

1. **Before the call**, inform the user that the **short drama/narration/short film production process** is in progress, typically taking **a few minutes to tens of minutes**, and that a message will be sent again immediately after **function is restored**—the user does not need to contact you proactively.

2. **Initiate the call**, without waiting for the user to ask "Any progress?", proactively push the current progress to the user every 10 seconds, showing which step is currently being done.

3. **After the call is restored**, immediately forward the **complete signed video URL** upon success or a clear error; if the API exposes **`project_id`**, also provide this information upon failure/timeout for the user's subsequent operations or retry.

4. **Non-blocking path** (`create_and_submit` only): If the user wishes, you can submit and return the ID—then query it only when the user inquires.

### Function Signature

```python
execute_workflow(
    diy_story: str,                           # Story/script content (required)
    aspect: str,                              # Aspect ratio: 16:9 or 9:16 (required)
    project_name: str,                        # Project name (required)
    language: str,                            # zh or en (required)—see "Language" below
    video_duration: str = "auto",             # Duration, default "auto" (optional)
    style_id: Optional[int] = None,          # Style ID (optional)
    project_type: str = "director",           # Mode, default "director" (optional)
    character_info: Optional[List[Dict]] = None  # Character images (optional)
)
```

### Language (`language`, required)

Must be **`zh`** or **`en`**. Set it from the **dominant language of the user’s story/prompt and the current dialogue**:

- User writes or dictates the story **mainly in Chinese** (or your conversation with them is **mainly Chinese**) → `language="zh"`.
- User writes or dictates the story **mainly in English** (or the conversation is **mainly English**) → `language="en"`.
- **Mixed story**: choose the language of the **majority of the script body**; if evenly mixed, prefer the language the user used for **the latest explicit instructions**.

This value is passed to the Giggle API as the generation language; it must **not** be omitted or guessed without matching the content.

### Parameter Description

| Parameter | Required | Description |
|-----------|----------|-------------|
| diy_story | yes | Story or script content |
| aspect | yes | Aspect ratio: `16:9` or `9:16` |
| project_name | yes | Project name |
| language | yes | `zh` (Chinese) or `en` (English)—aligned with story/dialogue (see above) |
| video_duration | no | `auto`, `30`, `60`, `120`, `180`, `240`, `300`; default `"auto"` |
| style_id | no | Style ID; omit if not specified |
| project_type | no | `director` / `narration` / `short-film`; default `"director"` |
| character_info | no | Character image list: `[{"name": "Character name", "url": "Image URL"}, ...]` |

### Usage Flow

1. **Introduce and select generation mode** (required): Before generating, **must introduce the three modes** and let the user choose. Display:

   > We support three video generation modes. Please choose:
   >
   > **Episodes (director)**: AI director handles storyboards and shot language. Good for short drama with dialogue and plot.
   >
   > **Narration (narration)**: Narration-focused with visuals. Good for knowledge sharing, news commentary, product introductions.
   >
   > **Short Film (short-film)**: Story and visuals balanced; cinematic shots and pacing. Good for emotional shorts, creative stories, artistic expression.

   Wait for explicit user choice before continuing. If not specified, default to Episodes.

2. **If the user wants to pick a style**: Call `get_styles()` for the style list; show ID, name, category, description; wait for choice before continuing.
3. **If the user provides character image URLs**: Build `character_info` array with `name` and `url` per character.
4. **Set `language` (`zh` / `en`)** per **Language** section from the story and ongoing dialogue—**required before** `execute_workflow`.
5. **Run workflow**:
   - **Before** calling `execute_workflow()`, follow **Continuous progress updates** above: brief start message, realistic ETA—**you will report as soon as it returns**.
   - Call `execute_workflow()` with story, aspect ratio, project name, **and `language`**.
   - Set `project_type` per chosen mode; pass `video_duration` if specified (else `"auto"`); pass `style_id` if chosen; pass `character_info` if provided.
   - **Call once and wait** — the function handles create, submit, poll, pay, and completion; returns download link or error. **Immediately** after return, forward success (full signed URL) or failure to the user.

### Examples

**View style list**:

```python
api = TrusteeModeAPI()
styles_result = api.get_styles()
# Display style list to user
```

**Basic workflow (no duration, no style)**:

```python
api = TrusteeModeAPI()
result = api.execute_workflow(
    diy_story="An adventure story...",
    aspect="16:9",
    project_name="My Video Project",
    language="en",
)
# result contains download URL or error
```

**Specify duration, no style**:

```python
result = api.execute_workflow(
    diy_story="An adventure story...",
    aspect="16:9",
    project_name="My Video Project",
    language="en",
    video_duration="60"
)
```

**Specify duration and style**:

```python
result = api.execute_workflow(
    diy_story="An adventure story...",
    aspect="16:9",
    project_name="My Video Project",
    language="en",
    video_duration="60",
    style_id=142
)
```

**Narration mode**:

```python
result = api.execute_workflow(
    diy_story="Today we'll talk about AI development...",
    aspect="16:9",
    project_name="Narration Video",
    language="en",
    project_type="narration"
)
```

**Short film mode**:

```python
result = api.execute_workflow(
    diy_story="Sunset. An old fisherman rows home alone. The sea glows red...",
    aspect="16:9",
    project_name="Short Film",
    language="en",
    project_type="short-film"
)
```

**With character images** (when user provides character image URLs):

```python
result = api.execute_workflow(
    diy_story="Xiao Ming and Xiao Hong meet in the park, they smile at each other...",
    aspect="16:9",
    project_name="Custom Character Video",
    language="zh",
    character_info=[
        {"name": "Xiao Ming", "url": "https://xxx/xiaoming.jpg"},
        {"name": "Xiao Hong", "url": "https://xxx/xiaohong.jpg"}
    ]
)
```

## Return Value

The function blocks until the task completes (success or failure) or times out (1 hour). Wait for it to return.

**Success** (includes download link):

```json
{
    "code": 200,
    "msg": "success",
    "uuid": "...",
    "data": {
        "project_id": "...",
        "video_asset": {...},
        "status": "completed"
    }
}
```

Return the **full signed URL** to the user (`data.video_asset.download_url`), e.g.:

```
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4?Policy=...&Key-Pair-Id=...&Signature=...&response-content-disposition=attachment
```

Do not strip `response-content-disposition=attachment` or other query params from `download_url`. Do not return unsigned URLs without query params, e.g.:

```
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4
```

**Failure**:

```json
{
    "code": -1,
    "msg": "Error message",
    "data": null
}
```
