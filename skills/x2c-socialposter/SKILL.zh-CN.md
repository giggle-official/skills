---
name: x2c-socialposter
description: "通过 X2C Open API 管理社交媒体发布、数据分析、消息收发和内容创作。适用场景：(1) 发布文字/媒体帖子到 TikTok、Instagram、Facebook、YouTube、LinkedIn、Twitter 等 13+ 平台。(2) 定时或智能定时发布（自动选择最佳时间）。(3) 管理评论和回复。(4) 上传媒体文件（最大 5GB）。(5) 查看发布历史和账号数据分析。(6) 用 AI 生成帖子文案和 Hashtag 推荐。(7) 收发 IG/FB/Twitter 私信。(8) 创建可追踪短链接。(9) 查看 Google Business 评论。(10) 品牌信息查询。触发词：发布社交媒体、发帖、定时发布、智能定时、上传媒体、社交账号、评论、数据分析、Hashtag、生成文案、私信、短链接、品牌查询、GMB 评论。"
version: "0.2.0"
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

# X2C Social Poster（社交媒体全功能管理）

**来源**: [storyclaw-official/skills](https://github.com/storyclaw-official/skills) · 控制台: [x2cpool.com](https://x2cpool.com/)

通过 X2C Open API，在 13+ 个社交平台上发布内容、管理评论、查看数据分析、收发私信、生成 AI 文案，一站式管理你的社交媒体。

---

## 安装要求

| 要求 | 值 |
|------|-----|
| **可执行文件** | `python3` |
| **环境变量** | `X2C_API_KEY`（必需；从 [X2C 控制台](https://x2cpool.com/) 获取） |
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

1. 访问 https://x2cpool.com 注册/登录账号
2. 点击「Link Account」绑定社交媒体账号
3. 进入 Developer → API Keys，创建新密钥
4. 复制密钥并粘贴到对话框中
```

### 步骤 1：验证已绑定账号

```bash
python3 scripts/x2c_social.py --action status
```

显示已绑定的平台后，**主动提问**：
> "你已绑定：TikTok、Instagram、YouTube。要查看账号数据分析（粉丝、趋势）吗？[查看 / 跳过]"

---

## 各平台发帖要求速查表

| 平台 | 标识 | 需要媒体 | 文字上限 | 最大媒体数 | 支持格式 | 关键限制 |
|------|------|:---:|---:|:---:|---|---|
| YouTube | `youtube` | ✅ (视频) | 标题:100 描述:5,000 | 1 视频 | MP4, MOV, AVI, WMV | 标题缺失时自动截取正文前 100 字符。默认可见性 = public。 |
| Instagram | `instagram` | ✅ | 2,200 | 10 (轮播) | JPEG, PNG, MP4 | 必须 Business/Creator 账号。不支持纯文字。最多 5 个 hashtag、3 个 @提及。 |
| TikTok | `tiktok` | ✅ | 2,200 | 1 视频或 35 图 | MP4, JPG, JPEG, WEBP | 图片与视频不可混合。**不支持 PNG**。文本无换行。AI 内容须 `--ai-generated`。 |
| X (Twitter) | `twitter` | ❌ | 280 | 4 图或 1 视频 | JPEG, PNG, GIF, MP4 | 图片与视频不可混合。需 BYO API keys。 |
| Facebook | `facebook` | ❌ | 63,206 | 10+ | JPEG, PNG, MP4 | 必须是 Page（非个人账号）。 |
| LinkedIn | `linkedin` | ❌ | 3,000 | 9 | JPEG, PNG, GIF, MP4 | 个人或公司页面。 |
| Pinterest | `pinterest` | ✅ | 500 | 5 (轮播) | JPEG, PNG | 需要图片。视频帖需 `--thumbnail`。 |
| Reddit | `reddit` | ❌ | 标题:300 正文:40,000 | 1 | JPEG, PNG, GIF, MP4 | `--title` 必需。`--subreddit` 必需。 |
| GMB | `gmb` | ❌ | 1,500 | 1 | JPEG, PNG, MP4 | 已验证商家。文本不可含电话号码。 |
| Bluesky | `bluesky` | ❌ | 300 | 4 | JPEG, PNG, MP4 | 含链接在内 300 字符。 |
| Threads | `threads` | ❌ | 500 | 10 (轮播) | JPEG, PNG, MP4 | 关联 Instagram 账号。 |
| Snapchat | `snapchat` | ✅ | 160 | 1 | JPEG, PNG, MP4 | 仅支持 1 个媒体。 |
| Telegram | `telegram` | ❌ | 4,096 | 1 | JPEG, PNG, GIF, MP4 | 需 Bot + Channel/Group。 |

### ⚠️ 多平台同时发布注意

同时发布多平台时，**最短字符限制会覆盖所有平台**。需要不同文案时，请分开发布。

---

## 命令列表

### 原有命令

#### 1. 查看已绑定账号

```bash
python3 scripts/x2c_social.py --action status
```

#### 2. 发布帖子

```bash
# 纯文本
python3 scripts/x2c_social.py --action publish \
  --platforms twitter facebook \
  --post "Hello world! 🚀"

# 带本地文件（自动上传，最大 5GB）
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "快来看！🎬" \
  --media-files /path/to/video.mp4

# 带远程 URL
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok \
  --post "快来看！🎬" \
  --media-urls "https://example.com/video.mp4"

# YouTube（标题缺失时自动生成）
python3 scripts/x2c_social.py --action publish \
  --platforms youtube \
  --post "视频描述" \
  --title "我的 YouTube 视频" \
  --visibility public \
  --media-files /path/to/video.mp4

# Reddit（标题和 subreddit 必需）
python3 scripts/x2c_social.py --action publish \
  --platforms reddit \
  --post "帖子正文" \
  --title "讨论：2026年的AI" \
  --subreddit technology

# TikTok 标记 AI 内容
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok \
  --post "AI 生成内容" \
  --ai-generated \
  --media-files /path/to/video.mp4

# 定时发布
python3 scripts/x2c_social.py --action publish \
  --platforms tiktok instagram \
  --post "即将上线！⏰" \
  --media-files /path/to/video.mp4 \
  --schedule "2026-04-01T12:00:00Z"
```

#### 3–9. 历史 / 删除 / 评论 / 上传

```bash
# 查看发布历史
python3 scripts/x2c_social.py --action posts
python3 scripts/x2c_social.py --action posts --platform tiktok

# 删除帖子
python3 scripts/x2c_social.py --action delete-post --post-id post_abc123 --bulk

# 发表评论
python3 scripts/x2c_social.py --action comment \
  --post-id post_abc123 --platforms tiktok --comment "太棒了！🔥"

# 获取评论
python3 scripts/x2c_social.py --action comments --post-id post_abc123 --platform tiktok

# 回复评论
python3 scripts/x2c_social.py --action reply --comment-id cmt_xyz --comment "感谢！"

# 删除评论
python3 scripts/x2c_social.py --action delete-comment --comment-id cmt_xyz

# 单独上传媒体
python3 scripts/x2c_social.py --action upload --file /path/to/file.mp4 --folder videos
```

---

### 新功能命令（v2.0）

#### 10. AI 文案生成

根据主题或提示词自动生成适合目标平台的帖子文案。

```bash
# 生成 TikTok 文案（活跃风格）
python3 scripts/x2c_social.py --action generate \
  --gen-prompt "推广一部关于时间循环的 AI 短剧新集" \
  --platform tiktok \
  --gen-hashtags \
  --gen-emojis \
  --tone energetic \
  --language zh

# 生成 Twitter 文案（限 280 字符）
python3 scripts/x2c_social.py --action generate \
  --gen-prompt "X2C 社交工具上线公告" \
  --platform twitter \
  --gen-hashtags \
  --max-chars 280
```

`--tone` 可选：`energetic`（活跃）、`casual`（随性）、`professional`（专业）、`inspiring`（励志）等。
`--language` 可选：`en`、`zh`、`ja` 等。

#### 11. Hashtag 推荐

根据文案内容获取 AI 排名的 Hashtag 建议。

```bash
python3 scripts/x2c_social.py --action hashtags \
  --text "AI 生成的关于时间旅行的短剧" \
  --platform instagram \
  --max-tags 10 \
  --language zh
```

#### 12. 智能定时发布（最佳时间）

自动选择各平台的最佳发布时间，无需猜测。

```bash
python3 scripts/x2c_social.py --action auto-schedule \
  --platforms tiktok instagram \
  --post "新集上线了！🎬" \
  --media-files /path/to/video.mp4
```

#### 13. 帖子数据分析（通过 X2C 发布的帖子）

```bash
# 查看帖子分析
python3 scripts/x2c_social.py --action analytics-post \
  --post-id post_abc123 \
  --platforms instagram tiktok

# 通过平台原生 ID 查询
python3 scripts/x2c_social.py --action analytics-post \
  --post-id native_id_123 \
  --platforms youtube \
  --search-platform-id
```

数据延迟说明：
- TikTok：数据延迟 24–48 小时
- Pinterest：数据延迟 24–72 小时
- Instagram：需 ≥ 100 粉丝
- Facebook：需 ≥ 100 主页点赞

#### 14. 外部帖子数据分析

分析非通过 X2C 发布的帖子。

```bash
# 通过 URL 查询
python3 scripts/x2c_social.py --action analytics-social \
  --platform youtube \
  --url "https://youtube.com/watch?v=VIDEO_ID"

# 通过原生 ID 查询
python3 scripts/x2c_social.py --action analytics-social \
  --platform tiktok \
  --ext-id "7123456789"
```

支持平台：`youtube`, `tiktok`, `instagram`, `facebook`, `twitter`, `linkedin`。

#### 15. 账号数据分析

查看粉丝数、受众人口统计、历史趋势。

```bash
# 基础账号分析
python3 scripts/x2c_social.py --action analytics-account \
  --platforms instagram youtube tiktok

# 含每日趋势和 60 天数据
python3 scripts/x2c_social.py --action analytics-account \
  --platforms instagram \
  --daily \
  --period-60
```

#### 16. 完整发布历史

```bash
# 全平台最近 30 天
python3 scripts/x2c_social.py --action history --last-days 30

# 特定平台，最近 50 条，仅成功的
python3 scripts/x2c_social.py --action history \
  --platform instagram \
  --last-records 50 \
  --history-status success
```

#### 17. 平台 Feed / 时间线

```bash
python3 scripts/x2c_social.py --action feed \
  --platform twitter \
  --last-records 20
```

#### 18. 私信管理

```bash
# 查看私信列表
python3 scripts/x2c_social.py --action messages --platform instagram

# 发送私信
python3 scripts/x2c_social.py --action send-message \
  --platform instagram \
  --recipient-id ig_user_id_123 \
  --message "感谢关注！😊"

# 在对话中回复
python3 scripts/x2c_social.py --action send-message \
  --platform instagram \
  --conversation-id conv_abc \
  --message "很棒的问题！"

# 带媒体的私信
python3 scripts/x2c_social.py --action send-message \
  --platform twitter \
  --recipient-id twitter_user_id \
  --message "给你看这个！" \
  --media-url "https://cdn.example.com/image.jpg"
```

支持平台：`instagram`, `facebook`, `twitter`。

#### 19. 短链接 + UTM 追踪

```bash
# 创建可追踪短链接
python3 scripts/x2c_social.py --action links \
  --link-url "https://x2creel.ai/episode/123" \
  --utm-source instagram \
  --utm-medium bio \
  --utm-campaign drama_s2

# 查看已有短链接的点击分析
python3 scripts/x2c_social.py --action links \
  --link-id short_link_abc123
```

#### 20. Google Business 评论

```bash
python3 scripts/x2c_social.py --action reviews --last-days 30
```

#### 21. 品牌信息查询

```bash
python3 scripts/x2c_social.py --action brand --domain x2creel.ai
```

返回：品牌主色、Logo、官方社交链接、品牌描述等。

---

## 参数说明

| 参数 | 适用操作 | 描述 |
|------|----------|------|
| `--action` | 全部 | 要执行的操作 |
| `--post` | publish, auto-schedule | 帖子文本内容 |
| `--platforms` | publish, auto-schedule, analytics | 空格分隔的目标平台 |
| `--platform` | posts, comments, messages, feed, history, analytics-social | 单个平台 |
| `--media-urls` | publish, auto-schedule | 远程 URL 或本地路径（自动上传） |
| `--media-files` | publish, auto-schedule | 本地文件路径，自动上传 |
| `--schedule` | publish | ISO 8601 定时发布时间 |
| `--shorten-links` | publish | 缩短帖子中的链接 |
| `--title` | publish | 标题（YouTube 缺失自动生成；Reddit 必需） |
| `--subreddit` | publish | 目标 subreddit（不含 `r/`，Reddit 必需） |
| `--visibility` | publish | 可见性：public/unlisted/private（YouTube）等 |
| `--thumbnail` | publish | 视频封面 URL（Pinterest 视频帖必需） |
| `--ai-generated` | publish | 标记为 AI 生成内容（TikTok） |
| `--post-id` | comment, comments, delete-post, analytics-post | Ayrshare 帖子 ID |
| `--comment-id` | reply, delete-comment | 评论 ID |
| `--comment` | comment, reply | 评论或回复文本 |
| `--bulk` | delete-post | 从所有平台删除 |
| `--file` | upload | 本地文件路径 |
| `--folder` | upload, publish | 上传子文件夹（默认：`uploads`） |
| `--ext-id` | analytics-social | 平台原生帖子/视频 ID |
| `--url` | analytics-social | 帖子 URL（外部分析） |
| `--search-platform-id` | analytics-post | 按平台原生 ID 查询 |
| `--daily` | analytics-account | 含每日趋势 |
| `--quarters` | analytics-account | 季度聚合（YouTube） |
| `--period-60` | analytics-account | 60 天滚动窗口 |
| `--last-message-id` | messages | 私信分页游标 |
| `--message` | send-message | 私信文本 |
| `--recipient-id` | send-message | 收件人用户 ID |
| `--conversation-id` | send-message | 对话 ID |
| `--media-url` | send-message | 私信附加媒体 URL |
| `--last-records` | history, feed | 最多返回条数 |
| `--last-days` | history, reviews | 往前查询天数 |
| `--history-status` | history | 状态筛选：success / failed / scheduled |
| `--text` | hashtags | Hashtag 推荐的主题/文本 |
| `--max-tags` | hashtags | 最多返回 Hashtag 数（默认 10） |
| `--language` | hashtags, generate | 语言代码（en、zh、ja 等） |
| `--auto-schedule-type` | auto-schedule | 策略：next（默认） |
| `--gen-prompt` | generate | AI 生成的主题/提示词 |
| `--gen-hashtags` | generate | 在生成文案中包含 Hashtag |
| `--gen-emojis` | generate | 在生成文案中包含 Emoji |
| `--tone` | generate | 语气：energetic / casual / professional / inspiring |
| `--max-chars` | generate | 生成文案的最大字符数 |
| `--link-url` | links | 要缩短/追踪的 URL |
| `--link-id` | links | 已有短链接 ID（查看点击分析） |
| `--utm-source` | links | UTM source（如 instagram） |
| `--utm-medium` | links | UTM medium（如 bio） |
| `--utm-campaign` | links | UTM campaign 名称 |
| `--domain` | brand | 品牌查询的域名（如 x2creel.ai） |

---

## 交互引导

**这是最重要的一节。** 处理用户请求时，始终遵循以下原则：

### 核心原则：主动给出方案，而不是问开放式问题

根据已知信息，**直接给出具体方案**，让用户选择接受、修改或跳过。

| ❌ 不要这样问 | ✅ 应该这样做 |
|------------|------------|
| "要加 Hashtag 吗？" | 运行 hashtags API 后直接说：「推荐标签：`#AI短剧 #TikTok #短视频`，加入文案？[全加 / 自选 / 跳过]」 |
| "你想什么时候发？" | 「推荐**智能定时**，系统自动选择各平台最佳时段。[智能定时✓ / 立即发 / 自定义时间]」 |
| "要看数据吗？" | 发布后直接说：「已记录帖子 ID。TikTok 数据约 24 小时后可查，届时告诉我即可。」 |
| "用什么语气？" | 根据平台和话题推断：「我会用**活跃风格**来写 TikTok 文案，可以吗？[可以 / 改为：___]」 |

---

### 智能发布全流程

用户想发帖时，按以下步骤引导。**用户已提供的信息可直接跳过对应步骤。**

#### 阶段一：账号检查（每次会话一次）

```bash
python3 scripts/x2c_social.py --action check-key
python3 scripts/x2c_social.py --action status
```

显示已绑定平台后，主动提问：
> 「你已绑定：TikTok、Instagram、YouTube。要同时查看账号数据分析吗？[查看 / 跳过]」

#### 阶段二：AI 文案生成

如果用户只描述了主题，还没有写好文案，**主动提供 AI 文案**，无需等用户开口：

```bash
python3 scripts/x2c_social.py --action generate \
  --gen-prompt "[用户描述的主题]" \
  --platform [主要平台] \
  --gen-hashtags --gen-emojis \
  --tone [根据语境推断，默认 energetic] \
  --language [根据用户语言推断，默认 zh]
```

展示 2–3 个备选文案（或头条方案），让用户选择或修改，无需重新输入。

#### 阶段三：Hashtag 建议（自动运行，无需询问）

文案确定后，**立即自动**运行：

```bash
python3 scripts/x2c_social.py --action hashtags \
  --text "[确认后的文案]" \
  --platform [主要平台] \
  --max-tags 8
```

直接展示结果：
> 「推荐标签：`#AI短剧`（高相关）`#短视频`（高相关）`#TikTok`（中相关）。全部加入？[全加 / 自选 / 跳过]」

用户说「全加」或选择部分时，直接更新文案，无需重新输入。

#### 阶段四：平台专属检查

根据已确认的平台：
- **YouTube**：展示自动生成的标题，确认可见性（默认 `public`）。
- **Reddit**：确认 `--title` 和 `--subreddit`。
- **Instagram/TikTok/Snapchat**：提醒需要媒体，询问文件路径。
- **TikTok + AI 内容**：建议加 `--ai-generated`。

#### 阶段五：发布时间选择（智能定时为默认推荐）

> 「选择发布时间：
> ✨ **智能定时** — 系统自动选择各平台最佳时段（推荐）
> ⚡ **立即发布**
> 🕐 **自定义时间** — 如 2026-05-01T18:00:00Z
>
> [智能定时] [立即发] [自定义时间]」

- 智能定时 → 用 `--action auto-schedule`
- 自定义时间 → 用 `--action publish --schedule "ISO8601"`
- 立即发布 → 用 `--action publish`

#### 阶段六：发布后主动提供选项

成功发布后，**始终**用一个紧凑的区块展示快捷操作：

```
✅ 已发布到 [平台列表]！帖子 ID：post_abc123

快捷操作（任选，或全部跳过）：
🔗 创建可追踪短链接      → 要/不要
📊 数据分析：[各平台数据可用时间说明]
💬 查看/回复评论？        → 要/不要
```

如果帖文中有 URL，**自动提出创建短链接**：
> 「你的帖子包含链接。要创建带 UTM 追踪的短链接吗？我会自动使用 `utm_source=[平台]`。[创建 / 跳过]」

---

### 基于上下文主动触发的功能

以下情况无需用户主动提出，**Claude 主动识别并推荐**：

| 触发情境 | 主动提供的内容 | 执行命令 |
|---------|--------------|---------|
| `status` 显示已绑定账号后 | 「要查看账号数据分析吗？我可以展示粉丝数和趋势。」 | `analytics-account --platforms [全部已绑定]` |
| `posts` / `history` 列出帖子后 | 「要查看其中某篇的数据吗？[展示帖子 ID 列表供选择]」 | `analytics-post --post-id [选中的]` |
| GMB 在已绑定平台中 | 「你绑定了 Google Business，要查看近期评论吗？」 | `reviews --last-days 30` |
| 用户提到某个网站或品牌 | 「要查询 [域名] 的品牌信息吗？包括 Logo、品牌色、社交链接。」 | `brand --domain [域名]` |
| IG / FB / Twitter 已绑定 | 「要查看你的私信吗？」 | `messages --platform [平台]` |
| 用户说「查看历史」 | 提供带筛选器的完整历史 | `history --last-days 30` |
| 帖文包含 URL | 「要创建可追踪短链接吗？」 | `links --link-url [url] --utm-source [平台]` |

---

### 判断用户意图（请求模糊时）

```
你想做什么？

📝 创建并发布帖子          → 智能发布全流程（阶段一至六）
🤖 生成帖子文案/灵感        → AI 生成 + Hashtag 推荐
⏰ 智能定时发布             → 最佳时间自动发布
📊 查看数据分析             → 帖子或账号分析
💬 管理评论/私信            → 评论、回复或私信
📜 浏览发布历史             → 带筛选器的完整历史
📤 上传媒体文件             → 单独上传
🔗 创建短链接               → 链接创建 + UTM 追踪
⭐ 查看 GMB 评论            → Google Business 评论
🔍 品牌信息查询             → 品牌查询
🔗 查看已绑定账号           → 账号状态
```

---

## 错误处理

| 状态码 | 含义 | 处理方式 |
|--------|------|----------|
| 400 | 参数缺失或无效 | 检查平台要求并修正 |
| 401 | API Key 无效 | 引导用户在 x2cpool.com 验证/重置 |
| 402 | 需要社交订阅 | 引导用户在 x2cpool.com 检查订阅状态 |
| 429 | 触发限流 | 等待 5 分钟后重试 |
| 500 | 服务器错误 | 重试或通知用户 |

数据延迟说明（提前告知用户）：
- **TikTok**：数据延迟 24–48 小时
- **Pinterest**：数据延迟 24–72 小时
- **Instagram**：账号分析需 ≥ 100 粉丝
- **Facebook**：主页分析需 ≥ 100 主页点赞
