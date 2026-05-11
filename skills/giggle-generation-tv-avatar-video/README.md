# 照片数字人口播视频技能（中文）

基于 **Giggle** 侧封装的照片驱动数字人口播生成能力：人像图 URL + **TTS（音色 ID / 克隆音频）** 或 **整段音频驱动**，提交任务后轮询至完成，输出成片链接。

遵循 [Agent Skills](https://agentskills.io/specification) 思路，可在 Cursor / Claude Code 等环境中加载 `SKILL.md`。

## 功能概要

- 三种驱动（互斥）：**TTS + voice_over_id**、**TTS + clone_audio.url**、**drive_audio.url（对口型）**
- 子命令：`run`（默认）、`submit`、`query`
- 鉴权：请求头 **`x-auth`**，密钥来自环境变量 **`GIGGLE_API_KEY`**（在 [giggle.pro](https://giggle.pro/) 登录后，左侧栏 **API Key / API 密钥** 获取）

## 快速开始

在本目录下：

```bash
export GIGGLE_API_KEY="<你的密钥>"
pip install -r scripts/requirements.txt

python scripts/tv_avatar_video.py run \
  --image-url "https://example.com/portrait.jpg" \
  --tts-script "欢迎使用。" \
  --voice-over-id "<voice_over_id>"
```

可选：自建或本地网关时覆盖地址：

```bash
export GIGGLE_API_BASE="http://localhost:8090"
```

详细请求体与参数说明见 [references/tv_avatar_video.md](references/tv_avatar_video.md)；助手流程见 [SKILL.md](SKILL.md)。

## 目录结构

```
gen-avatar4-zh/
├── SKILL.md
├── README.md
├── LICENSE.txt
├── references/
│   ├── tv_avatar_video.md
│   ├── credentials.md
│   └── error_handling.md
└── scripts/
    ├── tv_avatar_video.py
    ├── requirements.txt
    └── shared/
```

## License

[LICENSE.txt](LICENSE.txt)
