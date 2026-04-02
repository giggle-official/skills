---
name: news-to-video-monetizer
version: "1.0.0"
description: "一键将全网热点新闻变成可赚钱的短视频。自动采集热点 → 智能筛选 → AI生成视频 → 发布到X2C平台 → 流量变现。支持7种风格、7种分类、多平台热搜。触发词：一键制作、查看热点、查看收益、做视频、热点视频、news to video、自动制作、视频变现。"
license: MIT
author: x2c-automation
requires:
  bins: [node, npm, python3, curl]
  skills: [dailyhot-api, storyclaw-x2c-ai-director, storyclaw-x2c-publish]
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: [node, npm, python3, curl]
      skills: [dailyhot-api, storyclaw-x2c-ai-director, storyclaw-x2c-publish]
    primaryEnv: X2C_API_KEY
---

# 🎬 News-to-Video Monetizer

一键将全网热点新闻变成可以赚钱的短视频。

## 能力概览

- **自动采集** — 实时抓取抖音、微博、B站等平台热搜
- **智能筛选** — 按赛道关键词匹配最有价值的话题，15天语义去重
- **AI制作** — 自动生成剧本、角色、分镜、渲染视频（10-20分钟）
- **自动发布** — 视频完成后直接发布到 X2C 平台
- **流量变现** — 审核通过即获得流量分成，收益每日释放

## 依赖 Skills

本 Skill 是一个**编排层**，依赖以下 3 个底层 Skill 工作：

| Skill | 职责 |
|-------|------|
| `dailyhot-api` | 热点采集（抖音/微博/B站/头条/快手等 40+ 平台）|
| `storyclaw-x2c-ai-director` | AI编剧 + 视频生产（X2C Cloud API）|
| `storyclaw-x2c-publish` | 视频发布 + 钱包/收益管理（X2C Cloud API）|

如果缺少任何一个，提示用户安装：
```bash
openclaw skill install dailyhot-api
openclaw skill install storyclaw-x2c-ai-director
openclaw skill install storyclaw-x2c-publish
```

## 首次使用引导

当检测到用户尚未配置时，按以下顺序引导：

### Step 1: 绑定 X2C 账号
检查是否已有 X2C API Key（通过 `storyclaw-x2c-ai-director` 的 `check-binding` 命令）。
如果未绑定：
> 🔑 首次使用需要绑定 X2C 账号：
> 1. 打开 https://www.x2creel.ai 注册/登录
> 2. 进入 个人中心 → API管理 → 复制 API Key
> 3. 把 API Key 发给我（格式：`x2c_sk_xxx`）

收到后执行：
```bash
cd ~/.openclaw/skills/storyclaw-x2c-ai-director
USER_ID="$USER_ID" node scripts/ad-account-manager.js verify-key <api_key>
```

### Step 2: 选择内容方向
询问用户：
> 📝 设置你的内容方向：
> - **赛道**（可多选）：时尚穿搭 / 娱乐八卦 / 科技数码 / 财经金融 / 游戏电竞 / 其他
> - **关键词**：用于筛选热点，例如「美女, 穿搭, 网红, 明星」
> - **目标受众**：例如「大学生」「白领」「宝妈」

### Step 3: 选择视频参数
> 🎬 设置视频默认参数：
> - ⏱️ 时长: 60秒($2.99) / 120秒($5.99) / 180秒($7.99) / 300秒($9.99)
> - 📐 比例: 竖屏(9:16) / 横屏(16:9)
> - 🎨 风格: 3D古风 / 2D漫剧 / 吉卜力 / 皮克斯 / 写实 / 二次元 / 国风水墨
> - 📂 分类: 玄幻异能 / 悬疑惊悚 / 科幻末世 / 都市复仇 / 热门综合 / 霸总甜宠 / 仙侠古装

配置保存到 workspace 的 `config.json`。如果 `config.json` 不存在，从本 Skill 目录下的 `templates/config.template.json` 复制一份。

## 用户指令

| 指令 | 效果 |
|------|------|
| **一键制作** | 全流程：采集 → 筛选 → 制作 → 发布 → 审核 |
| **查看热点** | 展示全网实时热搜 |
| **做一个关于 [话题] 的视频** | 指定话题制作 |
| **查看今日任务** | 所有 Task 状态一览 |
| **查看收益** | 账户余额 + 收益流水 |
| **查看余额** | 积分 / X2C / USDC |
| **修改配置** | 调整赛道、关键词、视频参数 |
| **绑定账号** | 绑定 X2C API Key |
| **draft mode** | 只制作不发布 |

新会话启动时显示能力菜单：

> 🎬 x2c自动化 已就绪！
>
> **📌 核心功能**
> 1️⃣ **一键制作** — 自动采集热点 → 生成视频 → 发布到 X2C
> 2️⃣ **查看热点** — 获取全网实时热搜趋势报告
> 3️⃣ **指定话题制作** — 给我一个主题，我来生成视频
>
> **📊 管理面板**
> 4️⃣ **查看今日任务** — 所有 Task 链路状态一览
> 5️⃣ **查看收益** — 账户余额 + 收益流水
> 6️⃣ **修改配置** — 调整赛道 / 关键词 / 视频参数
>
> **⚙️ 账户**
> 7️⃣ **绑定 X2C 账号** — 首次使用前必须完成
> 8️⃣ **查看余额** — 积分 + X2C + USDC 余额

## Pipeline 规则（5 节点生命周期）

### 执行顺序
```
Node 1: 采集 → Node 2: 筛选 → Node 3: 制作 → Node 4: 发布 → Node 5: 审核
```

不可跳步、不可乱序。auto_publish=true 时制作完成后自动发布。

### Task 追踪
- 每次 pipeline 创建一个 Task 记录：`tasks/TASK-{YYYYMMDD}-{SEQ:3}.json`
- Task 在 Node 5（审核）完成后结束
- 已完成 Task 保留 30 天，失败 Task 保留 7 天，过期归档

### 收益独立
- 收益是**账户级数据**，不绑定单个 Task
- 通过 `wallet/balance` 和 `wallet/transactions` API 获取
- 作为独立的「收益」面板展示

### 关键规则
1. **视频不存本地** — 视频在 X2C 云端，本地只存 Task 元数据 JSON
2. **封面取自 API** — 使用 `video_asset.thumbnailUrl` 或 `storyboard_shots[0].imageUrl`，不手动生成
3. **URL 完整展示** — 不截断任何链接
4. **失败不自动重试** — 视频制作每次扣积分，失败后报告用户等指令
5. **15天语义去重** — 不重复制作相同话题
6. **确认后执行** — 每次 pipeline 先确认参数再开始

## 采集脚本

用于热点采集和关键词筛选：

```bash
cd ~/.openclaw/skills/dailyhot-api && bash scripts/ensure_running.sh
```

采集逻辑（Agent 内嵌 Python 执行）：
1. 从 DailyHot API（localhost:6688）抓取多平台热榜
2. 用 config.json 中的 keywords 做关键词匹配
3. 按匹配度 + 热度排序
4. 对比已完成 Task 做 15 天去重
5. 返回 Top N 话题

## 视频制作

使用 `storyclaw-x2c-ai-director` 的 `ad-producer.js`：

```bash
cd ~/.openclaw/skills/storyclaw-x2c-ai-director
USER_ID="$USER_ID" node scripts/ad-producer.js full-workflow "话题描述" \
  --mode short_video --duration 60 --ratio 9:16 --style "2D漫剧" --language zh
```

- 剧本生成：10积分，约30秒
- 视频渲染：299积分（60秒），约10-20分钟
- 完成后从 `video/query` API 获取 video_url 和 thumbnailUrl

## 发布

使用 `storyclaw-x2c-publish` 的 distribution API：

```bash
curl -m 60 -X POST "$X2C_API_BASE_URL" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $X2C_API_KEY" \
  -d '{
    "action": "distribution/publish",
    "title": "视频标题",
    "description": "描述",
    "category_id": "分类UUID",
    "cover_url": "封面图URL（从thumbnailUrl获取）",
    "video_urls": ["视频URL"],
    "enable_prediction": false
  }'
```

发布后用 `distribution/query` 查询审核状态（approved/pending_review/rejected）。

## 收益查询

```bash
# 余额
curl -m 60 -X POST "$X2C_API_BASE_URL" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $X2C_API_KEY" \
  -d '{"action": "wallet/balance"}'

# 流水
curl -m 60 -X POST "$X2C_API_BASE_URL" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $X2C_API_KEY" \
  -d '{"action": "wallet/transactions", "page": 1, "page_size": 10, "type": "earnings"}'
```

## 输出格式

### Task 看板
```
═══════════════════════════════════════════════════════════
 任务总数: {n}    总消耗: {n}积分 (${n})
═══════════════════════════════════════════════════════════

TASK-XXXXXXXX-XXX ｜ {title} {✅/🔄/❌}

Node 1 {✅/🔄/❌/⏳} 采集     {summary}
Node 2 {✅/🔄/❌/⏳} 筛选     {summary}
Node 3 {✅/🔄/❌/⏳} 制作     {summary}
Node 4 {✅/🔄/❌/⏳} 发布     {summary}
Node 5 {✅/🔄/❌/⏳} 审核     {summary}
```

### 收益面板
```
═══════════════════════════════════════════════════════════
 💰 账户收益
═══════════════════════════════════════════════════════════
积分余额:        {n}
X2C 钱包余额:    {n}
X2C 待领取:      {n}
USDC 余额:       {n}
```

## 成本参考

| 项目 | 积分 | 价格 |
|------|------|------|
| 剧本（短视频） | 10 | $0.10 |
| 视频 60秒 | 299 | $2.99 |
| 视频 120秒 | 599 | $5.99 |
| 视频 180秒 | 799 | $7.99 |
| 视频 300秒 | 999 | $9.99 |

## 已知限制

- 微博和快手的 DailyHot 接口偶尔返回 500（不影响整体采集）
- 视频渲染在 shot 阶段偶尔失败，属于 X2C 上游问题，重试通常成功
- 核心流程零模型依赖（不需要 OpenAI / Gemini / Claude API Key）
