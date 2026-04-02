# BOOTSTRAP.md - 首次启动自动引导

## 触发条件

每次新会话启动时，Agent 执行以下检查：

### Step 1: 检查依赖 Skills

```bash
# 必须存在以下 3 个 skill 目录
ls ~/.openclaw/skills/dailyhot-api/SKILL.md
ls ~/.openclaw/skills/storyclaw-x2c-ai-director/SKILL.md
ls ~/.openclaw/skills/storyclaw-x2c-publish/SKILL.md
```

如果任何一个缺失，输出：

> ⚠️ 缺少必要的 Skill，请先安装：
>
> ```
> openclaw skill install dailyhot-api
> openclaw skill install storyclaw-x2c-ai-director
> openclaw skill install storyclaw-x2c-publish
> ```
>
> 安装完成后重新开始对话。

### Step 2: 检查 X2C 账号绑定

检查 config.json 中 `x2c.api_key` 是否为空。

如果未绑定，引导用户：

> 🔑 首次使用需要绑定 X2C 账号：
>
> 1. 打开 https://www.x2creel.ai 注册/登录
> 2. 进入 个人中心 → API管理 → 复制 API Key
> 3. 把 API Key 发给我
>
> 格式：`x2c_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

收到 Key 后执行验证：
```bash
cd ~/.openclaw/skills/storyclaw-x2c-ai-director
node scripts/ad-account-manager.js verify-key <api_key>
```

验证通过 → 写入 config.json 和 credentials 文件 → 继续 Step 3。

### Step 3: 检查内容配置

检查 config.json 中 `content.niches` 是否为空数组。

如果未配置，询问用户：

> 📝 设置你的内容方向：
>
> **赛道**（可多选）：时尚穿搭 / 娱乐八卦 / 科技数码 / 财经金融 / 游戏电竞
> **关键词**：用于筛选热点，例如「美女, 穿搭, 网红, 明星」
> **目标受众**：例如「大学生」「白领」「宝妈」
>
> 直接告诉我你的选择即可。

### Step 4: 检查视频参数

如果 config.json 中 `video_production.defaults` 各项都有值，跳过。

否则引导用户选择：

> 🎬 设置视频默认参数：
>
> ⏱️ 时长: 60秒($2.99) / 120秒($5.99) / 180秒($7.99) / 300秒($9.99)
> 📐 比例: 竖屏(9:16) / 横屏(16:9)
> 🎨 风格: 3D古风 / 2D漫剧 / 吉卜力 / 皮克斯 / 写实 / 二次元 / 国风水墨
> 📂 分类: 玄幻异能 / 悬疑惊悚 / 科幻末世 / 都市复仇 / 热门综合 / 霸总甜宠 / 仙侠古装

### Step 5: 启动 DailyHot 服务

```bash
cd ~/.openclaw/skills/dailyhot-api && bash scripts/ensure_running.sh
```

### Step 6: 就绪

所有检查通过后，显示能力菜单（见 AGENTS.md Session Startup Behavior）。

---

## 配置模板

首次安装时，如果 config.json 不存在，使用以下模板创建：

```json
{
  "version": "1.0.0",
  "agent_id": "news-to-video-monetizer",
  "content": {
    "niches": [],
    "keywords": [],
    "exclude_keywords": [],
    "target_audience": "",
    "language": "zh-CN"
  },
  "video_production": {
    "defaults": {
      "mode": "short_video",
      "duration": 60,
      "ratio": "9:16",
      "style": "",
      "category": ""
    }
  },
  "pipeline": {
    "default_topics_count": 3,
    "dedup_ttl_days": 15,
    "auto_publish": true
  },
  "task_system": {
    "id_format": "TASK-{YYYYMMDD}-{SEQ:3}",
    "storage_dir": "tasks/",
    "lifecycle_nodes": ["collection", "filtering", "production", "publishing", "audit"],
    "retention": {
      "completed_ttl_days": 30,
      "failed_ttl_days": 7,
      "archive_before_delete": true,
      "archive_dir": "tasks/archive/"
    },
    "local_video_storage": false
  },
  "revenue": {
    "apis": {
      "balance": "wallet/balance",
      "transactions": "wallet/transactions"
    }
  },
  "sources": {
    "platforms": ["douyin", "weibo", "toutiao", "zhihu", "bilibili", "baidu", "kuaishou"],
    "min_virality_score": 50
  },
  "x2c": {
    "api_key": "",
    "email": "",
    "user_id": ""
  }
}
```
