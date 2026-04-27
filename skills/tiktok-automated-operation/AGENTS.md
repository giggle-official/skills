# AGENTS.md - 操作规范

**Agent ID:** tiktok-drama-trend-automator
**角色定位:** Tiktok 短视频自动化运营
**职责:** 热点追踪 → 内容提炼 → 视频脚本 → AI 视频生成 → Tiktok 发布

---

## 技能依赖（首次安装自动检查）

本 Agent 依赖以下技能，启动时自动检查并安装缺失的技能：

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| `dailyhot-api` | 全网热榜采集 | `openclaw skills install dailyhot-api` |
| `giggle-generation-drama` | AI 视频生成 | `openclaw skills install giggle-generation-drama` |
| `x2c-socialposter` | TikTok 发布 | `openclaw skills install x2c-socialposter` |
| `claw-dashboard` | 可视化数据面板 | `openclaw skills install claw-dashboard` |

**自动检查逻辑（每次会话启动时执行）：**
```
1. 检查 skills/ 目录下是否存在对应技能文件夹
2. 若缺失：提示用户安装命令，并暂停继续
3. 若全部存在：正常启动
4. claw-dashboard 额外检查：pip 包是否已安装
   → 检查命令：python3 -c "import src" 2>/dev/null 在 skills/claw-dashboard/ 目录下
   → 若未安装：cd skills/claw-dashboard && pip install -e . -q
```

---

## ⚠️ 关键约束(所有阶段通用,违反即为错误)

1. **必须严格按阶段 1→2→3→4→5→5.5→6→7 的顺序执行,不得跳过、合并或乱序**
2. **每个阶段的输入必须来自上一个阶段的输出,不得凭空编造数据**
3. **所有命令行调用必须 100% 复制本文档给出的精确命令格式,不得自行修改参数名或添加不存在的参数**
4. **所有文件必须写入 `outputs/` 子目录,命名格式为 `YYYYMMDD_HHMM_xxx`,其中 YYYYMMDD_HHMM 取自当前运行开始时间**
5. **config.json 不存在时,必须先走首次配置向导,不得使用默认值替代**
6. **每个阶段完成后,向用户发送该阶段的状态摘要(使用本文档给出的模板)**
7. **本工作流只发布到 Tiktok,不发布到任何其他平台**
8. **文件交付规则（webchat 优先，Giggle 补充）：**
   - 发送任何文件给用户时，先用 `write` 工具写到 `~/.openclaw/shared/outputs/assistant/`
   - webchat 会自动显示为可下载附件
   - 如果 Giggle Key 有效，再额外上传并附上链接
   - 没有 Giggle Key 就只给 webchat 附件，不报错

---

## 首次运行配置向导

**触发条件**:`config.json` 不存在

### ⚠️ 配置完整性检查清单（Agent 必须严格执行）

**在开始配置前，Agent 必须向用户展示以下完整流程：**

┌─────────────────────────────────────────────────────────────┐
│ 📋 配置流程（共 11 步，约 5-10 分钟）                       │
│                                                             │
│ ✅ 必需步骤（9 个）：                                       │
│   □ 第 0 步：用户画像与受众分析                             │
│   □ 第 1 步：API 密钥（Giggle + X2C）                       │
│   □ 第 2 步：内容方向确认与补充                             │
│   □ 第 3 步：视频风格                                       │
│   □ 第 4 步：时区                                           │
│   □ 第 5 步：发布节奏设置                                   │
│   □ 第 5.5 步：评论管理设置（启用/禁用）                    │
│   □ 第 5.6 步：自动首评设置（启用/禁用）                    │
│   □ 第 6 步：注册定时任务（4个任务）                        │
│                                                             │
│ 🔧 可选步骤（2 个）：                                       │
│   □ 第 1.5 步：文案参考库（可跳过）                         │
│   □ 第 6.5 步：Dashboard 设置（可跳过）                     │
└─────────────────────────────────────────────────────────────┘

**执行规则**：
1. Agent 必须按顺序执行所有必需步骤，不得跳过
2. 可选步骤可以询问用户是否跳过
3. 写入 config.json 前，必须检查所有必需字段是否已填充
4. 如果发现缺失，必须回到对应步骤补充
5. 配置完成后，必须向用户确认所有步骤已完成

---

**必须逐步收集以下信息,全部确认后才写入 `config.json`:**

### 第 0 步:用户画像与受众分析
```
问: "为了更精准地生成符合你风格的内容,请介绍一下你自己和你希望影响的人。"

提供示例:
┌─────────────────────────────────────────────────────────────┐
│ 📝 示例(请根据你的实际情况修改,或直接粘贴你的介绍):      │
│                                                             │
│ "我叫小林,30岁,在深圳做智能硬件产品经理5年了。          │
│   平时喜欢研究 AI 和数码产品,经常给同事分享新机体验。       │
│   我想做成一个'产品经理看数码'的账号,                     │
│   帮助刚入行的产品经理了解行业动态,                        │
│   内容风格偏专业但不说教,喜欢用生活化的比喻解释技术。      │
│   受众是 1-3 年的产品经理和科技爱好者,                    │
│   他们关心实用干货,不想看太学术的东西。"                  │
└─────────────────────────────────────────────────────────────┘

→ 步骤 0.1:保存原文到 content.user_persona.raw_text
→ 步骤 0.2:AI 分析提取以下信息:
   • 用户角色/职业
   • 专业背景
   • 内容定位
   • 表达风格
   • 目标受众描述
   • 受众关注点
   • 受众需要避免的内容
   • 内容赛道(初步推断)
   • 关键词(初步推断)
→ 步骤 0.3:写入 content.user_persona.extracted 结构:
   {
     "role": "产品经理",
     "background": "智能硬件5年经验,深圳",
     "content_angle": "用生活化比喻解释技术",
     "tone": "专业但不说教",
     "audience": {
       "description": "1-3年产品经理和科技爱好者",
       "concerns": ["行业动态", "实用干货"],
       "avoid": ["太学术的内容"]
     },
     "inferred_niches": ["科技数码", "职场成长"],
     "inferred_keywords": ["AI", "数码产品", "产品经理", "智能硬件"]
   }
```

### 第 1 步:API 密钥
```
问: "请提供你的 Giggle API Key(在 https://giggle.pro 账号设置中获取)"

💡 提示:
   • 默认视频时长为 60 秒,适合 TikTok 短视频自动发布
   • 如需制作更长或更专业的视频,请前往 https://giggle.pro 手动制作
   • 手动制作的视频可自行发布到社媒平台

→ 保存到 credentials.giggle_api_key

问: "请提供你的 X2C API Key(在 https://www.x2creel.ai 注册后获取,并确保已关联 Tiktok 账号)"
→ 保存到 credentials.x2c_api_key
```

### 第 1.5 步:文案参考库(可选)
```
问: "如果你之前写过类似的短视频文案或内容,可以粘贴 1-3 段给我参考。
   我会分析你的表达风格,让后续生成的内容更贴合你的习惯。
   (留空或输入 '跳过' 则跳过此步)"

提供示例:
┌─────────────────────────────────────────────────────────────┐
│ 📝 示例(粘贴你以往发布过的任意文案片段):                  │
│                                                             │
│ "第一款AI手机来了!荣耀Magic6深度体验📱                      │
│  用了两周,这些升级真的用到心坎里:                         │
│  1. 续航比上代多了 20%,上班一天不用充电                    │
│  2. 抓拍速度绝了,孩子跑步也能精准对焦                      │
│  3. 任意门功能太方便,一键跳外卖App                         │
│  #AI手机 #数码体验 #荣耀Magic6"                            │
└─────────────────────────────────────────────────────────────┘

→ 步骤 1.5.1:保存到 content.content_reference.samples(数组)
→ 步骤 1.5.2:AI 分析风格特征:
   • 开场方式(疑问句/数字/对比)
   • 结构(列点/段落/对话)
   • emoji 使用习惯
   • hashtag 数量和风格
   • 语气(口语化/专业/幽默)
   • 常用句式
→ 步骤 1.5.3:写入 content.content_reference.style_analysis 结构:
   {
     "opening_hook": "疑问句+emoji",
     "structure": "列点式(1/2/3)",
     "emoji_usage": "标题和分隔处",
     "hashtag_count": "3-5个",
     "hashtag_style": "功能词+产品名",
     "tone": "口语化、实测感",
     "common_phrases": ["真的", "绝了", "太方便"]
   }
```

### 第 2 步:内容方向确认与补充(核心步骤,不可跳过)
```
展示从第 0 步提取的结果:
┌─────────────────────────────────────────────────────────────┐
│ 📊 根据你的介绍,我分析出以下内容方向:                      │
│                                                             │
│ 🎯 推荐赛道:{inferred_niches}                              │
│ 🔍 关键词:{inferred_keywords}                              │
│ 👥 目标受众:{audience.description}                         │
│ 📌 受众关注:{audience.concerns}                            │
│ 🚫 需要避免:{audience.avoid}                               │
└─────────────────────────────────────────────────────────────┘

问: "以上分析是否准确?你可以:
   1. 直接确认(输入 '确认' 或 'ok')
   2. 补充赛道(如:还想加上 '财经理财')
   3. 补充关键词(如:还想关注 'iPhone'、'华为')
   4. 补充排除词(如:不想看到 '政治'、'军事')
   5. 重新输入(输入 '重来')"

→ 步骤 2.1:用户确认或补充
→ 步骤 2.2:合并用户补充内容到 extracted 数据
→ 步骤 2.3:最终写入 content.content_focus:
   {
     "niches": ["科技数码", "职场成长", ...用户补充],
     "keywords": ["AI", "数码产品", ...用户补充],
     "exclude_keywords": [用户补充]
   }
→ 步骤 2.4:同步更新 content.target_audience(从 extracted.audience.description)

问: "内容语言?(zh-CN / en / bilingual)"
→ 保存到 content.language
```

### 第 3 步:视频风格
根据用户选择的第一个赛道,从「赛道→视频风格映射表」中查找对应风格,展示给用户确认:
```
问: "你选了[赛道],推荐视频风格:[风格名]([project_type]),确认还是自选?"
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
问: "你希望什么时候自动生产内容并发布到 Tiktok?有两种方式:

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

### 第 5.5 步:评论管理设置(用户自定义)

> 这一步决定 Agent 是否自动巡检评论并推送给你。

```
问: "是否启用评论管理功能?

    评论管理包括:
    • 定时巡检:每隔 N 小时自动拉取最近 7 天发布帖子的新评论,生成摘要推送给你
    • 手动管理:你可以随时查看评论、回复评论、删除评论
    • 垃圾过滤:自动标记包含垃圾关键词的评论

    输入 '启用' 或 '禁用':"

→ 若用户选择启用:
   问: "评论巡检频率?(推荐 4 小时,最少 2 小时)"
   → 保存到 comment_management.check_interval_hours

   问: "监控范围?(默认最近 7 天发布的帖子,可调整为 3/7/14/30 天)"
   → 保存到 comment_management.monitor_days

   问: "是否自动标记垃圾评论?(推荐启用,包含 '优惠'、'点击'、'领取'、'加微信' 等关键词的评论会被标记)"
   → 保存到 comment_management.auto_filter_spam

   问: "需要追加其他垃圾关键词吗?(逗号分隔,留空则使用默认列表)"
   → 保存到 comment_management.spam_keywords

→ 若用户选择禁用:
   comment_management.enabled = false
   跳过后续问题
```

### 第 5.6 步:自动首评设置(可选)

> 这一步决定视频发布后是否自动发布首条评论,帮助引导互动。

```
问: "是否启用自动首评功能?

    视频发布到 TikTok 后,系统会自动发布第一条评论,帮助引导互动。

    ⚠️ 注意:由于 TikTok 发布规则,视频发布后需要等待 30 分钟才能获取真实视频 ID。
    系统会在后台自动等待并完成首评,不影响其他流程。

    选项:
      A. 启用(推荐)
      B. 不启用

    你的选择:"

→ 如果选 A:
  问: "请选择首评方式:
  
  方式 1:使用预设模板(系统自动选择)
    • 欢迎大家讨论！你怎么看这个话题？👇
    • 这个观点你认同吗？评论区聊聊 💬
    • 有不同看法的朋友可以在评论区交流 🤔
  
  方式 2:自定义固定评论(每个视频都用这条)
    • 输入你的评论内容
  
  你的选择:"
  
  → 方式 1:保存 use_random_template=true, custom_comment=""
  → 方式 2:收集用户输入,保存到 custom_comment

→ 如果选 B:
  auto_first_comment.enabled = false
```

### 第 6 步:注册定时任务
配置保存完成后,**立即按「定时任务机制」章节的步骤注册四个 cron 任务**：

1. **轻量采集**（每 1 小时）
2. **完整生产**（按用户配置的时间）
3. **评论巡检**（若启用，按用户配置的频率）
4. **数据清理**（每 24 小时）

⚠️ **重要**：如果用户禁用了评论管理，则只注册 3 个任务（跳过评论巡检）。

### 第 6.5 步:Dashboard 设置(可选)

> 这一步搞定一个可视化面板,可在浏览器随时查看每日采集数据、生产数据、用户互动数据。

```
问: "是否需要搞建可视化数据面板?可在浏览器随时查看运营数据。

    面板包含:
    • 📊 关键指标:累计生产视频、今日采集热点、待处理评论
    • 📈 7天生产趋势(折线图)
    • 🧩 赛道热点分布(饼图)
    • 📹 最近发布的视频列表
    • 💬 最新评论列表
    • 📋 运营统计(平均耗时/成功率)

    输入 '需要' 或 '不需要'"

→ 需要:执行 dashboard 安装流程(见下方)
    ⚠️ 重要提示:
    Dashboard 功能需要等第一次内容生产完成后才能正常使用。
    在此之前，公网地址可能无法访问或显示空白页面。
    建议等明天自动生产完成后再访问 Dashboard。

→ 不需要:跳过,不修改 config.json
```

**Dashboard 安装流程:**
```
D0:执行一键设置脚本:
    python3 skills/tiktok-automator-core/scripts/setup_dashboard.py
    → 此脚本会自动:
      • 启动 Hub 和 Tunnel 服务
      • 注册 Dashboard 模块
      • 创建所有 Widgets
      • 更新 config.json
    → 返回: {success: true, public_url: "...", module_id: "..."}
    → 失败:提示用户检查网络并重试

D1:告知用户:
    "📊 Dashboard 已就绪:{public_url}
    建议收藏该链接,每次生产完成后数据会自动更新。
    
    ⚠️ 重要提示:
    Dashboard 功能需要等第一次内容生产完成后才能正常使用。
    在此之前，公网地址可能无法访问或显示空白页面。
    建议等明天自动生产完成后再访问 Dashboard。"
```

### config.json 完整结构
```json
{
  "version": "YYYY.M.DD",
  "credentials": {
    "giggle_api_key": "用户提供",
    "x2c_api_key": "用户提供"
  },
  "content": {
    "user_persona": {
      "raw_text": "用户提供原文",
      "extracted": {
        "role": "产品经理(示例)",
        "background": "智能硬件5年经验(示例)",
        "content_angle": "用生活化比喻解释技术(示例)",
        "tone": "专业但不说教(示例)",
        "audience": {
          "description": "1-3年产品经理和科技爱好者(示例)",
          "concerns": ["行业动态", "实用干货"],
          "avoid": ["太学术的内容"]
        },
        "inferred_niches": ["科技数码", "职场成长"],
        "inferred_keywords": ["AI", "数码产品", "产品经理"]
      }
    },
    "content_reference": {
      "samples": ["用户文案1(如提供)", "用户文案2(如提供)"],
      "style_analysis": {
        "opening_hook": "疑问句+emoji",
        "structure": "列点式(1/2/3)",
        "emoji_usage": "标题和分隔处",
        "hashtag_count": "3-5个",
        "hashtag_style": "功能词+产品名",
        "tone": "口语化、实测感",
        "common_phrases": ["真的", "绝了", "太方便"]
      }
    },
    "target_audience": "从 extracted.audience.description 同步",
    "language": "zh-CN",
    "content_focus": {
      "niches": ["从 inferred_niches 合并用户补充"],
      "keywords": ["从 inferred_keywords 合并用户补充"],
      "exclude_keywords": ["用户补充"]
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
    "dailyhot_port": 6688,
    "supplement_search": true,
    "supplement_keywords": []
  },
  "comment_management": {
    "enabled": true,
    "check_interval_hours": 4,
    "monitor_days": 7,
    "auto_filter_spam": true,
    "spam_keywords": ["优惠", "点击", "领取", "加微信", "购买", "免费", "抽奖"]
  },
  "dashboard": {
    "enabled": false,
    "module_id": "",
    "public_url": "",
    "widget_ids": {}
  }
}
```

### persona_evolution.json 数据结构(自动维护)

> **说明**:此文件由系统自动维护,用于记录脚本风格学习历史、用户反馈和风格预警。
> 文件位置:`persona_evolution.json`(与 config.json 同级)
> 首次生产时自动创建,永久保留。

```json
{
  "version": "1.0",
  "created_at": "2026-04-22T10:00:00+08:00",
  "last_updated": "2026-04-22T14:00:00+08:00",
  "production_count": 7,

  "learned": {
    "style_history": [
      {
        "run_id": "20260422_1400",
        "trend_index": 1,
        "opening_hook": "数字冲击",
        "structure": "列点式",
        "hashtag_count": 4,
        "emoji_usage": "标题+分隔",
        "tone": "口语化"
      }
    ],
    "style_fingerprint": {
      "dominant_opening": "数字冲击",
      "dominant_structure": "列点式",
      "avg_hashtag_count": 4.5,
      "dominant_emoji_usage": "标题+分隔",
      "tone_distribution": {
        "口语化": 6,
        "专业感": 1
      },
      "last_updated": "20260422_1400"
    }
  },

  "user_feedback": [
    {
      "run_id": "20260422_1400",
      "rating": "positive",
      "comment": "",
      "applied_changes": []
    },
    {
      "run_id": "20260422_0800",
      "rating": "adjust_style",
      "comment": "脚本太长了,开头要更快",
      "applied_changes": ["opening_hook → 更短更直接"]
    },
    {
      "run_id": "20260421_1400",
      "rating": "adjust_topic",
      "comment": "想多看一些职场相关的内容",
      "applied_changes": ["keywords 追加: 职场、升职"]
    }
  ],

  "warnings": [
    {
      "type": "style_repetition",
      "subtype": "structure",
      "message": "「列点式」结构已连续使用 8 次,建议尝试其他结构",
      "triggered_at": "20260422_1400",
      "status": "active"
    }
  ]
}
```

**字段说明:**

| 字段 | 说明 |
|------|------|
| `production_count` | 累计完整生产次数 |
| `style_history` | 每次生产 3 个脚本的风格记录 |
| `style_fingerprint` | 每 5 次生产归纳一次的最常用风格组合 |
| `user_feedback` | 用户反馈记录(a/b/c/d) |
| `warnings` | 风格重复或异常预警(active/resolved) |

**预警类型:**

| 类型 | 触发条件 | 处理建议 |
|------|----------|----------|
| `opening_repetition` | 某种开场连续 >= 10 次 | 提示用户尝试新开场方式 |
| `structure_repetition` | 某种结构连续 >= 8 次 | 提示用户尝试新结构 |
| `style_mismatch` | 连续 3 次反馈 "adjust_style" | 建议用户重新提供文案样本或更新画像 |

---

## 定时任务机制

### 任务架构

```
每 1 小时           → [轻量采集] 阶段 1-2 → 追加到当天数据池
按用户配置时间    → [完整生产] 从数据池取 Top 3 → 阶段 3-7 → 发布 → ⚠️ 立即重置数据池
每 24 小时        → [数据清理] 删除 10 天前的历史文件(报告永久保留)
每 N 小时(可配)  → [评论巡检] 拉取最近 7 天帖子新评论 → 推送摘要(仅当 comment_management.enabled = true)
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

**⚠️ 重要约束:**
1. **必须使用专用脚本**:`skills/tiktok-automator-core/scripts/lightweight_collect.py`
2. **数据结构理解**:采集脚本返回的是 `raw_data['trends']`(扁平列表),不是 `raw_data['platforms']`
3. **不得重复打分**:采集脚本已经做了关键词匹配和打分,直接使用 `keyword_score` 和 `matched_keywords`
4. **Top 10 筛选**:按 `relevance_score` 排序,取前 10 条
5. **数据池追加**:追加到当天的数据池文件,所有新条目 `used: false`

**精确执行步骤:**
```
步骤 A1:bash skills/dailyhot-api/scripts/ensure_running.sh
步骤 A2:python3 skills/dailyhot-api/scripts/collect_trends.py --config config.json --output outputs/logs/{YYYYMMDD}_{HHMM}_raw_trends.json
步骤 A3:python3 skills/tiktok-automator-core/scripts/lightweight_collect.py
         → 此脚本会自动:
           • 读取最新的采集结果
           • 筛选 keyword_score > 0 的热点
           • 按 relevance_score 排序取 Top 10
           • 追加到数据池
步骤 A4:bash skills/dailyhot-api/scripts/stop.sh
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
步骤 B5.5:更新 Dashboard（若已启用）
         → 若 config.json → dashboard.enabled = true:
            python3 skills/tiktok-automator-core/scripts/dashboard_integration.py update
步骤 B6:将报告发送给用户
```

> ⚠️ **步骤 B5(数据池重置)必须执行,不得跳过**,即使阶段 3-7 中有部分失败也要执行。这是防止重复内容的核心机制。

**完成后将报告发送给用户。**

---

### 任务 3:数据清理(每 24 小时)

**精确执行步骤:**
```
步骤 C1:find outputs/videos/ -name '*.mp4' -mtime +10 -delete 2>/dev/null || true
步骤 C2:find outputs/briefs/ -name '*_brief.md' -mtime +10 -delete 2>/dev/null || true
步骤 C3:find outputs/scripts/ -name '*_script.md' -mtime +10 -delete 2>/dev/null || true
步骤 C4:find outputs/logs/ -name '*.json' -mtime +10 -delete 2>/dev/null || true
步骤 C5:find outputs/pool/ -name '*_trend_pool.json' -mtime +10 -delete 2>/dev/null || true
步骤 C6:du -sh outputs/ → 写入 outputs/logs/cleanup_log.json(追加)
```

> ⚠️ **绝对禁止**对 `outputs/reports/` 执行任何删除操作。

**静默执行,不通知用户。**

---

### 任务 4：评论巡检（每 N 小时，仅当 comment_management.enabled = true）

**执行内容**：拉取最近 monitor_days 天发布帖子的新评论，生成摘要推送给用户

**精确执行步骤：**
```
步骤 D1：读取 config.json → comment_management（确认 enabled = true）
步骤 D2：读取 comment_monitor.json（不存在则创建）
         → 获取 last_check 时间戳
步骤 D3：获取最近 monitor_days 天发布的帖子列表：
         → 从 outputs/logs/*_publish_log.json 读取成功发布的 post_id
         → 筛选 published_at 在最近 monitor_days 天内的帖子
步骤 D4：对每个 post_id 执行：
         python3 skills/x2c-socialposter/scripts/x2c_social.py \
           --action comments --post-id {post_id} --platform tiktok
         → 筛选 created_at > last_check 的新评论
         → 应用垃圾过滤（若 auto_filter_spam = true）
步骤 D5：生成评论摘要（模板见下方）
步骤 D6：更新 comment_monitor.json：
         → last_check = 当前时间
         → 更新每个 post 的 last_comment_check 和 total_comments
步骤 D7：将摘要发送给用户
```

**评论摘要模板：**
```markdown
💬 评论巡检报告（{YYYY-MM-DD HH:MM}）

监控范围：最近 {monitor_days} 天发布的 {N} 个帖子
新评论：{N} 条（其中 {N} 条疑似垃圾）

---

🎥 视频 1：{标题}
   发布时间：{YYYY-MM-DD HH:MM} | 平台：TikTok
   新评论：{N} 条
   
   1. @user123（{N}分钟前）："{评论内容}"
      → 回复：reply comment_abc123 你的回复内容
   
   2. @user456（{N}分钟前）："{评论内容}"
      → 回复：reply comment_def456 你的回复内容
   
   3. ⚠️ @spam_bot（{N}分钟前）："点击领取优惠..."
      → 删除：delete comment comment_xyz789

🎥 视频 2：{标题}
   新评论：{N} 条
   ...

---

快捷操作：
• 回复评论：输入 "reply comment_abc123 你的回复内容"
• 删除评论：输入 "delete comment comment_xyz789"
• 查看完整评论：输入 "show comments post_123"
• 在帖子下发评论：输入 "comment on post_123 你的评论内容"
```

**垃圾过滤规则：**
```
若 auto_filter_spam = true：
  → 评论内容包含 spam_keywords 中任何词 → 标记为 "⚠️ 疑似垃圾"
  → 在摘要中显示删除建议
```

**完成后将摘要发送给用户。**

### 任务 4.5：更新 Dashboard 评论数据（评论巡检完成后）

**执行条件**：`config.json` 中 `dashboard.enabled = true`

```
4.5.1：读取 config.json → dashboard（确认 enabled = true）
4.5.2：执行 Dashboard 数据更新：
       python3 skills/tiktok-automator-core/scripts/dashboard_integration.py update
4.5.3：静默执行，不通知用户
```

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
- name: `"Tiktok内容生产({用户配置的时间描述})"`(如"每天14:30"或"每6小时")
- schedule: 根据 production_mode 选择上方对应的 schedule 格式
- payload: `{"kind": "agentTurn", "message": "执行定时完整生产任务:严格按照 AGENTS.md「任务2:完整生产」步骤B1-B6执行。重点:步骤B5数据池重置必须执行,完成后将报告发送给用户。"}`
- sessionTarget: **"current"**
- delivery: `{"mode": "announce"}`

**任务 3：数据清理**
- name: `"历史数据清理（每24小时）"`
- schedule: `{"kind": "every", "everyMs": 86400000}`
- payload: `{"kind": "agentTurn", "message": "执行定时数据清理任务，按 AGENTS.md「任务3：数据清理」步骤C1-C6执行。绝对禁止删除 outputs/reports/ 目录。静默执行。"}`
- sessionTarget: **"current"**
- delivery: `{"mode": "none"}`

**任务 4：评论巡检（仅当 comment_management.enabled = true 时注册）**
- name: `"TikTok评论巡检（每{check_interval_hours}小时）"`
- schedule: `{"kind": "every", "everyMs": check_interval_hours × 3600000}`
- payload: `{"kind": "agentTurn", "message": "执行定时评论巡检任务：按 AGENTS.md「任务4：评论巡检」步骤D1-D6执行，拉取最近 monitor_days 天发布帖子的新评论，生成摘要推送给用户。"}`
- sessionTarget: **"current"**
- delivery: `{"mode": "announce"}`

> ⚠️ sessionTarget 必须为 **"current"**,不能用 "isolated"(isolated 会话无聊天频道,报告推送失败)。

**注册完成后向用户确认:**
```
⏰ 定时任务已设置
📡 轻量采集: 每 1 小时 → 追加热点到数据池(生产后全部重置)
🎬 Tiktok 生产: {用户配置的时间描述} → 取 Top 3 → 生成 3 个视频 → 发布 → 重置数据池
🗑️ 数据清理: 每 24 小时 → 清理 10 天前历史文件(报告永久保留)
💬 评论巡检: 每 {check_interval_hours} 小时 → 拉取最近 {monitor_days} 天帖子新评论 → 推送摘要 ({启用/禁用})

输入 'run now' 可手动立即触发一次完整生产
输入 'show comments' 查看最新评论
```

---

## 流水线执行(7 个阶段)

**触发方式:**
1. **手动**:用户输入 `run now` → 阶段 1-5.5-7 全部执行
2. **定时**:从数据池读取 → 阶段 3-5.5-7

**手动触发时先确认:**
```
🎬 即将启动 Tiktok 内容生产流水线
赛道: [niches]
关键词: [keywords 前5个]
发布平台: Tiktok
预计耗时: 50-60 分钟(含 3 个视频生成 + 间隔发布)
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
平台成功: {N}/18 | 赛道加权: {N} 个平台 | 总收集: {N} 条
→ 进入阶段 2...
```

---

### 阶段 2:智能筛选 → Top 3(含补充搜索)

**执行步骤:**
```
2.1:对阶段 1 收集的热点执行打分和去重
2.2:筛选匹配 keywords 或 niches 的候选热点
2.3:若候选热点 < advanced.min_trends(默认 3)且 supplement_search 启用:
     → 触发补充搜索(步骤 2.4-2.6)
     → 否则跳过补充搜索,直接进入 2.7
2.4:【补充搜索】对每个 keyword 执行 web_search:
     搜索词:"{keyword} 最新 {YYYY-MM-DD}"
     结果数:3-5 条/关键词
2.5:【补充搜索】筛选搜索结果:
     - 排除广告、营销软文(标题含"购买""优惠"等)
     - 提取标题、URL、来源网站
     - 标注 source: "web_search"
2.6:【补充搜索】对搜索结果打分:
     - 命中 keywords → +15 分/词
     - 命中 niches → +10 分
     - 来源是知名媒体(36kr/虎嗅/知乎/少数派等)→ +5 分
     - 合并到候选池
2.7:全局去重后按分数排序,取 Top 3
2.8:写入 outputs/logs/{运行ID}_top3.json
```

**打分公式(热榜来源):**
```
- 标题命中 keywords 中的词 → +15 分/词
- 标题或分类命中 niches → +10 分
- 平台排名前 3 → +10 分;前 5 → +5 分;前 10 → +2 分
- 同一话题跨平台出现 → 每多一个平台 +10 分
- 命中 exclude_keywords → 直接丢弃
```

**打分公式(补充搜索来源):**
```
- 标题命中 keywords → +15 分/词
- 标题命中 niches → +10 分
- 来源是知名媒体 → +5 分
- 命中 exclude_keywords → 直接丢弃
```

**去重**:标题去标点后重叠字符数 / 较短标题字符数 > 0.7 即为重复,保留高分。

**写入** `outputs/logs/{运行ID}_top3.json`

**状态输出(无补充搜索):**
```
📊 阶段 2/7 - 筛选完成
Top 3:
1. {标题} - {分}/100 - {平台} 🔥 | 📌 {命中词}
2. {标题} - {分}/100 - {平台} 🔥 | 📌 {命中词}
3. {标题} - {分}/100 - {平台} 🔥 | 📌 {命中词}
→ 进入阶段 3...
```

**状态输出(触发补充搜索):**
```
📊 阶段 2/7 - 筛选完成
热榜匹配: {N} 条 < 阈值 → 触发补充搜索
🔍 补充搜索: {N} 个关键词 → 找到 {N} 条候选
Top 3:
1. {标题} - {分}/100 - {平台} 🔥 | 📌 {命中词}
2. {标题} - {分}/100 - {平台} 🔥 | 📌 {命中词}
3. {标题} - {分}/100 - 主动搜索 🔍 | 📌 {命中词}
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

### 阶段 4:视频脚本编写

**为 Top 3 的每条热点各编写一个 60 秒 Tiktok 视频脚本(共 3 个脚本)。**

**对 trend1、trend2、trend3 分别执行:**
```
4.1:读取 outputs/briefs/{运行ID}_trend{N}_brief.md
4.2:读取 config.json → content.video_style.project_type
4.3:从映射表获取画面和配乐参数
4.4:读取 config.json → content.language,确定脚本语言
4.4.5:【新增】读取 config.json → content.user_persona.extracted(用户角色、表达风格)
4.4.6:【新增】读取 config.json → content.content_reference.style_analysis(初始文案风格)
4.4.7:【新增】读取 persona_evolution.json(如果存在):
       → 若 production_count >= 5,优先使用 learned.style_fingerprint
       → 读取 user_feedback 中的 applied_changes,覆盖对应字段
       → 若文件不存在,跳过此步
4.5:按模板生成脚本,融入用户风格特征(优先级见下方):
     • 开场钩子采用用户习惯方式(opening_hook)
     • 结构遵循用户常用格式(structure)
     • emoji 和 hashtag 数量参考用户习惯(emoji_usage, hashtag_count)
     • 语气贴合用户 tone(extracted.tone + style_analysis.tone)
     • 优先使用用户常用句式(common_phrases)
4.6:写入 outputs/scripts/{运行ID}_trend{N}_script.md
4.7:【新增】记录本次脚本风格到 persona_evolution.json → style_history:
     {
       "run_id": "{运行ID}",
       "trend_index": {N},
       "opening_hook": "实际使用的开场方式",
       "structure": "实际使用的结构",
       "hashtag_count": 实际数量,
       "emoji_usage": "实际使用位置",
       "tone": "实际语气"
     }
```

**风格数据优先级(从高到低):**
```
1. persona_evolution.json → user_feedback 中的 applied_changes(用户明确调整)
2. persona_evolution.json → style_fingerprint(实际使用习惯,5次生产后生效)
3. config.json → content_reference.style_analysis(初始风格分析)
4. config.json → user_persona.extracted(基础画像)
```

**脚本生成提示词增强:**
```
生成脚本时参考以下用户风格:
- 角色定位:{extracted.role} - {extracted.content_angle}
- 表达风格:{extracted.tone}
- 开场方式:{最高优先级来源的 opening_hook}
- 结构偏好:{最高优先级来源的 structure}
- 语气特点:{最高优先级来源的 tone}
- 常用表达:{style_analysis.common_phrases}
- hashtag 风格:{style_analysis.hashtag_style},数量 {最高优先级来源的 hashtag_count}
- emoji 使用:{最高优先级来源的 emoji_usage}
```

**⚠️ 脚本语言规则(必须严格执行):**

| config.json `content.language` | 脚本旁白语言 | Giggle API language 参数 |
|------|------|------|
| `zh-CN` | 全中文 | `zh` |
| `en` | 全英文 | `en` |
| `bilingual` | 旁白写英文(主语言),中文作括号补充关键词 | `en` |

规则说明:
- Giggle 根据旁白文本语言生成对应语音和字幕。**旁白文本语言 ≠ 视频语言,会导致声音与字幕不匹配。**
- `bilingual` 模式:旁白主体用英文写,发布文案(Tiktok caption)用中文写,实现"英文视频+中文配文"的双语效果。
- Tiktok 发布文案(caption)**始终用中文写**,无论语言设置如何。

**赛道→视频风格映射表:**

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

**脚本模板:**
```markdown
# 视频脚本 - {标题}

**来源**:{平台} | **赛道**:{赛道} | **时长**:60秒 | **风格**:{风格名}
**脚本语言**:{zh-CN→中文 / en→英文 / bilingual→英文旁白+中文文案}

## 视频生成参数
- project_type: {值}
- aspect: 9:16
- duration: 60
- language: {zh 或 en,根据 content.language 决定}

## 【0-5秒】钩子
**旁白**:> "{改写自提炼卡核心观点,语言见上方规则}"
**画面**:{描述}

## 【5-25秒】冲突展开
**旁白**:> "{来自提炼卡事件概要+关键数据}"
**画面**:{描述}

## 【25-45秒】反转/深度
**旁白**:> "{来自提炼卡多角度分析}"
**画面**:{描述}

## 【45-55秒】核心观点
**旁白**:> "{来自提炼卡核心观点}"
**画面**:{描述}

## 【55-60秒】CTA
**旁白**:> "{结尾提问+关注引导,与旁白同语言}"
**画面**:{关注引导}

## Tiktok 发布文案(始终用中文)
**正文**: {150-300字 + emoji + 8-12个 #标签,中文}
```

**状态输出:**
```
🎬 阶段 4/7 - 脚本完成
1. {标题} | {风格名} ({project_type}) | 60秒 ✅
2. {标题} | {风格名} ({project_type}) | 60秒 ✅
3. {标题} | {风格名} ({project_type}) | 60秒 ✅
→ 进入阶段 5...
```

---

### 阶段 5:视频生成

**⚠️ 关键要求:必须循环自动生成 3 个视频,不得中断等待用户确认**

**⚠️ 绝对禁止的行为:**
1. **禁止擅自终止视频生成**:即使耗时较长(每个 8-12 分钟),也必须等待所有 3 个视频全部完成
2. **禁止跳过视频 2 和 3**:必须生成所有 3 个视频,不得因为时间问题跳过
3. **禁止假设任务超时**:定时任务没有硬性超时限制,即使总耗时 30-40 分钟也必须完成
4. **禁止主动 kill 进程**:不得使用 `process kill` 终止视频生成进程

**正确的执行方式:**
- 使用 `for` 循环依次生成 3 个视频
- 每个视频使用 `process poll` 等待完成,`timeout` 设为 900000 (15 分钟)
- 如果单个视频超时,记录错误并继续下一个,但不得跳过所有视频

**为 3 个脚本分别生成视频(共 3 个视频)。使用 for 循环对 trend1、trend2、trend3 依次执行:**

```python
# 伪代码示例(实际执行时用真实代码)
for N in [1, 2, 3]:
    # 5.1:读取脚本
    script = read(f"outputs/scripts/{运行ID}_trend{N}_script.md")
    
    # 5.2:提取旁白
    narrations = extract_narrations(script)
    
    # 5.3:提取 project_type
    project_type = extract_project_type(script)
    
    # 5.4:读取 API Key
    giggle_api_key = config['credentials']['giggle_api_key']
    
    # 5.5:调用 Giggle API
    result = call_giggle_api(narrations, project_type, N)
    
    # 5.6:等待完成(使用 process poll,timeout=600000)
    wait_until_complete()
    
    # 5.7:下载视频
    download_video(result, f"outputs/videos/{运行ID}_trend{N}_video.mp4")
    
    # ⚠️ 不停止,直接继续下一个视频
```

**详细步骤(每个视频):**
```
5.1:读取 outputs/scripts/{运行ID}_trend{N}_script.md
5.2:提取所有旁白(> "..." 引用块),拼接为完整文本
5.3:提取 project_type
5.4:从 config.json 读取 giggle_api_key
5.5:执行 Giggle API 调用(代码见下方)
5.6:等待完成(每个 8-12 分钟,使用 process poll)
5.7:下载视频到 outputs/videos/{运行ID}_trend{N}_video.mp4
5.8:⚠️ 立即继续下一个视频,不等待用户确认
```

**⚠️ 关键执行约束(防止延迟):**
```
1. 使用 exec background 启动视频生成后,必须使用 process poll 等待完成
2. poll 的 timeout 设置为 900000 (15分钟),但不要一直等待 timeout
3. 正确的做法:
   → 启动进程后,立即调用 process poll(timeout=900000)
   → poll 会在进程完成时立即返回(不会等待 timeout)
   → 检查返回的 exit code,如果为 0 表示成功
   → 立即提取下载链接并下载视频
   → 不要再次调用 poll 或等待,直接继续下一个视频

4. 错误的做法(会导致延迟):
   ❌ 启动进程后,使用 poll 但不检查返回结果
   ❌ 进程完成后,继续等待或再次调用 poll
   ❌ 使用固定的 sleep 等待时间

5. 验证方法:
   → 检查 process log,确认视频生成完成的时间
   → 确保在完成后 1 分钟内启动下一个视频生成
```

**Giggle API 调用代码(对每个 trend 执行一次,替换 {N} 和对应文本):**
```python
import sys, os, json

skill_path = os.path.join(os.getcwd(), "skills/giggle-generation-drama/scripts")
if not os.path.exists(skill_path):
    skill_path = os.path.expanduser("~/.openclaw/skills/giggle-generation-drama/scripts")
sys.path.insert(0, skill_path)
os.environ["GIGGLE_API_KEY"] = "{giggle_api_key}"

# 语言映射:从 config.json 的 content.language 读取
# bilingual → "en"(双语内容以英文生成,旁白更国际化)
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

> 💡 **语言映射规则**:
> - `zh-CN` → Giggle `zh`(中文旁白和字幕)
> - `en` → Giggle `en`(英文旁白和字幕)
> - `bilingual`(双语)→ Giggle `en`(英文视频,配合中文发布文案实现双语效果)

**结果**:`result['data']['download_url']` 或 `result['data']['video_asset']['signed_url']`

**下载**:`curl -s -L -m 300 -o outputs/videos/{运行ID}_trend{N}_video.mp4 "{url}"`

**失败处理**:单个视频重试 1 次,仍失败则跳过该视频,继续生成下一个,报告中标注。

**状态输出:**
```
🎬 阶段 5/7 - 视频生成完成
1. {标题} - {N}秒 | {N}MB ✅
2. {标题} - {N}秒 | {N}MB ✅
3. {标题} - {N}秒 | {N}MB ✅(或 ❌ 失败已跳过)
→ 进入阶段 5.5(压缩检查)...
```

---

### 阶段 5.5:视频压缩(发布前自动执行)

**目的**:X2C 发布 API 的请求超时为 60 秒,大文件视频(>50MB)容易超时导致发布失败。此阶段在发布前自动检测并压缩超大视频。

**触发规则**:对每个已生成的视频文件执行判断:
- **≤ 45MB**:不压缩,直接跳过
- **> 45MB**:使用 ffmpeg 压缩到 ≤ 45MB(留 5MB 余量,目标 50MB 以下)

**⚠️ ffmpeg 路径**:系统未安装全局 ffmpeg,必须使用 imageio_ffmpeg 绑定的二进制:
```python
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
```

**精确执行步骤(对 trend1、trend2、trend3 分别执行):**

```python
import os, subprocess, json
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
MAX_SIZE_MB = 45  # 压缩目标(MB),留余量确保 < 50MB

def compress_video(input_path):
    """检查视频大小,超过阈值则压缩。返回最终文件路径。"""
    file_size_mb = os.path.getsize(input_path) / (1024 * 1024)

    if file_size_mb <= MAX_SIZE_MB:
        print(f"✅ {os.path.basename(input_path)}: {file_size_mb:.1f}MB ≤ {MAX_SIZE_MB}MB,无需压缩")
        return input_path

    print(f"⚠️ {os.path.basename(input_path)}: {file_size_mb:.1f}MB > {MAX_SIZE_MB}MB,开始压缩...")

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

    # Step 2: 计算目标码率(kbps)
    # 目标大小(KB) = MAX_SIZE_MB * 1024
    # 目标码率 = 目标大小(kbit) / 时长(s) - 音频码率(128kbps)
    target_total_bitrate = (MAX_SIZE_MB * 1024 * 8) / duration_sec  # kbps
    audio_bitrate = 128  # kbps
    video_bitrate = int(target_total_bitrate - audio_bitrate)
    video_bitrate = max(video_bitrate, 500)  # 最低 500kbps 保证画质

    # Step 3: 两遍压缩(单遍即可满足需求)
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
        # 压缩成功,用压缩文件替换原文件
        os.replace(compressed_path, input_path)
        print(f"✅ 压缩完成: {file_size_mb:.1f}MB → {compressed_size_mb:.1f}MB")
        return input_path
    else:
        # 压缩后仍然太大,清理临时文件
        os.remove(compressed_path)
        print(f"⚠️ 压缩后仍 {compressed_size_mb:.1f}MB,保留原文件")
        return input_path

# 对 3 个视频分别执行
for n in [1, 2, 3]:
    video_path = f"outputs/videos/{{运行ID}}_trend{n}_video.mp4"
    if os.path.exists(video_path):
        compress_video(video_path)
```

**状态输出:**
```
📦 阶段 5.5 - 视频压缩检查
1. {标题} - {原始}MB → {压缩后}MB ✅(或 "无需压缩")
2. {标题} - {原始}MB → {压缩后}MB ✅(或 "无需压缩")
3. {标题} - {原始}MB → {压缩后}MB ✅(或 "无需压缩")
→ 进入阶段 6...
```

---

### 阶段 6:Tiktok 发布

**⚠️ 关键要求:必须循环自动发布 3 个视频,每个间隔 10 分钟,不得中断等待用户确认**

**将 3 个视频依次发布到 Tiktok,每个视频之间间隔 10 分钟。使用 for 循环执行:**

```python
# 伪代码示例(实际执行时用真实代码)
# 步骤 6.1-6.2:检查 Tiktok 关联状态(只执行一次)
export X2C_API_KEY="{x2c_api_key}"
check_tiktok_status()  # 确认已关联

# 步骤 6.3-6.10:循环发布 3 个视频
for N in [1, 2, 3]:
    # 提取发布文案
    caption = extract_caption(f"outputs/scripts/{运行ID}_trend{N}_script.md")
    
    # 发布视频
    result = publish_to_tiktok(
        caption=caption,
        video_file=f"outputs/videos/{运行ID}_trend{N}_video.mp4"
    )
    
    # 记录结果
    record_publish_result(N, result)
    
    # 启动后台首评任务(不阻塞)
    if auto_first_comment_enabled:
        start_background_comment_task(N, result['post_id'])
    
    # ⚠️ 间隔 10 分钟(仅在前两个视频后)
    if N < 3:
        sleep(600)  # 10 分钟
    
    # ⚠️ 不停止,直接继续下一个视频

# 步骤 6.11:关闭 DailyHotApi 服务
bash skills/dailyhot-api/scripts/stop.sh
```

**详细步骤:**
```
6.1:export X2C_API_KEY="{x2c_api_key}"
6.2:python3 skills/x2c-socialposter/scripts/x2c_social.py --action status
     → 确认 Tiktok 已关联,否则暂停通知用户
6.3:循环开始 - 对 trend1, trend2, trend3 依次执行:
   6.3.1:提取发布文案
   6.3.2:发布视频(命令见下方)
   6.3.3:记录临时 Post ID
   6.3.4:启动后台首评任务(不阻塞主流程)
   6.3.5:如果不是最后一个视频,等待 10 分钟(sleep 600)
   6.3.6:⚠️ 立即继续下一个视频,不等待用户确认
6.4:循环结束
6.5:⚠️ 生成发布日志 outputs/logs/{runID}_publish_log.json(必须执行)
6.6:bash skills/dailyhot-api/scripts/stop.sh
```

> ⚠️ **间隔规则**:每发布一个视频后,必须等待 10 分钟再发布下一个。用 `sleep 600` 或等效方式实现。如果某个视频在阶段 5 生成失败,跳过该视频的发布,但仍然等待 10 分钟后再发布下一个。

> ⚠️ **发布日志必须生成**:步骤 6.5 必须执行,否则 Dashboard 无法统计视频数量。日志格式见下方。

**Tiktok 发布命令(对每个视频执行一次,替换 {N}):**
```bash
python3 skills/x2c-socialposter/scripts/x2c_social.py \
  --action publish \
  --platforms Tiktok \
  --post "{trend{N} 脚本中 Tiktok 发布文案的正文}" \
  --media-files "outputs/videos/{运行ID}_trend{N}_video.mp4"
```

**结果处理:**
- `success: true` → 记录 post_id ✅
- `success: false` / 401 → 暂停,通知用户重新授权
- 400 → 记录错误 ❌,继续发布下一个

**后台首评任务启动(仅当 auto_first_comment.enabled = true):**
```bash
# 读取发布结果,提取 temp_post_id、trend_title 和 publish_time
temp_post_id=$(echo "$publish_result" | jq -r '.posts[0].tikTokId')
trend_title=$(cat outputs/logs/{runID}_top3.json | jq -r '.[{N-1}].title')
publish_time=$(date -Iseconds)  # 当前时间，ISO 8601 格式

# 后台启动首评任务(不等待)
# ⚠️ 注意:必须传递 publish_time 参数,用于智能等待
nohup python3 skills/tiktok-automator-core/scripts/auto_first_comment.py \
  "$temp_post_id" "{N}" "$trend_title" "$publish_time" \
  > outputs/logs/auto_comment_trend{N}.log 2>&1 &

echo "🤖 后台首评任务已启动(trend{N})"
```

> 💡 **智能等待机制**:
> - 脚本会根据发布时间智能计算等待时间
> - 如果已过 30 分钟,立即开始检查
> - 否则等待到 30 分钟后开始检查
> - 每 2 分钟检查一次,最多等待 35 分钟

**发布日志格式(outputs/logs/{runID}_publish_log.json):**
```json
{
  "run_id": "{runID}",
  "production_time": "{ISO8601时间}",
  "trends": [
    {
      "title": "{trend1标题}",
      "platform": "{trend1平台}",
      "tiktok_post_id": "{Post ID}",
      "tiktok_id": "{TikTok ID}",
      "status": "success",
      "publish_time": "{ISO8601时间}",
      "video_file": "outputs/videos/{runID}_trend1_video.mp4"
    },
    {
      "title": "{trend2标题}",
      "platform": "{trend2平台}",
      "tiktok_post_id": "{Post ID}",
      "tiktok_id": "{TikTok ID}",
      "status": "success",
      "publish_time": "{ISO8601时间}",
      "video_file": "outputs/videos/{runID}_trend2_video.mp4"
    },
    {
      "title": "{trend3标题}",
      "platform": "{trend3平台}",
      "tiktok_post_id": "{Post ID}",
      "tiktok_id": "{TikTok ID}",
      "status": "success",
      "publish_time": "{ISO8601时间}",
      "video_file": "outputs/videos/{runID}_trend3_video.mp4"
    }
  ]
}
```

> ⚠️ **重要**:此文件必须生成,Dashboard 依赖它来统计视频数量和显示最近发布的视频。

**状态输出:**
```
📲 阶段 6/7 - Tiktok 发布完成
1. {标题} - ✅ Post ID: {id}
   🤖 后台首评任务已启动(预计 30-40 分钟后完成)
   ⏳ 等待 10 分钟...
2. {标题} - ✅ Post ID: {id}
   🤖 后台首评任务已启动(预计 30-40 分钟后完成)
   ⏳ 等待 10 分钟...
3. {标题} - ✅ Post ID: {id}
   🤖 后台首评任务已启动(预计 30-40 分钟后完成)
→ 进入阶段 7...

⚠️ 注意:自动首评任务在后台执行中,不影响报告生成。
完成后会记录到 outputs/logs/auto_comment_YYYYMMDD.json
失败会通知用户。
```

---

### 阶段 7:汇总报告与画像进化

```
7.0:【新增】检查自动首评失败通知:
     → python3 skills/tiktok-automator-core/scripts/check_comment_failures.py
     → 若有失败,将通知消息附加到报告末尾

7.1:生成 JSON 日志 → outputs/logs/{运行ID}_publish_log.json
7.2:生成报告 → outputs/reports/{运行ID}_内容产出报告.md

7.3:【新增】画像进化处理(B + D 机制):
     → 读取 persona_evolution.json(不存在则创建)
     → 统计本次 3 个脚本的 style_history:
        • 开场方式使用频次
        • 结构类型使用频次
        • 平均 hashtag 数量
        • emoji 使用位置
        • 语气分布
     → 更新 production_count += 1
     → 若 production_count % 5 == 0:
        • 归纳 style_fingerprint(取最高频特征)
        • 检查风格重复预警:
          - 某种开场连续 >= 10 次 → 触发 "opening_repetition" 预警
          - 某种结构连续 >= 8 次 → 触发 "structure_repetition" 预警
        • 检查用户反馈频次:
          - 连续 3 次 "adjust_style" → 触发 "style_mismatch" 预警
     → 将预警写入 warnings(status: active)
     → 保存 persona_evolution.json

7.4:将报告内容发送给用户(含反馈收集部分)

7.5:【新增】等待用户反馈(机制 C):
     → 报告末尾展示反馈选项
     → 用户回复后:
        • a(满意)→ 记录到 user_feedback,权重 +1
        • b(选题问题)→ 解析描述,更新 keywords/niches,写回 config.json(告知用户)
        • c(风格调整)→ 解析描述,更新 style_analysis,写回 config.json(告知用户)
        • d(跳过)→ 不记录
     → 若用户 24 小时内无回复,视为跳过
```

**报告模板:**
```markdown
# 📋 Tiktok 内容产出报告

> 🎬 Tiktok-自媒体运营 · v5
> 📅 {日期时间}
> ⏱ 总耗时:约 {N} 分钟

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
| 1 | {标题} | {分}/100 | {平台} 🔥 |
| 2 | {标题} | {分}/100 | {平台} 🔥 |
| 3 | {标题} | {分}/100 | {平台/主动搜索} 🔥/🔍 |

---

## 📰 热点提炼卡

### 热点 1:{标题}
{完整嵌入 trend1_brief.md}

### 热点 2:{标题}
{完整嵌入 trend2_brief.md}

### 热点 3:{标题}
{完整嵌入 trend3_brief.md}

---

## 🎬 视频(3 个)

### 视频 1:{标题}
| 项目 | 详情 |
|------|------|
| 时长 | {N}秒 |
| 风格 | {风格名} |
| 项目ID | {id} |
| 文件 | outputs/videos/{运行ID}_trend1_video.mp4 |

**Tiktok 发布文案:**
{完整嵌入}

### 视频 2:{标题}
| 项目 | 详情 |
|------|------|
| 时长 | {N}秒 |
| 风格 | {风格名} |
| 项目ID | {id} |
| 文件 | outputs/videos/{运行ID}_trend2_video.mp4 |

**Tiktok 发布文案:**
{完整嵌入}

### 视频 3:{标题}
| 项目 | 详情 |
|------|------|
| 时长 | {N}秒 |
| 风格 | {风格名} |
| 项目ID | {id} |
| 文件 | outputs/videos/{运行ID}_trend3_video.mp4 |

**Tiktok 发布文案:**
{完整嵌入}

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

## 📊 内容质量反馈(可选)

本次生产已完成,如果你有任何想法,可以直接回复:

- **a** - 满意,继续这个方向
- **b** - 热点选题不太对,我更希望看到 ___(请补充)
- **c** - 脚本风格需要调整,具体是 ___(请补充)
- **d** - 跳过

你的反馈会帮助我持续优化内容质量。

---
> 🤖 Tiktok-自媒体运营 v5 自动生成
```

**规则**:报告自包含,提炼卡和发布文案完整嵌入。生成后必须发送给用户。

### 阶段 7.5：更新 Dashboard（若已启用）

**执行条件**：`config.json` 中 `dashboard.enabled = true`

```
7.5.1：读取 config.json → dashboard（确认 enabled = true）
7.5.2：执行 Dashboard 数据更新：
       python3 skills/tiktok-automator-core/scripts/dashboard_integration.py update
       → 更新全部 8 个组件（KPI 卡、趋势图、帖子表、评论表、统计行）
       → 失败：静默失败，不影响报告发送
7.5.3：若更新成功，在报告中附加一行：
       "📊 Dashboard 已更新：{config.dashboard.public_url}"
```

---

## 已加载的技能

| 技能 | 功能 | 阶段 | 依赖 |
|------|------|------|------|
| `dailyhot-api` | 40+ 平台热榜聚合 | 阶段 1 | Node.js ≥ 20 |
| `giggle-generation-drama` | Giggle API 视频生成 | 阶段 5 | Giggle API Key |
| `x2c-socialposter` | Tiktok 视频发布 | 阶段 6 | X2C API Key |
| `claw-dashboard` | 可视化数据面板 | 阶段 7.5 | 无(自动安装) |

---

## 权限边界

- **工作区**:`~/.openclaw/workspace-Tiktok-drama-trend-automator/`
- **输出目录**:`outputs/{briefs,scripts,videos,reports,logs,pool}/`
- **禁止**:写入工作区外的任何路径

---

## 会话启动行为

**0. 检查技能依赖**
```
→ 检查 skills/ 目录下是否存在：
   - dailyhot-api/
   - giggle-generation-drama/
   - x2c-socialposter/
   - claw-dashboard/
→ 若缺失任何技能：
   提示用户：
   "⚠️ 缺少必要技能：{skill_name}
   请执行：openclaw skills install {skill_name}
   安装完成后重新启动。"
   → 暂停继续

→ 若 claw-dashboard 存在，额外检查 pip 包：
   python3 skills/tiktok-automator-core/scripts/dashboard_integration.py check
   → need_pip = true：自动安装：python3 skills/tiktok-automator-core/scripts/dashboard_integration.py install_pip
```

**1. 检查 `config.json`**

**2. 不存在** → 展示配置检查清单 → 配置向导

**3. 存在但不完整** → 检查缺失字段 → 补充配置
```
必需字段检查清单：
- credentials.giggle_api_key
- credentials.x2c_api_key
- content.user_persona
- content.content_focus
- content.video_style
- content.language
- schedule.timezone
- schedule.production_mode
- comment_management.enabled
- auto_first_comment.enabled
- dashboard.enabled

若任何必需字段缺失：
→ 提示用户："⚠️ 配置不完整，缺少：{field_name}。现在补充配置。"
→ 跳转到对应步骤补充
```

**4. 存在且完整** → 执行以下步骤:

   **4.1 检查 persona_evolution.json 预警:**
   ```
   → 读取 persona_evolution.json
   → 若存在 status == "active" 的 warnings:
      展示给用户:
      ┌─────────────────────────────────────────────────────────────┐
      │ ⚠️ 风格优化建议                                              │
      │                                                             │
      │ {warning.message}                                           │
      │                                                             │
      │ 你可以选择:                                                 │
      │ • 输入 'ignore warning' 忽略并继续                          │
      │ • 输入 'update persona' 更新画像                            │
      │ • 输入 'add sample' 提供新的文案样本                        │
      │ • 输入 'run now' 直接开始生产(使用当前风格)               │
      └─────────────────────────────────────────────────────────────┘
   → 若无预警,继续显示摘要
   ```

   **4.2 显示摘要:**
   ```
   🎬 Tiktok 自媒体运营 - 就绪
   赛道:{niches}
   关键词:{keywords 前5个}
   Tiktok:@{handle}

   ⏰ 定时任务:
     📡 轻量采集: 每 1 小时 - {状态}
     🎬 Tiktok 生产: {用户配置的时间描述} - {状态}(生产后自动重置数据池)
     🗑️ 数据清理: 每 24 小时 - {状态}
     💬 评论巡检: 每 {check_interval_hours} 小时 - {启用/禁用}

   📊 Dashboard: {已启用 → 显示 URL | 未启用 → 输入 'setup dashboard' 搞建}

   📊 今日数据池: {N} 条采集 | {N} 条未使用
   🕐 上次数据池重置: {last_production_reset 或 "从未生产"}
   📈 累计生产次数: {production_count}
   🎨 风格指纹: {若 production_count >= 5,展示 style_fingerprint 摘要}

   可用命令:
   • 'run now' - 手动触发完整生产
   • 'show persona' - 查看完整用户画像
   • 'show evolution' - 查看风格学习数据
   • 'update persona' - 更新用户画像
   • 'add sample' - 添加文案样本
   • 'reset evolution' - 重置学习数据
   • 'show comments' - 查看最新评论
   • 'setup dashboard' - 搞建可视化面板
   • 'show dashboard' - 显示 Dashboard 地址
   ```

---

## 用户交互命令

### `show persona`
展示当前完整的用户画像和学习数据摘要。

**输出内容:**
```
👤 用户画像
━━━━━━━━━━━━━━━━━━━━
• 角色: {extracted.role}
• 背景: {extracted.background}
• 内容定位: {extracted.content_angle}
• 表达风格: {extracted.tone}

👥 受众画像
━━━━━━━━━━━━━━━━━━━━
• 描述: {extracted.audience.description}
• 关注点: {extracted.audience.concerns}
• 需要避免: {extracted.audience.avoid}

📝 初始文案风格(首次配置)
━━━━━━━━━━━━━━━━━━━━
• 开场方式: {style_analysis.opening_hook}
• 结构偏好: {style_analysis.structure}
• 语气特点: {style_analysis.tone}
• 常用表达: {style_analysis.common_phrases}

📈 累计生产次数: {production_count}

可用命令: 'update persona' | 'show evolution'
```

### `show evolution`
展示 `persona_evolution.json` 的完整学习数据。

**输出内容:**
```
📊 风格学习数据
━━━━━━━━━━━━━━━━━━━━
• 累计生产: {production_count} 次
• 风格历史记录: {style_history.length} 条

🎨 当前风格指纹(每5次更新)
━━━━━━━━━━━━━━━━━━━━
• 主导开场: {style_fingerprint.dominant_opening}
• 主导结构: {style_fingerprint.dominant_structure}
• 平均 hashtag: {style_fingerprint.avg_hashtag_count}
• emoji 使用: {style_fingerprint.dominant_emoji_usage}
• 语气分布: {style_fingerprint.tone_distribution}

⚠️ 活跃预警: {warnings.length} 条
{预警列表}

💬 最近反馈: {user_feedback.length} 条
{最近3条反馈}

可用命令: 'reset evolution' | 'add sample'
```

### `update persona`
重新引导用户输入自我介绍,更新用户画像。

**流程:**
```
1. 展示当前画像
2. 询问:"请重新介绍你自己(或输入 '取消' 保持现状)"
3. 用户输入新描述 → AI 重新提取画像
4. 展示新旧对比,询问是否确认更新
5. 确认后写回 config.json → content.user_persona
6. 同时清空 persona_evolution.json 中的 style_fingerprint(建议保留 style_history)
```

### `add sample`
引导用户提供新的文案样本,追加到参考库并重新分析风格。

**流程:**
```
1. 询问:"请粘贴 1-3 段你满意的文案样本(输入 '完成' 结束)"
2. 用户可多次输入,每次追加到 content_reference.samples
3. 收集完成后,重新分析全部样本,更新 style_analysis
4. 展示新旧风格对比
5. 确认后写回 config.json → content_reference.style_analysis
```

### `reset evolution`
清除学习数据,从头开始风格学习。

**流程:**
```
1. 确认:"确定要清除所有风格学习数据吗?这将重置 production_count 和 style_fingerprint,但保留 config.json 中的基础配置。(是/否)"
2. 确认后:
   - 清空 persona_evolution.json 中的 learned.style_history
   - 清空 learned.style_fingerprint
   - 清空 user_feedback
   - 清空 warnings
   - production_count 重置为 0
   - last_updated 更新
```

### `ignore warning`
忽略当前的活跃预警。

**流程:**
```
→ 将所有 status == "active" 的 warnings 标记为 "ignored"
→ 提示:"预警已忽略,下次生产将正常进行"
```

---

### `setup auto-comment`
配置自动首评功能。

**执行:**
```bash
python3 skills/tiktok-automator-core/scripts/configure_auto_comment.py
```

**说明:**
- 视频发布后自动等待 30 分钟获取真实 TikTok 视频 ID
- 获取成功后自动发布首条评论
- 失败会通知用户

### `show auto-comment status`
查看自动首评配置和最近执行状态。

**执行:**
```bash
cat config.json | jq '.auto_first_comment'
ls -la outputs/logs/auto_comment*.json
```

### `check comment failures`
手动检查自动首评失败通知。

**执行:**
```bash
python3 skills/tiktok-automator-core/scripts/check_comment_failures.py
```

## 评论管理命令

### `show comments <post_id>`
查看指定帖子的所有评论。

**执行:**
```bash
python3 skills/x2c-socialposter/scripts/x2c_social.py \
  --action comments --post-id {post_id} --platform tiktok
```

**输出格式:**
```
💬 帖子评论：{标题}
总评论数：{N} 条

1. @user123（{N}分钟前）："{评论内容}"
   comment_id: comment_abc123

2. @user456（{N}分钟前）："{评论内容}"
   comment_id: comment_def456

...
```

### `recent posts`
查看最近发布的帖子列表。

**执行:**
```
→ 读取 outputs/logs/*_publish_log.json
→ 按时间排序，展示最近 10 个帖子
```

**输出格式:**
```
📱 最近发布的帖子

1. {标题} | {YYYY-MM-DD HH:MM} | TikTok
   post_id: post_123
   → 查看评论: show comments post_123

2. {标题} | {YYYY-MM-DD HH:MM} | TikTok
   post_id: post_456
   → 查看评论: show comments post_456

...
```

### `reply <comment_id> <内容>`
回复特定评论。

**执行:**
```bash
python3 skills/x2c-socialposter/scripts/x2c_social.py \
  --action reply --comment-id {comment_id} --platforms tiktok --comment "你的回复内容"
```

**示例:**
```
用户: "reply comment_abc123 谢谢你的支持！🙏"
Agent: → 执行回复
        → 返回: "✅ 已回复评论 comment_abc123"
```

### `delete comment <comment_id>`
删除指定评论。

**执行:**
```bash
python3 skills/x2c-socialposter/scripts/x2c_social.py \
  --action delete-comment --comment-id {comment_id}
```

**示例:**
```
用户: "delete comment comment_xyz789"
Agent: → 执行删除
        → 返回: "✅ 已删除评论 comment_xyz789"
```

### `comment on <post_id> <内容>`
在指定帖子下发评论。

**执行:**
```bash
python3 skills/x2c-socialposter/scripts/x2c_social.py \
  --action comment --post-id {post_id} --platforms tiktok --comment "你的评论内容"
```

**示例:**
```
用户: "comment on post_123 感谢大家的支持！🙏"
Agent: → 执行发评论
        → 返回: "✅ 已在帖子 post_123 下发评论"
```

---

## Dashboard 命令

### `setup dashboard`
首次搞建可视化面板（使用 claw-dashboard）。

**执行流程:**
```
1. python3 skills/tiktok-automator-core/scripts/dashboard_integration.py check
2. python3 skills/tiktok-automator-core/scripts/dashboard_integration.py setup
3. 告知用户公网地址
```

### `show dashboard`
显示 Dashboard 文件路径。

**执行:**
```
→ 读取 config.json → dashboard.file
→ 若 enabled = false：提示用户输入 'setup dashboard'
→ 若 enabled = true：返回 "📊 Dashboard 路径：{file}
   用浏览器打开即可查看。"
```

### `update dashboard`
手动刷新 Dashboard 数据。

**执行:**
```
python3 skills/tiktok-automator-core/scripts/dashboard_integration.py update
→ 成功："✅ Dashboard 已更新"
→ 失败：提示错误原因
```

### `remove dashboard`
移除 Dashboard（需确认）。

**执行:**
```
1. 确认："确定要移除 Dashboard 吗？(是/否)"
2. 确认后：
   → 将 config.json 中 dashboard.enabled 设为 false
   → 删除 outputs/dashboard/ 目录
   → 提示用户已移除
```

| 错误 | 阶段 | 处理 |
|------|------|------|
| DailyHotApi 启动失败 | 1 | 检查 Node.js,重新 ensure_running.sh |
| 平台采集 500 | 1 | 跳过该平台,继续其他 |
| 热榜匹配 < 阈值 | 2 | 触发补充搜索,用 web_search 补充候选 |
| 补充搜索无结果 | 2 | 记录警告,用现有候选继续 |
| Top 3 不足 | 2 | 有多少用多少,最少 1 条 |
| web_search 无结果 | 3 | 换关键词重新搜索 |
| Giggle API 超时 | 5 | 重试 1 次,仍失败跳过 |
| Giggle 余额不足 | 5 | 暂停,通知用户充值 |
| ffmpeg 压缩失败 | 5.5 | 保留原始文件,继续发布(可能超时) |
| 压缩后仍超 50MB | 5.5 | 保留压缩文件,继续发布 |
| X2C 发布超时 | 6 | 重试 1 次,仍失败记录错误 |
| X2C 401 | 6 | 暂停,通知用户重新授权 |
| X2C 400 | 6 | 记录错误 |
| 数据池为空 | B1 | 先执行一次轻量采集 |
| 数据池不足 3 条 | B4 | 有多少用多少 |
| 清理误删 reports/ | 清理 | 绝对禁止,find 命令不含 reports 路径 |
| outputs/ 目录不存在 | 清理 | 跳过该目录,继续其他,不报错 |
| Dashboard 安装失败 | 配置 | 检查网络,重试 dashboard_setup() |
| Dashboard 服务未运行 | 更新 | 静默失败,不影响报告发送 |
| Dashboard 更新失败 | 7.5/4.5 | 静默失败,不影响主流程 |
