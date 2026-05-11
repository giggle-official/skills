# 数字人口播视频 CLI（封装 API）

使用人像图片 **URL** 与下列 **三种驱动之一** 创建口播视频。脚本：`scripts/tv_avatar_video.py`。

**说明**：以下 JSON 仅用于理解字段；实际调用建议使用 CLI，由脚本组装请求体并轮询。

---

## 1）TTS + 已有 `voice_over_id`

`drive_mode`: **1**。需提供 `tts_script` 与 `voice_over_id`，**不要**填 `clone_audio`。

示例：

```json
{
  "drive_mode": 1,
  "image": { "url": "https://example.com/face.jpg" },
  "tts_script": "欢迎使用，这是一条文案驱动的数字人口播示例。",
  "voice_over_id": "zeeTdrCqbhpVKOucLtOKdhytM7rbJx5t",
  "mode_type": "1"
}
```

CLI：

```bash
python scripts/tv_avatar_video.py run \
  --image-url "https://example.com/face.jpg" \
  --tts-script "欢迎使用，这是一条文案驱动的数字人口播示例。" \
  --voice-over-id "zeeTdrCqbhpVKOucLtOKdhytM7rbJx5t"
```

---

## 2）TTS + `clone_audio`（克隆/参考音色）

`drive_mode`: **1**。需提供 `tts_script` 与 `clone_audio.url`，**不要**填 `voice_over_id`。可选 `voice_speed`（示例中为 `1`）。

示例：

```json
{
  "drive_mode": 1,
  "image": { "url": "https://example.com/face.jpg" },
  "tts_script": "欢迎使用，这是一条文案驱动的数字人口播示例。",
  "clone_audio": { "url": "https://example.com/reference_voice.mp3" },
  "voice_speed": 1,
  "mode_type": "1"
}
```

CLI：

```bash
python scripts/tv_avatar_video.py run \
  --image-url "https://example.com/face.jpg" \
  --tts-script "欢迎使用，这是一条文案驱动的数字人口播示例。" \
  --clone-audio-url "https://example.com/reference_voice.mp3" \
  --voice-speed 1
```

---

## 3）音频驱动（对口型）

`drive_mode`: **2**。使用 `drive_audio.url`，**不要**与 `tts_script` / `voice_over_id` / `clone_audio` 同时使用。

示例：

```json
{
  "drive_mode": 2,
  "image": { "url": "https://example.com/face.jpg" },
  "drive_audio": { "url": "https://example.com/speech.mp3" },
  "mode_type": "1"
}
```

CLI：

```bash
python scripts/tv_avatar_video.py run \
  --image-url "https://example.com/face.jpg" \
  --drive-audio-url "https://example.com/speech.mp3"
```

---

## 提交与查询

**提交**（成功时示例）：

```json
{
  "code": 200,
  "msg": "success",
  "uuid": "...",
  "data": { "task_id": "53e147de-7f61-4bef-b13d-78e401aa32b2" }
}
```

**查询**（进行中字段依网关为准；完成时）：

```json
{
  "code": 200,
  "msg": "success",
  "uuid": "...",
  "data": {
    "task_id": "...",
    "urls": ["https://example.com/result.mp4"],
    "status": "completed",
    "err_msg": ""
  }
}
```

成片链接：**`data.urls[0]`**。脚本在 `status == completed` 时默认将该 URL 打印到 stdout。

---

## 子命令

| 子命令 | 说明 |
|--------|------|
| `run` | 提交并轮询直至完成 |
| `submit` | 仅提交，stdout 打印 `task_id` |
| `query` | 对已有 `task_id` 继续轮询（超时恢复） |

### 通用选项

| 选项 | 说明 |
|------|------|
| `--image-url` | 人像图 URL（必填） |
| `--mode-type` | 默认 `"1"` |
| `--timeout` / `--interval` | 轮询上限与间隔（秒） |
| `--output PATH` | 将成片 URL 下载到本地 |
| `--json` | 打印最后一次查询的完整响应 JSON |
| `-q` | 静默进度 |
| `--base-url` | 单次命令覆盖 `GIGGLE_API_BASE` |

### `query`

```bash
python scripts/tv_avatar_video.py query --task-id "<task_id>" --timeout 1200
```

---

## 批量示例

```bash
T1=$(python scripts/tv_avatar_video.py submit \
  --image-url "https://example.com/a.jpg" \
  --tts-script "第一段" \
  --voice-over-id "<id>" -q)
T2=$(python scripts/tv_avatar_video.py submit \
  --image-url "https://example.com/b.jpg" \
  --tts-script "第二段" \
  --voice-over-id "<id>" -q)

python scripts/tv_avatar_video.py query --task-id "$T1"
python scripts/tv_avatar_video.py query --task-id "$T2"
```
