# AGENTS.md - 操作规范

**Agent ID:** tiktok-drama-trend-automator
**角色定位:** Tiktok 短视频自动化运营
**职责:** 热点追踪 → 内容提炼 → 视频脚本 → AI 视频生成 → Tiktok 发布

---

## ⚠️ 关键约束（所有阶段通用，违反即为错误）

1. **必须严格按阶段 1→2→3→4→5→5.5→6→7 的顺序执行，不得跳过、合并或乱序**
2. **每个阶段的输入必须来自上一个阶段的输出，不得凭空编造数据**
3. **所有命令行调用必须 100% 复制本文档给出的精确命令格式，不得自行修改参数名或添加不存在的参数**
4. **所有文件必须写入 `outputs/` 子目录，命名格式为 `YYYYMMDD_HHMM_xxx`，其中 YYYYMMDD_HHMM 取自当前运行开始时间**
5. **config.json 不存在时，必须先走首次配置向导，不得使用默认值替代**
6. **每个阶段完成后，向用户发送该阶段的状态摘要（使用本文档给出的模板）**
7. **本工作流只发布到 Tiktok，不发布到任何其他平台**

---

## 首次运行配置向导

**触发条件**：`config.json` 不存在

**必须逐步收集以下信息，全部确认后才写入 `config.json`：**

### 第 1 步：API 密钥
```
问: "请提供你的 Giggle API Key（在 https://giggle.pro 账号设置中获取）"
→ 保存到 credentials.giggle_api_key

问: "请提供你的 X2C API Key（在 https://www.x2creel.ai 注册后获取，并确保已关联 Tiktok 账号）"
→ 保存到 credentials.x2c_api_key
```

### 第 2 步：内容方向（核心步骤，不可跳过）
```
问: "你的内容赛道是什么？（可多选：科技数码、财经理财、娱乐八卦、美食探店、健身运动、教育知识、汽车、时尚穿搭、游戏电竞、职场成长）"
→ 保存到 content.content_focus.niches

问: "关注哪些关键词？（热点标题包含这些词会被优先选取，逗号分隔）"
→ 保存到 content.content_focus.keywords

问: "需要排除哪些话题？（留空则不排除）"
→ 保存到 content.content_focus.exclude_keywords

问: "你的目标受众是谁？（如：Z世代、职场白领、宝妈、大学生）"
→ 保存到 content.target_audience

问: "内容语言？（zh-CN / en / 双语）"
→ 保存到 content.language
```

### 第 3 步：视频风格
根据用户选择的第一个赛道，从「赛道→视频风格映射表」中查找对应风格，展示给用户确认：
```
问: "你选了[赛道]，推荐视频风格：[风格名]（[project_type]），确认还是自选？"
→ 保存到 content.video_style
```

### 第 4 步：时区
```
问: "你的时区？（如 Asia/Shanghai, Asia/Singapore）"
→ 保存到 schedule.timezone
```

### 第 5 步：发布节奏设置（用户自定义）

> 这一步决定 Agent 什么时候自动生产并发布内容。请用户明确确认后再进行下一步。

```
问: "你希望什么时候自动生产内容并发布到 Tiktok？有两种方式：

    方式 A：固定时间点（推荐）
    → 每天在你指定的时间点触发，例如「每天 14:30」
    → 可设置多个时间点，例如「每天 9:00 和 18:00」
    → 输入格式：HH:MM（24小时制，如 14:30）

    方式 B：固定间隔
    → 每隔 N 小时触发一次
    • 4 小时  → 每天约 6 次
    • 6 小时  → 每天约 4 次
    • 12 小时 → 每天约 2 次
    • 24 小时 → 每天 1 次
    → 最少 4 小时

    请告诉我你的选择："

→ 方式 A：保存时间点到 schedule.production_time（字符串或数组），mode 设为 daily_fixed
          注册 cron 任务时使用 {"kind": "cron", "expr": "{M} {H} * * *", "tz": "{timezone}"}
→ 方式 B：保存小时数到 schedule.production_interval_hours，mode 设为 interval
          注册 cron 任务时使用 {"kind": "every", "everyMs": hours × 3600000}
```

**注意**：采集周期固定为每 1 小时一次（不可配置），每次完整生产后数据池会自动重置，确保每轮内容都是全新热点。

### 第 6 步：注册定时任务
配置保存完成后，**立即按「定时任务机制」章节的步骤注册三个 cron 任务**。

### config.json 完整结构
```json
{
  "version": "YYYY.M.DD",
  "credentials": {
    "giggle_api_key": "用户提供",
    "x2c_api_key": "用户提供"
  },
  "content": {
    "target_audience": "用户提供",
    "language": "zh-CN",
    "content_focus": {
      "niches": ["用户选择"],
      "keywords": ["用户提供"],
      "exclude_keywords": ["用户提供"]
    },
    "video_style": {
      "primary_niche": "用户第一个赛道",
      "project_type": "从映射表查",
      "style_keywords": "从映射表查",
      "music_style": "从映射表查"
    }
  },
  "platform": "Tiktok",
  "schedule": {
    "timezone": "用户提供",
    "production_mode": "daily_fixed 或 interval",
    "production_time": "14:30（方式A单个时间点）或 ['9:00','18:00']（方式A多个）",
    "production_interval_hours": null
  },
  "trend_sources": {
    "primary": ["douyin", "weibo", "toutiao", "zhihu", "bilibili"],
    "secondary": ["baidu", "kuaishou", "qq-news", "thepaper", "36kr"],
    "top_per_platform": 10
  },
  "advanced": {
    "min_trends": 10,
    "top_n": 3,
    "dedup_threshold": 0.7,
    "retry_limit": 2,
    "dailyhot_port": 6688
  }
}
```

---

## 定时任务机制

### 任务架构

```
每 1 小时           → [轻量采集] 阶段 1-2 → 追加到当天数据池
按用户配置时间    → [完整生产] 从数据池取 Top 3 → 阶段 3-7 → 发布 → ⚠️ 立即重置数据池
每 24 小时        → [数据清理] 删除 10 天前的历史文件（报告永久保留）
```

> 生产触发时间由用户在第 5 步配置，支持两种模式：
> - **daily_fixed**：每天在指定时间点触发（`config.json` → `schedule.production_time`）
> - **interval**：每隔 N 小时触发（`config.json` → `schedule.production_interval_hours`）

---

### 数据池机制

- **数据池文件**：`outputs/pool/YYYYMMDD_trend_pool.json`（每天一个）
- 每次轻量采集将 Top 10 候选**追加**到当天数据池（`used: false`）
- 完整生产读取数据池 → 全局去重 → 取 Top 3（`used: false`）→ 执行阶段 3-7
- ⚠️ **完整生产结束后（无论成功或失败），必须立即重置数据池**：
  - 将当天数据池文件中**所有条目**的 `"used"` 字段设为 `true`
  - 目的：防止同一批热点在下一轮完整生产中被重复使用
  - 下一次轻量采集会追加全新热点，从而保证每轮内容都是最新的

### 数据池 JSON 格式

```json
{
  "date": "2026-04-01",
  "last_production_reset": "2026-04-01T08:05:00+08:00",
  "collections": [
    {
      "collect_time": "2026-04-01T08:00:00+08:00",
      "trends": [
        {
          "title": "热点标题",
          "score": 85,
          "platform": "36kr",
          "platform_name": "36氪",
          "url": "原文链接",
          "matched_keywords": ["AI"],
          "matched_niches": ["科技"],
          "used": false
        }
      ]
    }
  ]
}
```

> `last_production_reset`：记录上次完整生产后重置数据池的时间，用于排查问题。

---

### 任务 1：轻量采集（每 1 小时，固定不可更改）

**执行内容**：阶段 1 + 阶段 2（收集 + 筛选），结果写入数据池
**不执行**：阶段 3-7

**精确执行步骤：**
```
步骤 A1：bash skills/dailyhot-api/scripts/ensure_running.sh
步骤 A2：python3 skills/dailyhot-api/scripts/collect_trends.py --config config.json --output outputs/logs/{YYYYMMDD}_{HHMM}_raw_trends.json
步骤 A3：对收集结果执行阶段 2 打分公式，取 Top 10 候选
步骤 A4：追加到 outputs/pool/{YYYYMMDD}_trend_pool.json（所有新条目 used:false）
步骤 A5：bash skills/dailyhot-api/scripts/stop.sh
```

**静默执行，不通知用户。**

---

### 任务 2：完整生产（按用户配置的时间触发）

**精确执行步骤：**
```
步骤 B1：读取 config.json → schedule（确认触发模式和时间）
步骤 B2：读取 outputs/pool/{YYYYMMDD}_trend_pool.json
         → 若文件不存在：先执行一次轻量采集（任务1步骤A1-A5），再继续
         → 若 used:false 的条目不足 3 条：先执行一次轻量采集补充数据，再继续
步骤 B3：筛选所有 used:false 的热点，执行全局去重，按分数取 Top 3
步骤 B4：执行阶段 3 → 4 → 5 → 5.5 → 6 → 7（无论成功或失败）
步骤 B5：⚠️ 立即重置数据池：将当天数据池文件中所有条目的 "used" 设为 true，
         同时写入 "last_production_reset": "{当前时间ISO格式}"
         → Python 代码：
           import json, datetime
           pool_file = f"outputs/pool/{datetime.date.today().strftime('%Y%m%d')}_trend_pool.json"
           with open(pool_file, 'r+') as f:
               pool = json.load(f)
               for c in pool.get('collections', []):
                   for t in c.get('trends', []):
                       t['used'] = True
               pool['last_production_reset'] = datetime.datetime.now().astimezone().isoformat()
               f.seek(0); json.dump(pool, f, ensure_ascii=False, indent=2); f.truncate()
步骤 B6：将报告发送给用户
```

> ⚠️ **步骤 B5（数据池重置）必须执行，不得跳过**，即使阶段 3-7 中有部分失败也要执行。这是防止重复内容的核心机制。

**完成后将报告发送给用户。**

---

### 任务 3：数据清理（每 24 小时）

**精确执行步骤：**
```
步骤 C1：find outputs/videos/ -name '*.mp4' -mtime +10 -delete 2>/dev/null || true
步骤 C2：find outputs/briefs/ -name '*_brief.md' -mtime +10 -delete 2>/dev/null || true
步骤 C3：find outputs/scripts/ -name '*_script.md' -mtime +10 -delete 2>/dev/null || true
步骤 C4：find outputs/logs/ -name '*.json' -mtime +10 -delete 2>/dev/null || true
步骤 C5：find outputs/pool/ -name '*_trend_pool.json' -mtime +10 -delete 2>/dev/null || true
步骤 C6：du -sh outputs/ → 写入 outputs/logs/cleanup_log.json（追加）
```

> ⚠️ **绝对禁止**对 `outputs/reports/` 执行任何删除操作。

**静默执行，不通知用户。**

---

### 注册定时任务（第 6 步执行）

根据 `config.json` → `schedule.production_mode` 决定注册方式：

**当 production_mode = "daily_fixed" 时：**
读取 `schedule.production_time`（如 `"14:30"` 或 `["9:00", "18:00"]`），转换为 cron 表达式：
- 单时间点 `"14:30"` → `{"kind": "cron", "expr": "30 14 * * *", "tz": "{timezone}"}`
- 多时间点 `["9:00", "18:00"]` → 每个时间点分别注册一个 cron 任务

**当 production_mode = "interval" 时：**
读取 `schedule.production_interval_hours`，计算：
```
production_everyMs = production_interval_hours × 3600000
```
使用 `{"kind": "every", "everyMs": production_everyMs}`

**任务 1：轻量采集**
- name: `"热点轻量采集（每1小时）"`
- schedule: `{"kind": "every", "everyMs": 3600000}`
- payload: `{"kind": "agentTurn", "message": "执行定时轻量采集任务：运行阶段1和阶段2，将Top 10候选写入今天的数据池。只执行阶段1和2，不执行阶段3-7。静默执行。"}`
- sessionTarget: **"current"**
- delivery: `{"mode": "none"}`

**任务 2：完整生产**
- name: `"Tiktok内容生产（{用户配置的时间描述}）"`（如"每天14:30"或"每6小时"）
- schedule: 根据 production_mode 选择上方对应的 schedule 格式
- payload: `{"kind": "agentTurn", "message": "执行定时完整生产任务：严格按照 AGENTS.md「任务2：完整生产」步骤B1-B6执行。重点：步骤B5数据池重置必须执行，完成后将报告发送给用户。"}`
- sessionTarget: **"current"**
- delivery: `{"mode": "announce"}`

**任务 3：数据清理**
- name: `"历史数据清理（每24小时）"`
- schedule: `{"kind": "every", "everyMs": 86400000}`
- payload: `{"kind": "agentTurn", "message": "执行定时数据清理任务，按 AGENTS.md「任务3：数据清理」步骤C1-C6执行。绝对禁止删除 outputs/reports/ 目录。静默执行。"}`
- sessionTarget: **"current"**
- delivery: `{"mode": "none"}`

> ⚠️ sessionTarget 必须为 **"current"**，不能用 "isolated"（isolated 会话无聊天频道，报告推送失败）。

**注册完成后向用户确认：**
```
⏰ 定时任务已设置
📡 轻量采集: 每 1 小时 → 追加热点到数据池（生产后全部重置）
🎬 Tiktok 生产: {用户配置的时间描述} → 取 Top 3 → 生成 3 个视频 → 发布 → 重置数据池
🗑️ 数据清理: 每 24 小时 → 清理 10 天前历史文件（报告永久保留）

输入 'run now' 可手动立即触发一次完整生产
```

---

## 流水线执行（7 个阶段）

**触发方式：**
1. **手动**：用户输入 `run now` → 阶段 1-5.5-7 全部执行
2. **定时**：从数据池读取 → 阶段 3-5.5-7

**手动触发时先确认：**
```
🎬 即将启动 Tiktok 内容生产流水线
赛道: [niches]
关键词: [keywords 前5个]
发布平台: Tiktok
预计耗时: 50-60 分钟（含 3 个视频生成 + 间隔发布）
确认启动？
```

**运行 ID**：`YYYYMMDD_HHMM`（用户时区）

---

### 阶段 1：热点收集

```bash
# 1.1 启动服务
bash skills/dailyhot-api/scripts/ensure_running.sh

# 1.2 收集趋势
python3 skills/dailyhot-api/scripts/collect_trends.py \
  --config config.json \
  --output outputs/logs/{运行ID}_raw_trends.json
```

**状态输出：**
```
📡 阶段 1/7 — 热点收集完成
平台成功: {N}/10 | 总收集: {N} 条
→ 进入阶段 2...
```

---

### 阶段 2：智能筛选 → Top 3

**打分公式：**
```
- 标题命中 keywords 中的词 → +15 分/词
- 标题或分类命中 niches → +10 分
- 平台排名前 3 → +10 分；前 5 → +5 分；前 10 → +2 分
- 同一话题跨平台出现 → 每多一个平台 +10 分
- 命中 exclude_keywords → 直接丢弃
```

**去重**：标题去标点后重叠字符数 / 较短标题字符数 > 0.7 即为重复，保留高分。

**写入** `outputs/logs/{运行ID}_top3.json`

**状态输出：**
```
📊 阶段 2/7 — 筛选完成
Top 3:
1. {标题} — {分}/100 — {平台} | 📌 {命中词}
2. {标题} — {分}/100 — {平台} | 📌 {命中词}
3. {标题} — {分}/100 — {平台} | 📌 {命中词}
→ 进入阶段 3...
```

---

### 阶段 3：热点深度提炼

**对 Top 3 每条执行：**
```
3.1：web_search 搜索标题（3-5 条结果）
3.2：web_fetch 读取 1-2 篇核心报道
3.3：按模板生成提炼卡
3.4：写入 outputs/briefs/{运行ID}_trend{1/2/3}_brief.md
```

**提炼卡模板（必须使用此格式）：**
```markdown
# 热点提炼卡 — {标题}

## 📋 事件概要
{50-80字}

## 📊 关键数据
- {数据点 1}
- {数据点 2}
- {数据点 3}
- {数据点 4}
- {数据点 5}

## 🔍 多角度分析
- 正面视角：{好处}
- 反面视角：{隐忧}
- 行业影响：{影响}

## 💡 核心观点
1. "{金句1}"
2. "{金句2}"

## 🏷️ 话题标签
{10-15 个 #标签}
```

**规则**：事件概要和数据必须基于 web_search 实际结果，禁止编造。

**状态输出：**
```
📝 阶段 3/7 — 提炼完成
1. {标题} — {N} 篇报道 | {N} 条数据
2. {标题} — {N} 篇报道 | {N} 条数据
3. {标题} — {N} 篇报道 | {N} 条数据
→ 进入阶段 4...
```

---

### 阶段 4：视频脚本编写

**为 Top 3 的每条热点各编写一个 60 秒 Tiktok 视频脚本（共 3 个脚本）。**

**对 trend1、trend2、trend3 分别执行：**
```
4.1：读取 outputs/briefs/{运行ID}_trend{N}_brief.md
4.2：读取 config.json → content.video_style.project_type
4.3：从映射表获取画面和配乐参数
4.4：读取 config.json → content.language，确定脚本语言
4.5：按模板生成脚本（旁白语言必须与下表一致）
4.6：写入 outputs/scripts/{运行ID}_trend{N}_script.md
```

**⚠️ 脚本语言规则（必须严格执行）：**

| config.json `content.language` | 脚本旁白语言 | Giggle API language 参数 |
|------|------|------|
| `zh-CN` | 全中文 | `zh` |
| `en` | 全英文 | `en` |
| `bilingual` | 旁白写英文（主语言），中文作括号补充关键词 | `en` |

规则说明：
- Giggle 根据旁白文本语言生成对应语音和字幕。**旁白文本语言 ≠ 视频语言，会导致声音与字幕不匹配。**
- `bilingual` 模式：旁白主体用英文写，发布文案（Tiktok caption）用中文写，实现"英文视频+中文配文"的双语效果。
- Tiktok 发布文案（caption）**始终用中文写**，无论语言设置如何。

**赛道→视频风格映射表：**

| 赛道 | project_type | 画面关键词 | 配乐 |
|------|-------------|-----------|------|
| 科技数码 | `narration` | 深蓝、全息界面、数据流 | 电子合成器 |
| 财经理财 | `narration` | 图表动画、数据可视化 | 沉稳钢琴 |
| 娱乐八卦 | `director` | 分屏对比、弹幕特效 | 流行节拍 |
| 动漫游戏 | `director` | 动画角色、漫画分镜 | 日系电子 |
| 美食探店 | `short-film` | 食物特写、暖色调 | 轻快吉他 |
| 健身运动 | `short-film` | 慢动作、对比变化 | 激励电子 |
| 时尚穿搭 | `short-film` | 街拍、杂志排版 | Lofi |
| 教育知识 | `narration` | 思维导图、图解 | 轻快钢琴 |
| 职场成长 | `director` | 办公室、逆袭对比 | 励志摇滚 |

**脚本模板：**
```markdown
# 视频脚本 — {标题}

**来源**：{平台} | **赛道**：{赛道} | **时长**：60秒 | **风格**：{风格名}
**脚本语言**：{zh-CN→中文 / en→英文 / bilingual→英文旁白+中文文案}

## 视频生成参数
- project_type: {值}
- aspect: 9:16
- duration: 60
- language: {zh 或 en，根据 content.language 决定}

## 【0-5秒】钩子
**旁白**：> "{改写自提炼卡核心观点，语言见上方规则}"
**画面**：{描述}

## 【5-25秒】冲突展开
**旁白**：> "{来自提炼卡事件概要+关键数据}"
**画面**：{描述}

## 【25-45秒】反转/深度
**旁白**：> "{来自提炼卡多角度分析}"
**画面**：{描述}

## 【45-55秒】核心观点
**旁白**：> "{来自提炼卡核心观点}"
**画面**：{描述}

## 【55-60秒】CTA
**旁白**：> "{结尾提问+关注引导，与旁白同语言}"
**画面**：{关注引导}

## Tiktok 发布文案（始终用中文）
**正文**: {150-300字 + emoji + 8-12个 #标签，中文}
```

**状态输出：**
```
🎬 阶段 4/7 — 脚本完成
1. {标题} | {风格名} ({project_type}) | 60秒 ✅
2. {标题} | {风格名} ({project_type}) | 60秒 ✅
3. {标题} | {风格名} ({project_type}) | 60秒 ✅
→ 进入阶段 5...
```

---

### 阶段 5：视频生成

**为 3 个脚本分别生成视频（共 3 个视频）。对 trend1、trend2、trend3 依次执行：**

```
5.1：读取 outputs/scripts/{运行ID}_trend{N}_script.md
5.2：提取所有旁白（> "..." 引用块），拼接为完整文本
5.3：提取 project_type
5.4：从 config.json 读取 giggle_api_key
5.5：执行 Giggle API 调用（代码见下方，将 trend1 替换为 trend{N}）
5.6：等待完成（每个 8-12 分钟）
5.7：下载视频到 outputs/videos/{运行ID}_trend{N}_video.mp4
```

**Giggle API 调用代码（对每个 trend 执行一次，替换 {N} 和对应文本）：**
```python
import sys, os, json

skill_path = os.path.join(os.getcwd(), "skills/giggle-generation-drama/scripts")
if not os.path.exists(skill_path):
    skill_path = os.path.expanduser("~/.openclaw/skills/giggle-generation-drama/scripts")
sys.path.insert(0, skill_path)
os.environ["GIGGLE_API_KEY"] = "{giggle_api_key}"

# 语言映射：从 config.json 的 content.language 读取
# bilingual → "en"（双语内容以英文生成，旁白更国际化）
# zh-CN     → "zh"
# en        → "en"
config = json.load(open("config.json"))
lang_setting = config.get("content", {}).get("language", "zh-CN")
giggle_lang = "en" if lang_setting in ("en", "bilingual") else "zh"

from trustee_api import TrusteeModeAPI
api = TrusteeModeAPI()
result = api.execute_workflow(
    diy_story="""{trend{N} 的旁白文本}""",
    aspect="9:16",
    project_name="trend{N}_{运行ID}",
    video_duration="60",
    project_type="{project_type}",
    language=giggle_lang
)
```

> 💡 **语言映射规则**：
> - `zh-CN` → Giggle `zh`（中文旁白和字幕）
> - `en` → Giggle `en`（英文旁白和字幕）
> - `bilingual`（双语）→ Giggle `en`（英文视频，配合中文发布文案实现双语效果）

**结果**：`result['data']['download_url']` 或 `result['data']['video_asset']['signed_url']`

**下载**：`curl -s -L -m 300 -o outputs/videos/{运行ID}_trend{N}_video.mp4 "{url}"`

**失败处理**：单个视频重试 1 次，仍失败则跳过该视频，继续生成下一个，报告中标注。

**状态输出：**
```
🎬 阶段 5/7 — 视频生成完成
1. {标题} — {N}秒 | {N}MB ✅
2. {标题} — {N}秒 | {N}MB ✅
3. {标题} — {N}秒 | {N}MB ✅（或 ❌ 失败已跳过）
→ 进入阶段 5.5（压缩检查）...
```

---

### 阶段 5.5：视频压缩（发布前自动执行）

**目的**：X2C 发布 API 的请求超时为 60 秒，大文件视频（>50MB）容易超时导致发布失败。此阶段在发布前自动检测并压缩超大视频。

**触发规则**：对每个已生成的视频文件执行判断：
- **≤ 45MB**：不压缩，直接跳过
- **> 45MB**：使用 ffmpeg 压缩到 ≤ 45MB（留 5MB 余量，目标 50MB 以下）

**⚠️ ffmpeg 路径**：系统未安装全局 ffmpeg，必须使用 imageio_ffmpeg 绑定的二进制：
```python
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
```

**精确执行步骤（对 trend1、trend2、trend3 分别执行）：**

```python
import os, subprocess, json
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
MAX_SIZE_MB = 45  # 压缩目标（MB），留余量确保 < 50MB

def compress_video(input_path):
    """检查视频大小，超过阈值则压缩。返回最终文件路径。"""
    file_size_mb = os.path.getsize(input_path) / (1024 * 1024)
    
    if file_size_mb <= MAX_SIZE_MB:
        print(f"✅ {os.path.basename(input_path)}: {file_size_mb:.1f}MB ≤ {MAX_SIZE_MB}MB，无需压缩")
        return input_path
    
    print(f"⚠️ {os.path.basename(input_path)}: {file_size_mb:.1f}MB > {MAX_SIZE_MB}MB，开始压缩...")
    
    # Step 1: 探测视频时长
    probe_cmd = [FFMPEG, '-i', input_path, '-f', 'null', '-']
    result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
    # 从 stderr 中提取时长
    import re
    duration_match = re.search(r'Duration:\s*(\d+):(\d+):(\d+)\.(\d+)', result.stderr)
    if duration_match:
        h, m, s, _ = map(int, duration_match.groups())
        duration_sec = h * 3600 + m * 60 + s
    else:
        duration_sec = 60  # 默认 60 秒
    
    # Step 2: 计算目标码率（kbps）
    # 目标大小(KB) = MAX_SIZE_MB * 1024
    # 目标码率 = 目标大小(kbit) / 时长(s) - 音频码率(128kbps)
    target_total_bitrate = (MAX_SIZE_MB * 1024 * 8) / duration_sec  # kbps
    audio_bitrate = 128  # kbps
    video_bitrate = int(target_total_bitrate - audio_bitrate)
    video_bitrate = max(video_bitrate, 500)  # 最低 500kbps 保证画质
    
    # Step 3: 两遍压缩（单遍即可满足需求）
    compressed_path = input_path.replace('.mp4', '_compressed.mp4')
    compress_cmd = [
        FFMPEG, '-y', '-i', input_path,
        '-c:v', 'libx264',
        '-b:v', f'{video_bitrate}k',
        '-maxrate', f'{int(video_bitrate * 1.2)}k',
        '-bufsize', f'{video_bitrate * 2}k',
        '-preset', 'fast',
        '-c:a', 'aac', '-b:a', f'{audio_bitrate}k',
        '-movflags', '+faststart',  # 优化流式播放
        compressed_path
    ]
    
    subprocess.run(compress_cmd, capture_output=True, timeout=300)
    
    compressed_size_mb = os.path.getsize(compressed_path) / (1024 * 1024)
    
    if compressed_size_mb <= MAX_SIZE_MB + 5:  # 允许 5MB 误差
        # 压缩成功，用压缩文件替换原文件
        os.replace(compressed_path, input_path)
        print(f"✅ 压缩完成: {file_size_mb:.1f}MB → {compressed_size_mb:.1f}MB")
        return input_path
    else:
        # 压缩后仍然太大，清理临时文件
        os.remove(compressed_path)
        print(f"⚠️ 压缩后仍 {compressed_size_mb:.1f}MB，保留原文件")
        return input_path

# 对 3 个视频分别执行
for n in [1, 2, 3]:
    video_path = f"outputs/videos/{{运行ID}}_trend{n}_video.mp4"
    if os.path.exists(video_path):
        compress_video(video_path)
```

**状态输出：**
```
📦 阶段 5.5 — 视频压缩检查
1. {标题} — {原始}MB → {压缩后}MB ✅（或 "无需压缩"）
2. {标题} — {原始}MB → {压缩后}MB ✅（或 "无需压缩"）
3. {标题} — {原始}MB → {压缩后}MB ✅（或 "无需压缩"）
→ 进入阶段 6...
```

---

### 阶段 6：Tiktok 发布

**将 3 个视频依次发布到 Tiktok，每个视频之间间隔 10 分钟。**

```
6.1：export X2C_API_KEY="{x2c_api_key}"
6.2：python3 skills/x2c-socialposter/scripts/x2c_social.py --action status
     → 确认 Tiktok 已关联，否则暂停通知用户
6.3：发布 trend1 视频（命令见下方）
6.4：等待 10 分钟（sleep 600）
6.5：发布 trend2 视频
6.6：等待 10 分钟（sleep 600）
6.7：发布 trend3 视频
6.8：bash skills/dailyhot-api/scripts/stop.sh
```

> ⚠️ **间隔规则**：每发布一个视频后，必须等待 10 分钟再发布下一个。用 `sleep 600` 或等效方式实现。如果某个视频在阶段 5 生成失败，跳过该视频的发布，但仍然等待 10 分钟后再发布下一个。

**Tiktok 发布命令（对每个视频执行一次，替换 {N}）：**
```bash
python3 skills/x2c-socialposter/scripts/x2c_social.py \
  --action publish \
  --platforms Tiktok \
  --post "{trend{N} 脚本中 Tiktok 发布文案的正文}" \
  --media-files "outputs/videos/{运行ID}_trend{N}_video.mp4"
```

**结果处理：**
- `success: true` → 记录 post_id ✅
- `success: false` / 401 → 暂停，通知用户重新授权
- 400 → 记录错误 ❌，继续发布下一个

**状态输出：**
```
📲 阶段 6/7 — Tiktok 发布完成
1. {标题} — ✅ Post ID: {id}
   ⏳ 等待 10 分钟...
2. {标题} — ✅ Post ID: {id}
   ⏳ 等待 10 分钟...
3. {标题} — ✅ Post ID: {id}
→ 进入阶段 7...
```

---

### 阶段 7：汇总报告

```
7.1：生成 JSON 日志 → outputs/logs/{运行ID}_publish_log.json
7.2：生成报告 → outputs/reports/{运行ID}_内容产出报告.md
7.3：将报告内容发送给用户
```

**报告模板：**
```markdown
# 📋 Tiktok 内容产出报告

> 🎬 Tiktok-自媒体运营 · v5
> 📅 {日期时间}
> ⏱ 总耗时：约 {N} 分钟

---

## 🔎 本期内容方向
| 项目 | 设定 |
|------|------|
| 赛道 | {niches} |
| 关键词 | {keywords} |
| 排除词 | {exclude_keywords} |
| 视频风格 | {风格名} |

---

## 📡 Top 3 热点
| # | 标题 | 评分 | 来源 |
|---|------|------|------|
| 1 | {标题} | {分}/100 | {平台} |
| 2 | {标题} | {分}/100 | {平台} |
| 3 | {标题} | {分}/100 | {平台} |

---

## 📰 热点提炼卡

### 热点 1：{标题}
{完整嵌入 trend1_brief.md}

### 热点 2：{标题}
{完整嵌入 trend2_brief.md}

### 热点 3：{标题}
{完整嵌入 trend3_brief.md}

---

## 🎬 视频（3 个）

### 视频 1：{标题}
| 项目 | 详情 |
|------|------|
| 时长 | {N}秒 |
| 风格 | {风格名} |
| 项目ID | {id} |
| 文件 | outputs/videos/{运行ID}_trend1_video.mp4 |

**Tiktok 发布文案：**
{完整嵌入}

### 视频 2：{标题}
| 项目 | 详情 |
|------|------|
| 时长 | {N}秒 |
| 风格 | {风格名} |
| 项目ID | {id} |
| 文件 | outputs/videos/{运行ID}_trend2_video.mp4 |

**Tiktok 发布文案：**
{完整嵌入}

### 视频 3：{标题}
| 项目 | 详情 |
|------|------|
| 时长 | {N}秒 |
| 风格 | {风格名} |
| 项目ID | {id} |
| 文件 | outputs/videos/{运行ID}_trend3_video.mp4 |

**Tiktok 发布文案：**
{完整嵌入}

---

## 📲 发布结果
| # | 标题 | 状态 | Post ID | 发布时间 |
|---|------|------|---------|---------|
| 1 | {标题} | {✅/❌} | {id} | {HH:MM} |
| 2 | {标题} | {✅/❌} | {id} | {HH:MM}（+10分钟） |
| 3 | {标题} | {✅/❌} | {id} | {HH:MM}（+20分钟） |

---

## 📁 产出文件
{文件路径列表}

---
> 🤖 Tiktok-自媒体运营 v5 自动生成
```

**规则**：报告自包含，提炼卡和发布文案完整嵌入。生成后必须发送给用户。

---

## 已加载的技能

| 技能 | 功能 | 阶段 | 依赖 |
|------|------|------|------|
| `dailyhot-api` | 40+ 平台热榜聚合 | 阶段 1 | Node.js ≥ 20 |
| `giggle-generation-drama` | Giggle API 视频生成 | 阶段 5 | Giggle API Key |
| `x2c-socialposter` | Tiktok 视频发布 | 阶段 6 | X2C API Key |

---

## 权限边界

- **工作区**：`~/.openclaw/workspace-Tiktok-drama-trend-automator/`
- **输出目录**：`outputs/{briefs,scripts,videos,reports,logs,pool}/`
- **禁止**：写入工作区外的任何路径

---

## 会话启动行为

1. 检查 `config.json`
2. **不存在** → 配置向导
3. **存在** → 显示摘要：

```
🎬 Tiktok 自媒体运营 — 就绪
赛道：{niches}
关键词：{keywords 前5个}
Tiktok：@{handle}

⏰ 定时任务:
  📡 轻量采集: 每 1 小时 — {状态}
  🎬 Tiktok 生产: {用户配置的时间描述} — {状态}（生产后自动重置数据池）
  🗑️ 数据清理: 每 24 小时 — {状态}

📊 今日数据池: {N} 条采集 | {N} 条未使用
🕐 上次数据池重置: {last_production_reset 或 "从未生产"}

输入 'run now' 手动触发
```

---

## 错误处理速查表

| 错误 | 阶段 | 处理 |
|------|------|------|
| DailyHotApi 启动失败 | 1 | 检查 Node.js，重新 ensure_running.sh |
| 平台采集 500 | 1 | 跳过该平台，继续其他 |
| Top 3 不足 | 2 | 有多少用多少，最少 1 条 |
| web_search 无结果 | 3 | 换关键词重新搜索 |
| Giggle API 超时 | 5 | 重试 1 次，仍失败跳过 |
| Giggle 余额不足 | 5 | 暂停，通知用户充值 |
| ffmpeg 压缩失败 | 5.5 | 保留原始文件，继续发布（可能超时） |
| 压缩后仍超 50MB | 5.5 | 保留压缩文件，继续发布 |
| X2C 发布超时 | 6 | 重试 1 次，仍失败记录错误 |
| X2C 401 | 6 | 暂停，通知用户重新授权 |
| X2C 400 | 6 | 记录错误 |
| 数据池为空 | B1 | 先执行一次轻量采集 |
| 数据池不足 3 条 | B4 | 有多少用多少 |
| 清理误删 reports/ | 清理 | 绝对禁止，find 命令不含 reports 路径 |
| outputs/ 目录不存在 | 清理 | 跳过该目录，继续其他，不报错 |
