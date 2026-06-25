---
name: x2c-socialposter
description: "通过 X2C Open API 管理社交媒体发布和互动。适用场景：(1) 发布文本/媒体帖子到 TikTok、Instagram、Facebook、YouTube、LinkedIn、Twitter 等 13+ 个平台。(2) 定时发布。(3) 管理评论和回复。(4) 上传媒体文件（最大 5GB）获取 CDN 链接。(5) 查看发布历史和已绑定账号。触发词：发布社交媒体、发帖、社交媒体、定时发布、上传媒体、社交账号、评论帖子。"
version: "0.1.0"
license: MIT
author: storyclaw-official
homepage: https://github.com/storyclaw-official/skills
repository: https://github.com/storyclaw-official/skills
requires:
  bins: [python3]
  env: [X2C_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "📱",
      "requires": {
        "bins": ["python3"],
        "env": ["X2C_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "X2C_API_KEY",
      "installSpec": {
        "bins": ["python3"],
        "env": ["X2C_API_KEY"],
        "pip": ["requests"]
      }
    }
  }
---

English | [简体中文](./SKILL.zh-CN.md)

# X2C Social Poster（社交媒体发布器）

**来源**: [storyclaw-official/skills](https://github.com/storyclaw-official/skills) · 控制台: [x2creel.ai](https://www.x2creel.ai/)

通过 X2C Open API 发布帖子、管理评论和上传媒体到 13+ 个社交平台。支持智能上传（大文件自动使用预签名 URL）、平台规则校验、本地文件一步到位发布。

---

## 安装要求

| 要求 | 值 |
|------|-----|
| **可执行文件** | `python3` |
| **环境变量** | `X2C_API_KEY`（必需；从 [X2C 控制台](https://www.x2creel.ai/) 获取） |
| **Pip 依赖** | `requests` |

---

## 首次使用引导

### 步骤 0：检查 API Key

```bash
python3 scripts/x2c_social.py --action check-key
```

- 已设置 → 进入步骤 1
- 未设置 → 引导用户：

```
🔑 X2C API Key 尚未配置，让我们来设置：

1. 访问 https://www.x2creel.ai/social-accounts 注册/登录账号
2. 点击「Link Account」绑定你的社交媒体账号（TikTok、Instagram 等）
3. 在同一页面下方找到「Developer API Key」区域，点击「Get API Key」获取密钥
4. 复制你的 X2C Open API Key，粘贴到对话框中
```

### 步骤 1：验证已绑定账号

```bash
python3 scripts/x2c_social.py --action status
```

---

## 各平台发帖要求速查表

**发布前务必检查目标平台的要求，提前引导用户提供必要信息。**

| 平台 | 标识 | 需要媒体 | 文字上限 | 最大媒体数 | 支持格式 | 关键限制 |
|------|------|:---:|---:|:---:|---|---|
| YouTube | `youtube` | ✅ (视频) | 标题:100 描述:5,000 | 1 视频 | MP4, MOV, AVI, WMV | `--title` 必需（缺失时自动截取帖子文本前 100 字符）。默认可见性 = public。 |
| Instagram | `instagram` | ✅ | 2,200 | 10 (轮播) | JPEG, PNG, MP4 | 必须 Business/Creator 账号。不支持纯文本。最多 5 个 hashtag、3 个 @提及。 |
| TikTok | `tiktok` | ✅ | 2,200 | 1 视频或 35 图 | MP4, JPG, JPEG, WEBP | 图片与视频不可混合。**不支持 PNG**。文本无换行。AI 内容须 `--ai-generated`。 |
| X (Twitter) | `twitter` | ❌ | 280 | 4 图或 1 视频 | JPEG, PNG, GIF, MP4 | 图片与视频不可混合。需 BYO API keys。超 280 字用 `longPost`。 |
| Facebook | `facebook` | ❌ | 63,206 | 10+ | JPEG, PNG, MP4 | 必须是 Page（非个人账号）。 |
| LinkedIn | `linkedin` | ❌ | 3,000 | 9 | JPEG, PNG, GIF, MP4 | 个人或公司页面。 |
| Pinterest | `pinterest` | ✅ | 500 | 5 (轮播) | JPEG, PNG | 需要图片。视频帖需 `--thumbnail`。 |
| Reddit | `reddit` | ❌ | 标题:300 正文:40,000 | 1 | JPEG, PNG, GIF, MP4 | `--title` 必需。`--subreddit` 必需。 |
| GMB | `gmb` | ❌ | 1,500 | 1 | JPEG, PNG, MP4 | 已验证商家。文本不可含电话号码。 |
| Bluesky | `bluesky` | ❌ | 300 | 4 | JPEG, PNG, MP4 | 含链接在内 300 字符。 |
| Threads | `threads` | ❌ | 500 | 10 (轮播) | JPEG, PNG, MP4 | 关联 Instagram 账号。 |
| Snapchat | `snapchat` | ✅ | 160 | 1 | JPEG, PNG, MP4 | 仅支持 1 个媒体。 |
| Telegram | `telegram` | ❌ | 4,096 | 1 | JPEG, PNG, GIF, MP4 | 需 Bot + Channel/Group。 |

### ⚠️ 多平台同时发布注意事项

同时发布到多个平台时，内容保护按顺序执行——**最短的字符限制会覆盖所有平台**（比如同时发 Twitter + LinkedIn，280 字符限制会截断所有平台的文本）。如需不同平台用不同文本，请**分开发布**。

### 平台专属参数

| 参数 | 适用平台 | 说明 |
|------|----------|------|
| `--title` | YouTube, Reddit | 帖子/视频标题（必需）。YouTube 缺失时自动从帖子文本截取前 100 字符。 |
| `--subreddit` | Reddit | 目标 subreddit，不含 `r/`（必需） |
| `--visibility` | YouTube, TikTok | YouTube: `public`/`unlisted`/`private`；TikTok: `PUBLIC_TO_EVERYONE` 等 |
| `--thumbnail` | Pinterest | 视频封面 URL（视频帖必需） |
| `--ai-generated` | TikTok | 标记为 AI 生成内容（AI 内容建议使用） |

---

## 媒体上传

脚本使用**智能上传** —— 根据文件大小自动选择最佳方式：

| 方式 | 文件大小 | 上限 | 工作原理 |
|------|----------|------|----------|
| **直接上传** | ≤ 50MB | ~50MB | 一步 multipart 上传 |
| **预签名 URL** | > 50MB | **5GB** | 获取 S3 预签名 URL → PUT 直传 S3 |

用户无需关心选择哪种方式，脚本自动处理。

### 单独上传

```bash
# 小文件 → 直接上传
python3 scripts/x2c_social.py --action upload --file /path/to/image.jpg

# 大文件 → 自动预签名上传
python3 scripts/x2c_social.py --action upload --file /path/to/large_video.mp4 --folder videos
```

### 一步到位发布本地文件

发布时传入本地文件，脚本**自动上传**后发布：

```bash
# 75MB 视频 → 自动预签名上传 → 发布
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "快来看！🎬" \
  --media-files /path/to/large_video.mp4
```

输出流程：
```json
{"status": "uploading", "file": "large_video.mp4", "size_mb": 75.2, "method": "presigned"}
{"status": "uploaded", "file": "large_video.mp4", "url": "https://v.arkfs.co/...", "method": "presigned"}
{"success": true, "data": {"id": "post_abc123", "postIds": [...]}}
```

---

## 命令列表

### 1. 查看已绑定账号

```bash
python3 scripts/x2c_social.py --action status
```

### 2. 发布帖子

```bash
# 纯文本（适用于：twitter, facebook, linkedin, reddit, gmb, bluesky, threads, telegram）
python3 scripts/x2c_social.py --action publish \
  --platforms twitter facebook \
  --post "Hello world! 🚀"

# 带本地文件 — 自动上传（任意大小，最大 5GB）
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "看这个！🎬" \
  --media-files /path/to/video.mp4

# 带远程 URL
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "看这个！🎬" \
  --media-urls "https://example.com/video.mp4"

# YouTube — 必须提供标题
python3 scripts/x2c_social.py --action publish \
  --platforms youtube \
  --post "视频描述" \
  --title "我的 YouTube 视频" \
  --visibility public \
  --media-files /path/to/video.mp4

# Reddit — 必须提供标题和 subreddit
python3 scripts/x2c_social.py --action publish \
  --platforms reddit \
  --post "帖子正文" \
  --title "讨论：2026年的AI" \
  --subreddit technology

# TikTok — 标记 AI 内容
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok \
  --post "AI 生成内容" \
  --ai-generated \
  --media-files /path/to/ai_video.mp4

# 定时发布
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "即将上线！⏰" \
  --media-files /path/to/video.mp4 \
  --schedule "2026-04-01T12:00:00Z"

# 缩短链接
python3 scripts/x2c_social.py --action publish \
  --platforms twitter linkedin \
  --post "阅读我们的博客：https://example.com/very-long-url" \
  --shorten-links
```

### 3. 查看发布历史

```bash
python3 scripts/x2c_social.py --action posts
python3 scripts/x2c_social.py --action posts --platform tiktok
```

### 4. 删除帖子

```bash
python3 scripts/x2c_social.py --action delete-post --post-id post_abc123
python3 scripts/x2c_social.py --action delete-post --post-id post_abc123 --bulk
```

### 5. 发表评论

```bash
python3 scripts/x2c_social.py --action comment \
  --post-id post_abc123 --platforms tiktok --comment "太棒了！🔥"
```

### 6. 获取评论

```bash
python3 scripts/x2c_social.py --action comments --post-id post_abc123 --platform tiktok
```

### 7. 回复评论

```bash
python3 scripts/x2c_social.py --action reply \
  --comment-id comment_xyz --platforms tiktok --comment "感谢！"
```

### 8. 删除评论

```bash
python3 scripts/x2c_social.py --action delete-comment --comment-id comment_xyz
```

### 9. 单独上传媒体

```bash
python3 scripts/x2c_social.py --action upload --file /path/to/file.mp4 --folder videos
```

---

## 参数说明

| 参数 | 是否必需 | 描述 |
|------|----------|------|
| `--action` | ✅ | 要执行的操作 |
| `--post` | 发布时需要 | 帖子文本内容 |
| `--platforms` | 发布时需要 | 空格分隔的目标平台 |
| `--platform` | 筛选时 | 单个平台筛选 |
| `--media-urls` | ❌ | 远程 URL 或本地路径（自动上传） |
| `--media-files` | ❌ | 本地文件路径，自动上传 |
| `--schedule` | ❌ | ISO 8601 格式的定时发布时间 |
| `--shorten-links` | ❌ | 缩短帖子中的链接 |
| `--title` | YouTube/Reddit | 帖子/视频标题 |
| `--subreddit` | Reddit | 目标 subreddit（不含 `r/`） |
| `--visibility` | YouTube/TikTok | 可见性设置 |
| `--thumbnail` | Pinterest | 视频封面 URL |
| `--ai-generated` | TikTok | 标记为 AI 生成内容 |
| `--post-id` | 帖子操作 | Ayrshare 帖子 ID |
| `--comment-id` | 评论操作 | 评论 ID |
| `--comment` | 评论/回复 | 评论或回复文本 |
| `--bulk` | ❌ | 从所有平台删除 |
| `--file` | 上传时 | 本地文件路径 |
| `--folder` | ❌ | 上传子文件夹（默认：`uploads`） |

---

## 交互引导

**当用户请求模糊时，按以下步骤引导。如果信息充分，直接执行。**

### 步骤 1：新手检查

始终先执行首次使用引导，验证 API Key 和已绑定账号。

### 步骤 2：确认意图

```
你想做什么？
  📝 发布帖子
  📊 查看发布历史
  💬 管理评论
  📤 上传媒体
  🔗 查看已绑定账号
```

### 步骤 3：发布帖子 — 按平台智能引导

1. **问目标平台** → 仅显示已绑定的平台。

2. **根据平台要求主动询问必填项**：
   - YouTube → 询问 `--title` 和 `--visibility`
   - Reddit → 询问 `--title` 和 `--subreddit`
   - Instagram/TikTok/Pinterest/Snapchat → 提醒必须附带媒体
   - TikTok + AI 内容 → 建议使用 `--ai-generated`

3. **询问帖子内容** → 检查文字长度是否超过平台限制。

4. **询问媒体** → 接受本地文件或远程 URL。本地文件自动上传（任意大小）。

5. **询问定时** → 立即发布还是定时。

### 步骤 4：执行并展示

脚本会：
1. 自动上传本地文件（智能选择上传方式）
2. 校验平台规则
3. 构建平台专属 options
4. 发布并返回每个平台的结果

清晰展示结果，高亮显示每个平台的成功/失败状态。

---

## 错误处理

| 状态码 | 含义 | 处理方式 |
|--------|------|----------|
| 400 | 参数缺失或无效 | 检查平台要求并修正 |
| 401 | API Key 无效 | 引导用户验证/重置 Key |
| 500 | 服务器错误 | 重试或通知用户 |

脚本还会在调用 API 前进行**客户端校验**：文字长度、媒体必需检查、必填项（title/subreddit）、媒体数量限制等。致命错误会阻止发布，警告会显示但不阻止。
