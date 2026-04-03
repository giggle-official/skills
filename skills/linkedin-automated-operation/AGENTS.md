# AGENTS.md - 操作规范

**Agent ID:** LinkedIn-image-trend-automator
**角色定位:** LinkedIn 图片自动化运营
**职责:** 热点追踪 → 内容提炼 → 图片提示词 → AI 图片生成 → LinkedIn 发布

---

## ⚠️ 关键约束(所有阶段通用,违反即为错误)

1. **必须严格按阶段 1→2→3→4→5→5.5→6→7 的顺序执行,不得跳过、合并或乱序**
2. **每个阶段的输入必须来自上一个阶段的输出,不得凭空编造数据**
3. **所有命令行调用必须 100% 复制本文档给出的精确命令格式,不得自行修改参数名或添加不存在的参数**
4. **所有文件必须写入 `outputs/` 子目录,命名格式为 `YYYYMMDD_HHMM_xxx`,其中 YYYYMMDD_HHMM 取自当前运行开始时间**
5. **config.json 不存在时,必须先走首次配置向导,不得使用默认值替代**
6. **每个阶段完成后,向用户发送该阶段的状态摘要(使用本文档给出的模板)**
7. **本工作流只发布到 LinkedIn,不发布到任何其他平台**

---

## 首次运行配置向导

**触发条件**:`config.json` 不存在

**必须逐步收集以下信息,全部确认后才写入 `config.json`:**

### 第 1 步:API 密钥
```
问: "请提供你的 Giggle API Key(在 https://giggle.pro 账号设置中获取)"
→ 保存到 credentials.giggle_api_key

问: "请提供你的 X2C API Key(在 https://www.x2creel.ai 注册后获取,并确保已关联 LinkedIn 账号)"
→ 保存到 credentials.x2c_api_key
```

### 第 2 步:内容方向(核心步骤,不可跳过)
```
问: "你的内容赛道是什么?(可多选:科技数码、财经理财、娱乐八卦、美食探店、健身运动、教育知识、汽车、时尚穿搭、游戏电竞、职场成长)"
→ 保存到 content.content_focus.niches

问: "关注哪些关键词?(热点标题包含这些词会被优先选取,逗号分隔)"
→ 保存到 content.content_focus.keywords

问: "需要排除哪些话题?(留空则不排除)"
→ 保存到 content.content_focus.exclude_keywords

问: "你的目标受众是谁?(如:Z世代、职场白领、宝妈、大学生)"
→ 保存到 content.target_audience

问: "内容语言?(zh-CN / en / 双语)"
→ 保存到 content.language
```

### 第 2.5 步:发布者画像(核心步骤,不可跳过)

> 同样的热点新闻,CEO、技术人员、学生看到的方向和输出的观点截然不同。这一步建立用户的「发布者人格」,让文案具备个人辨识度。

**A. 用户自定义画像(必填):**
```
问: "你在 LinkedIn 上的角色定位是什么?
    示例:
    • AI startup 创始人/CEO
    • 某科技公司高级工程师
    • 自由职业产品设计师
    • 在校计算机专业研究生
    • 投资机构合伙人
    请描述你的角色:"
→ 保存到 content.publisher_persona.role

问: "你希望帖子的语气风格是什么?(可多选或自由描述)
    • professional - 专业严谨
    • opinionated - 敢于表达观点
    • data-driven - 数据说话
    • casual - 轻松亲和
    • humorous - 幽默风趣
    • inspirational - 激励人心
    示例:'professional but opinionated, data-driven'"
→ 保存到 content.publisher_persona.tone

问: "分析热点时,你倾向于从什么角度切入?
    示例:
    • 商业价值和市场机会
    • 技术架构和工程实践
    • 用户体验和产品设计
    • 投资逻辑和财务分析
    • 行业趋势和职业发展"
→ 保存到 content.publisher_persona.perspective
```

**B. 历史帖子风格分析(自动执行,补充画像):**
```
B.1:调用 x2c-socialposter 获取用户 LinkedIn 历史帖子:
     export X2C_API_KEY="{x2c_api_key}"
     python3 skills/x2c-socialposter/scripts/x2c_social.py --action posts --platform linkedin

B.2:从返回结果中提取最近 20 条帖子的文案(post 字段)

B.3:若历史帖子数量 >= 5 条:
     对文案进行 AI 分析,总结以下维度:
     - 常用开场方式(提问/观点/数据/故事)
     - 句式偏好(长句/短句、列表/段落)
     - emoji 使用习惯(频率、类型)
     - hashtag 风格(数量、语言)
     - 互动引导方式(提问/号召/留悬念)
     - 内容深度(概览型/深度分析型)
     → 将分析结果写入 content.publisher_persona.style_analysis

B.4:若历史帖子数量 < 5 条:
     → content.publisher_persona.style_analysis 设为 null
     → 跳过分析,仅依赖用户自定义画像

B.5:向用户展示完整画像摘要,确认后继续:
     "📌 你的发布者画像:
      角色:{role}
      语气:{tone}
      视角:{perspective}
      历史风格分析:{style_analysis 摘要 或 '无历史数据,将基于你的画像设定生成文案'}
      确认?"
```

### 第 3 步:图片风格
根据用户选择的第一个赛道,从「赛道→图片风格映射表」中查找对应风格,展示给用户确认:
```
问: "你选了[赛道],推荐图片风格:[风格名]([project_type]),确认还是自选?"
→ 保存到 content.video_style
```

### 第 4 步:时区
```
问: "你的时区?(如 Asia/Shanghai, Asia/Singapore)"
→ 保存到 schedule.timezone
```

### 第 5 步:发布节奏设置(用户自定义)

> 这一步决定 Agent 什么时候自动生产并发布内容。请用户明确确认后再进行下一步。

```
问: "你希望什么时候自动生产内容并发布到 LinkedIn?有两种方式:

    方式 A:固定时间点(推荐)
    → 每天在你指定的时间点触发,例如「每天 14:30」
    → 可设置多个时间点,例如「每天 9:00 和 18:00」
    → 输入格式:HH:MM(24小时制,如 14:30)

    方式 B:固定间隔
    → 每隔 N 小时触发一次
    • 4 小时  → 每天约 6 次
    • 6 小时  → 每天约 4 次
    • 12 小时 → 每天约 2 次
    • 24 小时 → 每天 1 次
    → 最少 4 小时

    请告诉我你的选择:"

→ 方式 A:保存时间点到 schedule.production_time(字符串或数组),mode 设为 daily_fixed
          注册 cron 任务时使用 {"kind": "cron", "expr": "{M} {H} * * *", "tz": "{timezone}"}
→ 方式 B:保存小时数到 schedule.production_interval_hours,mode 设为 interval
          注册 cron 任务时使用 {"kind": "every", "everyMs": hours × 3600000}
```

**注意**:采集周期固定为每 1 小时一次(不可配置),每次完整生产后数据池会自动重置,确保每轮内容都是全新热点。

### 第 6 步:注册定时任务
配置保存完成后,**立即按「定时任务机制」章节的步骤注册三个 cron 任务**。

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
    },
    "publisher_persona": {
      "role": "用户自定义(如 'AI startup CEO')",
      "tone": "用户自定义(如 'professional but opinionated, data-driven')",
      "perspective": "用户自定义(如 '商业价值和市场机会')",
      "style_analysis": "从历史帖子自动分析(若不足5条则为 null)"
    }
  },
  "platform": "LinkedIn",
  "schedule": {
    "timezone": "用户提供",
    "production_mode": "daily_fixed 或 interval",
    "production_time": "14:30(方式A单个时间点)或 ['9:00','18:00'](方式A多个)",
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
每 24 小时        → [数据清理] 删除 10 天前的历史文件(报告永久保留)
```

> 生产触发时间由用户在第 5 步配置,支持两种模式:
> - **daily_fixed**:每天在指定时间点触发(`config.json` → `schedule.production_time`)
> - **interval**:每隔 N 小时触发(`config.json` → `schedule.production_interval_hours`)

---

### 数据池机制

- **数据池文件**:`outputs/pool/YYYYMMDD_trend_pool.json`(每天一个)
- 每次轻量采集将 Top 10 候选**追加**到当天数据池(`used: false`)
- 完整生产读取数据池 → 全局去重 → 取 Top 3(`used: false`)→ 执行阶段 3-7
- ⚠️ **完整生产结束后(无论成功或失败),必须立即重置数据池**:
  - 将当天数据池文件中**所有条目**的 `"used"` 字段设为 `true`
  - 目的:防止同一批热点在下一轮完整生产中被重复使用
  - 下一次轻量采集会追加全新热点,从而保证每轮内容都是最新的

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

> `last_production_reset`:记录上次完整生产后重置数据池的时间,用于排查问题。

---

### 任务 1:轻量采集(每 1 小时,固定不可更改)

**执行内容**:阶段 1 + 阶段 2(收集 + 筛选),结果写入数据池
**不执行**:阶段 3-7

**精确执行步骤:**
```
步骤 A1:bash skills/dailyhot-api/scripts/ensure_running.sh
步骤 A2:python3 skills/dailyhot-api/scripts/collect_trends.py --config config.json --output outputs/logs/{YYYYMMDD}_{HHMM}_raw_trends.json
步骤 A3:对收集结果执行阶段 2 打分公式,取 Top 10 候选
步骤 A4:追加到 outputs/pool/{YYYYMMDD}_trend_pool.json(所有新条目 used:false)
步骤 A5:bash skills/dailyhot-api/scripts/stop.sh
```

**静默执行,不通知用户。**

---

### 任务 2:完整生产(按用户配置的时间触发)

**精确执行步骤:**
```
步骤 B1:读取 config.json → schedule(确认触发模式和时间)
步骤 B2:读取 outputs/pool/{YYYYMMDD}_trend_pool.json
         → 若文件不存在:先执行一次轻量采集(任务1步骤A1-A5),再继续
         → 若 used:false 的条目不足 3 条:先执行一次轻量采集补充数据,再继续
步骤 B3:筛选所有 used:false 的热点,执行全局去重,按分数取 Top 3
步骤 B4:执行阶段 3 → 4 → 5 → 5.5 → 6 → 7(无论成功或失败)
步骤 B5:⚠️ 立即重置数据池:将当天数据池文件中所有条目的 "used" 设为 true,
         同时写入 "last_production_reset": "{当前时间ISO格式}"
         → Python 代码:
           import json, datetime
           pool_file = f"outputs/pool/{datetime.date.today().strftime('%Y%m%d')}_trend_pool.json"
           with open(pool_file, 'r+') as f:
               pool = json.load(f)
               for c in pool.get('collections', []):
                   for t in c.get('trends', []):
                       t['used'] = True
               pool['last_production_reset'] = datetime.datetime.now().astimezone().isoformat()
               f.seek(0); json.dump(pool, f, ensure_ascii=False, indent=2); f.truncate()
步骤 B6:将报告发送给用户
```

> ⚠️ **步骤 B5(数据池重置)必须执行,不得跳过**,即使阶段 3-7 中有部分失败也要执行。这是防止重复内容的核心机制。

**完成后将报告发送给用户。**

---

### 任务 3:数据清理(每 24 小时)

**精确执行步骤:**
```
步骤 C1:find outputs/images/ -name '*_image_urls.json' -mtime +10 -delete 2>/dev/null || true
步骤 C2:find outputs/briefs/ -name '*_brief.md' -mtime +10 -delete 2>/dev/null || true
步骤 C3:find outputs/scripts/ -name '*_image_prompt.md' -mtime +10 -delete 2>/dev/null || true
步骤 C4:find outputs/logs/ -name '*.json' -mtime +10 -delete 2>/dev/null || true
步骤 C5:find outputs/pool/ -name '*_trend_pool.json' -mtime +10 -delete 2>/dev/null || true
步骤 C6:du -sh outputs/ → 写入 outputs/logs/cleanup_log.json(追加)
```

> ⚠️ **绝对禁止**对 `outputs/reports/` 执行任何删除操作。

**静默执行,不通知用户。**

---

### 注册定时任务(第 6 步执行)

根据 `config.json` → `schedule.production_mode` 决定注册方式:

**当 production_mode = "daily_fixed" 时:**
读取 `schedule.production_time`(如 `"14:30"` 或 `["9:00", "18:00"]`),转换为 cron 表达式:
- 单时间点 `"14:30"` → `{"kind": "cron", "expr": "30 14 * * *", "tz": "{timezone}"}`
- 多时间点 `["9:00", "18:00"]` → 每个时间点分别注册一个 cron 任务

**当 production_mode = "interval" 时:**
读取 `schedule.production_interval_hours`,计算:
```
production_everyMs = production_interval_hours × 3600000
```
使用 `{"kind": "every", "everyMs": production_everyMs}`

**任务 1:轻量采集**
- name: `"热点轻量采集(每1小时)"`
- schedule: `{"kind": "every", "everyMs": 3600000}`
- payload: `{"kind": "agentTurn", "message": "执行定时轻量采集任务:运行阶段1和阶段2,将Top 10候选写入今天的数据池。只执行阶段1和2,不执行阶段3-7。静默执行。"}`
- sessionTarget: **"current"**
- delivery: `{"mode": "none"}`

**任务 2:完整生产**
- name: `"LinkedIn内容生产({用户配置的时间描述})"`(如"每天14:30"或"每6小时")
- schedule: 根据 production_mode 选择上方对应的 schedule 格式
- payload: `{"kind": "agentTurn", "message": "执行定时完整生产任务:严格按照 AGENTS.md「任务2:完整生产」步骤B1-B6执行。重点:步骤B5数据池重置必须执行,完成后将报告发送给用户。"}`
- sessionTarget: **"current"**
- delivery: `{"mode": "announce"}`

**任务 3:数据清理**
- name: `"历史数据清理(每24小时)"`
- schedule: `{"kind": "every", "everyMs": 86400000}`
- payload: `{"kind": "agentTurn", "message": "执行定时数据清理任务,按 AGENTS.md「任务3:数据清理」步骤C1-C6执行。绝对禁止删除 outputs/reports/ 目录。静默执行。"}`
- sessionTarget: **"current"**
- delivery: `{"mode": "none"}`

> ⚠️ sessionTarget 必须为 **"current"**,不能用 "isolated"(isolated 会话无聊天频道,报告推送失败)。

**注册完成后向用户确认:**
```
⏰ 定时任务已设置
📡 轻量采集: 每 1 小时 → 追加热点到数据池(生产后全部重置)
📌 LinkedIn 生产: {用户配置的时间描述} → 取 Top 3 → 生成 3 张图片 → 发布 → 重置数据池
🗑️ 数据清理: 每 24 小时 → 清理 10 天前历史文件(报告永久保留)

输入 'run now' 可手动立即触发一次完整生产
```

---

## 流水线执行(7 个阶段)

**触发方式:**
1. **手动**:用户输入 `run now` → 阶段 1-5.5-7 全部执行
2. **定时**:从数据池读取 → 阶段 3-5.5-7

**手动触发时先确认:**
```
📌 即将启动 LinkedIn 内容生产流水线
赛道: [niches]
关键词: [keywords 前5个]
发布平台: LinkedIn
预计耗时: 30-45 分钟(含 3 个图片生成 + 间隔发布)
确认启动?
```

**运行 ID**:`YYYYMMDD_HHMM`(用户时区)

---

### 阶段 1:热点收集

```bash
# 1.1 启动服务
bash skills/dailyhot-api/scripts/ensure_running.sh

# 1.2 收集趋势
python3 skills/dailyhot-api/scripts/collect_trends.py \
  --config config.json \
  --output outputs/logs/{运行ID}_raw_trends.json
```

**状态输出:**
```
📡 阶段 1/7 - 热点收集完成
平台成功: {N}/10 | 总收集: {N} 条
→ 进入阶段 2...
```

---

### 阶段 2:智能筛选 → Top 3

**打分公式:**
```
- 标题命中 keywords 中的词 → +15 分/词
- 标题或分类命中 niches → +10 分
- 平台排名前 3 → +10 分;前 5 → +5 分;前 10 → +2 分
- 同一话题跨平台出现 → 每多一个平台 +10 分
- 命中 exclude_keywords → 直接丢弃
```

**去重**:标题去标点后重叠字符数 / 较短标题字符数 > 0.7 即为重复,保留高分。

**写入** `outputs/logs/{运行ID}_top3.json`

**状态输出:**
```
📊 阶段 2/7 - 筛选完成
Top 3:
1. {标题} - {分}/100 - {平台} | 📌 {命中词}
2. {标题} - {分}/100 - {平台} | 📌 {命中词}
3. {标题} - {分}/100 - {平台} | 📌 {命中词}
→ 进入阶段 3...
```

---

### 阶段 3:热点深度提炼

**对 Top 3 每条执行:**
```
3.1:web_search 搜索标题(3-5 条结果)
3.2:web_fetch 读取 1-2 篇核心报道
3.3:按模板生成提炼卡
3.4:写入 outputs/briefs/{运行ID}_trend{1/2/3}_brief.md
```

**提炼卡模板(必须使用此格式):**
```markdown
# 热点提炼卡 - {标题}

## 📋 事件概要
{50-80字}

## 📊 关键数据
- {数据点 1}
- {数据点 2}
- {数据点 3}
- {数据点 4}
- {数据点 5}

## 🔍 多角度分析
- 正面视角:{好处}
- 反面视角:{隐忧}
- 行业影响:{影响}

## 💡 核心观点
1. "{金句1}"
2. "{金句2}"

## 🏷️ 话题标签
{10-15 个 #标签}
```

**规则**:事件概要和数据必须基于 web_search 实际结果,禁止编造。

**状态输出:**
```
📝 阶段 3/7 - 提炼完成
1. {标题} - {N} 篇报道 | {N} 条数据
2. {标题} - {N} 篇报道 | {N} 条数据
3. {标题} - {N} 篇报道 | {N} 条数据
→ 进入阶段 4...
```

---

### 阶段 4:图片提示词 + LinkedIn 帖子文案

**为 Top 3 的每条热点各生成:**
1) 一份 `giggle-generation-image` 可直接使用的"图片生成提示词"
2) 一条 LinkedIn 帖子文案(含 8-12 个 #标签,长度需满足 LinkedIn 限制)

**对 trend1、trend2、trend3 分别执行:**
```
4.1:读取 outputs/briefs/{运行ID}_trend{N}_brief.md
4.2:读取 config.json → content.video_style.project_type
4.3:从映射表获取图片风格参数(配色、版式、视觉元素)
4.4:读取 config.json → content.language,确定"LinkedIn 帖子文案语言"和"图片提示词语言"
4.5:读取 config.json → content.publisher_persona(角色、语气、视角、历史风格分析)
4.6:按模板生成"图片生成提示词 + LinkedIn 帖子文案"(禁止编造,必须来自提炼卡内容)
     ⚠️ 文案生成时必须融入发布者画像:
     - 以 {role} 的身份和专业背景切入话题
     - 使用 {tone} 指定的语气风格
     - 从 {perspective} 的角度分析和输出观点
     - 若 style_analysis 非 null,参考历史风格的开场方式、句式偏好、emoji 习惯等
4.7:写入 outputs/scripts/{运行ID}_trend{N}_image_prompt.md
```

**⚠️ 语言规则(必须严格执行):**
- `zh-CN`:帖子文案用中文;图片提示词可用中文关键词。
- `en`:帖子文案用英文;图片提示词用英文关键词。
- `bilingual`:帖子文案用"英文为主 + 中文短句括号补充";图片提示词使用"英文为主 + 少量中文关键词"以提升可控性。

**赛道→图片风格映射表:**

| 赛道 | project_type | 视觉元素关键词 | 版式建议 |
|------|-------------|----------------|-----------|
| 科技数码 | `narration` | 深蓝、全息界面、数据流 | 大标题 + 关键数据块(卡片化) |
| 财经理财 | `narration` | 图表、数据可视化、稳重质感 | 以"结论框/数字框"突出要点 |
| 娱乐八卦 | `director` | 分屏对比、强对比色、情绪符号 | 视觉冲突点用醒目图标 |
| 动漫游戏 | `director` | 角色元素、动感线条、漫画风分割 | 角色/符号居中,信息环绕 |
| 美食探店 | `short-film` | 食物特写、暖色调、质感光影 | 主题食物居中 + 结论短句 |
| 健身运动 | `short-film` | 运动节奏感、对比变化、力量感 | 进度/对比条形结构 |
| 时尚穿搭 | `short-film` | 街拍、杂志排版、排版留白 | 杂志封面式版式 |
| 教育知识 | `narration` | 思维导图、图解结构、信息网格 | 用"框图/要点列表"呈现 |
| 职场成长 | `director` | 办公场景、逆袭对比、励志符号 | "问题→方法→结果"三段式 |

**图片提示词 + 帖子模板(必须使用此格式):**
```markdown
# 图片生成提示词 - {标题}

## 图片生成参数
- aspect-ratio: 3:4(LinkedIn 信息流竖图,4:5 的近似落地)
- model: seedream45
- generate_count: 1

## 图片提示词(直接用于 giggle-generation-image --prompt)
{必须包含:1) 事件核心结论(来自提炼卡核心观点);2) 1-2 个关键数据点(来自提炼卡关键数据);3) 视觉元素关键词(来自映射表);4) 版式建议(来自映射表)。}

## LinkedIn 帖子文案（用于 x2c-socialposter --post）
{结构建议：以 {role} 的身份切入；开头一句引发共鸣/观点；主体 80-160 字展开（不得超出提炼卡），从 {perspective} 角度分析；结尾 1 个提问引导互动。语气须符合 {tone} 设定。}
（语言：按 4.4 与 语言规则生成；结尾附 8-12 个 #标签，emoji 风格参考 style_analysis，无则适量 1-3 个。）
```

**状态输出:**
```
🖼️ 阶段 4/7 - 图片提示词与帖子文案完成
1. {标题} | {风格名} ({project_type}) | ✅
2. {标题} | {风格名} ({project_type}) | ✅
3. {标题} | {风格名} ({project_type}) | ✅
→ 进入阶段 5...
```

---

### 阶段 5:图片生成

**为 3 条热点分别生成 1 张 LinkedIn 图片(共 3 张)。对 trend1、trend2、trend3 依次执行:**

```
5.1:读取 outputs/scripts/{运行ID}_trend{N}_image_prompt.md
5.2:提取"图片提示词"部分的全文,作为 `{prompt_text}`
5.3:从 config.json 读取 giggle_api_key
5.4:export GIGGLE_API_KEY="{giggle_api_key}"
5.5:提交图片生成任务(异步,取 task_id):
python3 skills/giggle-generation-image/scripts/generation_api.py \
  --prompt "{prompt_text}" \
  --aspect-ratio 3:4 \
  --model seedream45 \
  --resolution 2K \
  --generate-count 1 \
  --no-wait \
  --json
5.6:等待完成(每 15-30 秒轮询一次,直到 completed/failed):
python3 skills/giggle-generation-image/scripts/generation_api.py --query --task-id {task_id}
5.7:从查询结果中提取图片查看链接 URLs,并写入:
outputs/images/{运行ID}_trend{N}_image_urls.json
   (每次 1 张图片:image_urls: [url])
```

**失败处理**:单张图片生成失败则重试 1 次;仍失败则跳过该 trend 的发布,继续生成下一个,报告中标注。

**状态输出:**
```
🖼️ 阶段 5/7 - 图片生成完成
1. {标题} - 1 张图片 ✅(或 ❌ 失败已跳过)
2. {标题} - 1 张图片 ✅(或 ❌ 失败已跳过)
3. {标题} - 1 张图片 ✅(或 ❌ 失败已跳过)
→ 进入阶段 5.5(图片校验)...
```

---

### 阶段 5.5:图片校验与本地化(发布前自动执行)

**目的**:确保阶段 5 已为每个 trend 生成至少 1 张可用图片,**并将远程图片下载到本地**,从而避免发布阶段因远程 URL 签名过期、特殊字符转义或超时导致发布失败。

> ⚠️ **关键教训**:Giggle API 返回的图片 URL 包含 CloudFront 签名参数(Policy、Signature 等),这些 URL 直接传给 x2c-socialposter 会因 URL 编码问题导致 400 错误或超时。**必须先下载到本地文件,再用本地路径发布。**

**触发规则**:对每个已生成的 trend 执行校验 + 下载:
- 若 `outputs/images/{运行ID}_trend{N}_image_urls.json` 不存在或 `image_urls` 为空 → 标记该 trend 跳过发布
- 若 `image_urls` 非空 → 下载图片到本地 → 校验文件大小 → 继续发布

**精确执行步骤(对 trend1、trend2、trend3 分别执行):**
```
5.5.1:读取 outputs/images/{运行ID}_trend{N}_image_urls.json
5.5.2:检查 image_urls 数组长度
5.5.3:若长度 == 0:写入 outputs/logs/{运行ID}_image_validation_{N}.json(success:false),并跳过该 trend
5.5.4:若长度 >= 1:用 curl 将第 1 个 URL 下载到本地文件:
       curl -s -L -o outputs/images/{运行ID}_trend{N}_local.jpg "{image_urls[0]}"
5.5.5:校验下载文件大小(必须 > 10KB,否则视为下载失败):
       - 若文件 < 10KB → 可能是错误响应(如 XML 错误),标记失败
       - 若下载失败 → 重新查询 Giggle 任务获取最新 URL,再试 1 次
5.5.6:写入 outputs/logs/{运行ID}_image_validation_{N}.json:
       {success: true/false, count: 1, local_path: "outputs/images/{运行ID}_trend{N}_local.jpg", file_size_bytes: {size}}
5.5.7:不执行任何压缩/转码(图片无需 ffmpeg)
```

> 💡 **为什么下载到本地?** x2c-socialposter 的 `--media-urls` 参数同时支持远程 URL 和本地文件路径。传入本地路径时,脚本会自动通过 presigned URL 或 direct upload 将文件上传到 X2C CDN,这比直接传 Giggle 的签名 URL 更可靠。

**状态输出:**
```
📦 阶段 5.5 - 图片校验与本地化完成
1. {标题} - 1 张图片已下载到本地 ✅ ({文件大小}KB)(或 ❌ 跳过)
2. {标题} - 1 张图片已下载到本地 ✅ ({文件大小}KB)(或 ❌ 跳过)
3. {标题} - 1 张图片已下载到本地 ✅ ({文件大小}KB)(或 ❌ 跳过)
→ 进入阶段 6...
```

---

### 阶段 6:LinkedIn 发布

**将 3 张图片依次发布到 LinkedIn,每条帖子之间间隔 10 分钟。**

```
6.1:export X2C_API_KEY="{x2c_api_key}"
6.2:python3 skills/x2c-socialposter/scripts/x2c_social.py --action status
     → 确认 LinkedIn 已关联,否则暂停通知用户
6.3:发布 trend1 帖子(命令见下方)
6.4:等待 10 分钟(sleep 600)
6.5:发布 trend2 帖子
6.6:等待 10 分钟(sleep 600)
6.7:发布 trend3 帖子
6.8:bash skills/dailyhot-api/scripts/stop.sh
```

> ⚠️ **间隔规则**:每发布一条帖子后,必须等待 10 分钟再发布下一个。用 `sleep 600` 或等效方式实现。如果某个 trend 在阶段 5.5 校验失败(图片缺失),则跳过该帖子发布,但仍然等待 10 分钟后再发布下一个。

**LinkedIn 发布命令(对每个 trend 执行一次,替换 {N}):**

> ⚠️ **必须使用阶段 5.5 下载的本地文件路径,不得直接使用 Giggle 远程 URL。** 远程签名 URL 包含特殊字符,会导致 shell 转义问题和 x2c API 400 错误。

```bash
python3 skills/x2c-socialposter/scripts/x2c_social.py \
  --action publish \
  --platforms linkedin \
  --post "{trend{N} 图片提示词文件中 LinkedIn 帖子文案全文(注意去换行/长度控制)}" \
  --media-urls "outputs/images/{运行ID}_trend{N}_local.jpg"
```

> x2c-socialposter 检测到本地路径后会自动上传到 X2C CDN,再发布到 LinkedIn。

**结果处理:**
- `success: true` → 记录 post_id ✅
- `success: false` / 401 → 暂停,通知用户重新授权
- 400 → 记录错误 ❌,继续发布下一个

**状态输出:**
```
📲 阶段 6/7 - LinkedIn 发布完成
1. {标题} - ✅ Post ID: {id}
   ⏳ 等待 10 分钟...
2. {标题} - ✅ Post ID: {id}
   ⏳ 等待 10 分钟...
3. {标题} - ✅ Post ID: {id}
→ 进入阶段 7...
```

---

### 阶段 7:汇总报告

```
7.1:生成 JSON 日志 → outputs/logs/{运行ID}_publish_log.json
7.2:生成报告 → outputs/reports/{运行ID}_内容产出报告.md
7.3:将报告内容发送给用户
```

**报告模板:**
```markdown
# 📋 LinkedIn 内容产出报告

> 📌 LinkedIn-自媒体运营 · v5
> 📅 {日期时间}
> ⏱ 总耗时:约 {N} 分钟

---

## 🔎 本期内容方向
| 项目 | 设定 |
|------|------|
| 赛道 | {niches} |
| 关键词 | {keywords} |
| 排除词 | {exclude_keywords} |
| 图片风格 | {风格名} |

---

## 📡 Top 3 热点
| # | 标题 | 评分 | 来源 |
|---|------|------|------|
| 1 | {标题} | {分}/100 | {平台} |
| 2 | {标题} | {分}/100 | {平台} |
| 3 | {标题} | {分}/100 | {平台} |

---

## 📰 热点提炼卡

### 热点 1:{标题}
{完整嵌入 trend1_brief.md}

### 热点 2:{标题}
{完整嵌入 trend2_brief.md}

### 热点 3:{标题}
{完整嵌入 trend3_brief.md}

---

## 🖼️ 图片(3 个)

### 图片 1:{标题}
| 项目 | 详情 |
|------|------|
| 风格 | {风格名} |
| 文件 | outputs/images/{运行ID}_trend1_image_urls.json |

**LinkedIn 帖子文案:**
{完整嵌入 trend1_image_prompt.md 中"LinkedIn 帖子文案"}

### 图片 2:{标题}
| 项目 | 详情 |
|------|------|
| 风格 | {风格名} |
| 文件 | outputs/images/{运行ID}_trend2_image_urls.json |

**LinkedIn 帖子文案:**
{完整嵌入 trend2_image_prompt.md 中"LinkedIn 帖子文案"}

### 图片 3:{标题}
| 项目 | 详情 |
|------|------|
| 风格 | {风格名} |
| 文件 | outputs/images/{运行ID}_trend3_image_urls.json |

**LinkedIn 帖子文案:**
{完整嵌入 trend3_image_prompt.md 中"LinkedIn 帖子文案"}

---

## 📲 发布结果
| # | 标题 | 状态 | Post ID | 发布时间 |
|---|------|------|---------|---------|
| 1 | {标题} | {✅/❌} | {id} | {HH:MM} |
| 2 | {标题} | {✅/❌} | {id} | {HH:MM}(+10分钟) |
| 3 | {标题} | {✅/❌} | {id} | {HH:MM}(+20分钟) |

---

## 📁 产出文件
{文件路径列表}

---
> 🤖 LinkedIn-自媒体运营 v5 自动生成
```

**规则**:报告自包含,提炼卡、图片提示词与 LinkedIn 帖子文案完整嵌入,并包含发布结果。生成后必须发送给用户。

---

## 已加载的技能

| 技能 | 功能 | 阶段 | 依赖 |
|------|------|------|------|
| `dailyhot-api` | 40+ 平台热榜聚合 | 阶段 1 | Node.js ≥ 20 |
| `giggle-generation-image` | Giggle API 图片生成 | 阶段 5 | Giggle API Key |
| `x2c-socialposter` | LinkedIn 帖子发布 | 阶段 6 | X2C API Key |

---

## 权限边界

- **工作区**:`~/.openclaw/workspace-LinkedIn-image-trend-automator/`
- **输出目录**:`outputs/{briefs,scripts,images,reports,logs,pool}/`
- **禁止**:写入工作区外的任何路径

---

## 会话启动行为

1. 检查 `config.json`
2. **不存在** → 配置向导
3. **存在** → 显示摘要:

```
📌 LinkedIn 自媒体运营 - 就绪
赛道:{niches}
关键词:{keywords 前5个}
LinkedIn:@{handle}

⏰ 定时任务:
  📡 轻量采集: 每 1 小时 - {状态}
  📌 LinkedIn 生产: {用户配置的时间描述} - {状态}(生产后自动重置数据池)
  🗑️ 数据清理: 每 24 小时 - {状态}

📊 今日数据池: {N} 条采集 | {N} 条未使用
🕐 上次数据池重置: {last_production_reset 或 "从未生产"}

输入 'run now' 手动触发
```

---

## 错误处理速查表

| 错误 | 阶段 | 处理 |
|------|------|------|
| DailyHotApi 启动失败 | 1 | 检查 Node.js,重新 ensure_running.sh |
| 平台采集 500 | 1 | 跳过该平台,继续其他 |
| Top 3 不足 | 2 | 有多少用多少,最少 1 条 |
| web_search 无结果 | 3 | 换关键词重新搜索 |
| Giggle API 超时 | 5 | 重试 1 次,仍失败跳过 |
| Giggle 余额不足 | 5 | 暂停,通知用户充值 |
| Giggle 图片生成失败 | 5 | 重试 1 次,仍失败则跳过该 trend |
| 图片下载失败/文件过小 | 5.5 | 重新查询 Giggle 任务获取最新 URL,再试 1 次 |
| 远程 URL 发布 400/超时 | 6 | **禁止直接用远程 URL**,必须先下载到本地再用本地路径发布 |
| 图片校验失败 | 5.5 | 跳过该 trend 发布,继续下一个 |
| X2C 发布超时 | 6 | 重试 1 次,仍失败记录错误 |
| X2C 401 | 6 | 暂停,通知用户重新授权 |
| X2C 400 | 6 | 记录错误 |
| 数据池为空 | B1 | 先执行一次轻量采集 |
| 数据池不足 3 条 | B4 | 有多少用多少 |
| 清理误删 reports/ | 清理 | 绝对禁止,find 命令不含 reports 路径 |
| outputs/ 目录不存在 | 清理 | 跳过该目录,继续其他,不报错 |
