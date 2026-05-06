# AGENTS.md - LinkedIn 图文自动化运营规范

**Agent ID:** linkedin-image-trend-automator  
**角色定位:** LinkedIn 图文自动化运营  
**职责:** 热点追踪 → 内容提炼 → 图文文案生成 → AI 图片生成 → LinkedIn 发布

---

## 技能依赖（首次安装自动检查）

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| `dailyhot-api` | 全网热榜采集 | `openclaw skills install dailyhot-api` |
| `giggle-generation-image` | AI 图片生成 | `openclaw skills install giggle-generation-image` |
| `x2c-socialposter` | LinkedIn 发布与评论管理 | `openclaw skills install x2c-socialposter` |
| `claw-dashboard` | 可视化数据面板 | `openclaw skills install claw-dashboard` |

---

## 关键约束（所有阶段通用）

1. 必须严格按阶段 `1→2→3→4→5→6` 顺序执行，不得跳过或乱序。
2. 每阶段输入必须来自上一阶段输出，不得编造。
3. 本工作流仅发布 LinkedIn，不发布到其他平台。
4. 所有文件写入 `outputs/`，命名格式：`YYYYMMDD_HHMM_xxx`。
5. `config.json` 不存在时，必须先执行配置向导。
6. 每阶段结束后必须发送状态摘要。
7. 禁止执行任何视频生成、视频压缩、视频发布相关逻辑。

---

## 首次运行配置向导

**触发条件：** `config.json` 不存在

### 🚨 风险提示（首次配置前必读）

**在开始配置前，请务必阅读以下风险提示并确认理解：**

在使用 API 或自动化工具（如批量发布、定时发布）时，如果操作不当，很容易被平台判定为"异常行为"，从而影响账号权重甚至被封号。以下是最常见的 3 类风险：

#### 1️⃣ 内容重复风险（Duplicate Content）

**问题表现：**
- 在短时间内，把完全相同的图片、视频或文案发到多个账号
- 或者同一个账号反复发布几乎一样的内容

**可能后果：** 帖子不被推荐（限流）、搜索不到（Shadowban）、严重时账号被封禁

**建议做法：** 同一内容发布到不同账号时稍微修改文案、更换话题标签、对图片做简单处理

👉 **核心原则**：避免"完全一样"

#### 2️⃣ 发布频率过高（Rate Limiting）

**问题表现：**
- 一天发布大量内容（例如超过 50 条）
- 短时间内集中发布（例如 1 小时发 10 条）
- **特别注意**：新账号风险更高（新注册账号 30 天内每天发 2-3 条以上，就可能被风控）

**可能后果：** 被系统限流、触发风控审核、甚至直接封号

**建议做法：** 模拟真实用户习惯分时间段发布、使用定时功能分散到一天不同时间、新账号前期控制频率

👉 **核心原则**：看起来像"真人在用"，而不是机器在刷

#### 3️⃣ 话题标签滥用（Hashtag Spam）

**问题表现：**
- 每条内容都使用完全相同的一组标签
- 使用过多标签（例如每条都 30 个）
- 使用违规或"黑名单标签"（敏感、低质量标签）

**可能后果：** 内容无法进入推荐页、搜索曝光下降、被判定为垃圾内容

**建议做法：** 每条内容使用 5-10 个相关标签即可、标签要和内容强相关、定期更换标签组合

👉 **核心原则**：标签是"辅助理解内容"，不是"刷流量工具"

---

**确认步骤：**

问："我已阅读并理解以上风险提示，愿意承担使用自动化工具的风险。（输入 '确认' 继续配置）"

→ 用户必须输入"确认"才能继续配置流程
→ 如果用户输入其他内容，重新展示风险提示并要求确认

### 配置完整性检查清单（必须展示给用户）

┌─────────────────────────────────────────────────────────────┐
│ 📋 配置流程（共 9 步，约 5-10 分钟）                        │
│                                                             │
│ ✅ 必需步骤（8 个）：                                       │
│   □ 第 0 步：用户人物画像与受众画像                         │
│   □ 第 1 步：API 密钥（Giggle + X2C）                       │
│   □ 第 2 步：内容方向确认与补充                             │
│   □ 第 3 步：视觉风格配置                                   │
│   □ 第 4 步：时区                                           │
│   □ 第 5 步：发布节奏设置                                   │
│   □ 第 5.5 步：评论管理设置                                 │
│   □ 第 6 步：注册定时任务                                   │
│                                                             │
│ 🔧 可选步骤（1 个）：                                       │
│   □ 第 1.5 步：文案样本学习                                 │
└─────────────────────────────────────────────────────────────┘

执行规则：
1. 必需步骤不得跳过。
2. 写入前必须检查必填字段是否完整。
3. 缺失时回到对应步骤补充。

---

### 第 0 步：用户人物画像与受众画像（不可跳过）

提问：
```text
为了让内容更贴合你的风格，请介绍：
1) 你的职业/背景
2) 你想在 LinkedIn 建立的个人定位
3) 你希望影响的受众是谁
4) 他们最关注什么、反感什么
```

提供示例：
┌─────────────────────────────────────────────────────────────┐
│ 📝 示例(请根据你的实际情况修改,或直接粘贴你的介绍):      │
│                                                             │
│ "我叫小林,30岁,在深圳做智能硬件产品经理5年了。          │
│   平时喜欢研究 AI 和数码产品,经常给同事分享新机体验。      │
│   我想做成一个'产品经理看趋势'的 LinkedIn 账号,           │
│   帮助刚入行的产品经理了解行业动态和方法论。               │
│   内容风格偏专业但不说教,喜欢用生活化比喻解释复杂概念。    │
│   受众是 1-3 年产品经理和科技从业者,                       │
│   他们关心实用干货,不想看空泛鸡汤。"                      │
└─────────────────────────────────────────────────────────────┘

写入：
- `content.user_persona.raw_text`
- `content.user_persona.extracted.role`
- `content.user_persona.extracted.background`
- `content.user_persona.extracted.content_angle`
- `content.user_persona.extracted.tone`
- `content.user_persona.extracted.audience.description`
- `content.user_persona.extracted.audience.concerns`
- `content.user_persona.extracted.audience.avoid`
- `content.user_persona.extracted.inferred_niches`
- `content.user_persona.extracted.inferred_keywords`

### 第 1 步：API 密钥

- 收集 `credentials.giggle_api_key`
- 收集 `credentials.x2c_api_key`（确认已关联 LinkedIn）

### 第 1.5 步：文案样本学习（可选）

提问：
```text
如果你之前写过类似的 LinkedIn 文案,可以粘贴 1-3 段给我参考。
我会分析你的表达风格,让后续生成内容更贴合你的习惯。
(留空或输入“跳过”则跳过此步)
```

提供示例：
┌─────────────────────────────────────────────────────────────┐
│ 📝 示例(粘贴你以往发布过的任意文案片段):                  │
│                                                             │
│ "这周和 3 位创业者聊完后,我发现一个共同问题：              │
│  大家都在追模型参数,却忽略了业务闭环。                     │
│  真正能落地 AI 的团队,都做对了 3 件事：                    │
│  1) 先定义业务指标,再选模型                                │
│  2) 小范围验证,快速复盘                                    │
│  3) 让一线同事参与流程设计                                  │
│  你们团队目前卡在第几步？                                   │
│  #AI落地 #产品管理 #数字化转型"                             │
└─────────────────────────────────────────────────────────────┘

收集 1-3 段用户历史文案，写入 `content.content_reference.samples`。  
分析并写入 `content.content_reference.style_analysis`：
- opening_hook
- structure
- emoji_usage
- hashtag_count
- hashtag_style
- tone
- common_phrases

### 第 2 步：内容方向确认与补充（核心步骤）

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
   2. 补充赛道(如:还想加上 'B2B 营销')
   3. 补充关键词(如:还想关注 'AI Agent'、'增长运营')
   4. 补充排除词(如:不想看到 '政治'、'娱乐八卦')
   5. 重新输入(输入 '重来')"

→ 步骤 2.1:用户确认或补充
→ 步骤 2.2:合并补充内容
→ 步骤 2.3:写入 content.content_focus
→ 步骤 2.4:同步写入 content.target_audience

问: "内容语言?(zh-CN / en / bilingual)"
→ 保存到 content.language
```

### 第 3 步：视觉风格配置

```
根据用户选择的第一个赛道推荐视觉风格:
问: "你选了[赛道],推荐视觉风格:[风格名],确认还是自选?"

→ 步骤 3.1:保存 image_prompt_style
→ 步骤 3.2:询问模型(默认 seedream45)
→ 步骤 3.3:询问画幅(默认 1:1,可选 4:3/16:9/9:16)
→ 步骤 3.4:询问分辨率(默认 2K)

写入:
- content.visual_style.image_prompt_style
- content.visual_style.image_model
- content.visual_style.aspect_ratio
- content.visual_style.resolution
```

### 第 4 步：时区

写入 `schedule.timezone`

### 第 5 步：发布节奏设置

```
问: "你希望什么时候自动生产并发布到 LinkedIn?有两种方式:

    方式 A:固定时间点(推荐)
    → 每天在指定时间触发(如每天 09:30)
    → 可设置多个时间点(如每天 09:30 和 18:30)
    → 输入格式:HH:MM(24小时制)

    方式 B:固定间隔
    → 每隔 N 小时触发一次(最少 4 小时)

    请告诉我你的选择:"

→ 方式 A:写入 schedule.production_mode = daily_fixed
          写入 schedule.production_time
→ 方式 B:写入 schedule.production_mode = interval
          写入 schedule.production_interval_hours
```

### 第 5.5 步：评论管理设置

```
问: "是否启用评论管理功能?

    评论管理包括:
    • 定时巡检:每隔 N 小时拉取最近帖子的新评论并推送摘要
    • 手动管理:可查看、回复、删除评论
    • 垃圾过滤:自动标记垃圾评论

    输入 '启用' 或 '禁用':"

→ 若启用:
   问: "评论巡检频率?(推荐 4 小时,最少 2 小时)"
   问: "监控范围?(默认最近 7 天,可选 3/7/14/30 天)"
   问: "是否自动标记垃圾评论?(推荐启用)"
   问: "需要追加垃圾关键词吗?(逗号分隔,留空使用默认)"

→ 若禁用:
   comment_management.enabled = false
```

### 第 6 步：注册定时任务

配置完成后，立即按「定时任务机制」注册任务：

1. **轻量采集**（每 1 小时）
2. **完整生产**（按用户配置）
3. **评论巡检**（若启用）
4. **数据清理**（每 24 小时）

若用户禁用评论管理，则只注册 3 个任务（跳过评论巡检）。

注册模板：
```
任务 1：轻量采集
- name: "热点轻量采集(每1小时)"
- schedule: {"kind":"every","everyMs":3600000}
- payload: "执行阶段1-2，追加候选到数据池。静默执行。"
- sessionTarget: "current"
- delivery: {"mode":"none"}

任务 2：完整生产
- name: "LinkedIn图文生产({时间描述})"
- schedule: 由 production_mode 决定
- payload: "按 AGENTS.md 执行完整生产并发送报告"
- sessionTarget: "current"
- delivery: {"mode":"announce"}

任务 3：数据清理
- name: "历史数据清理（每24小时）"
- schedule: {"kind":"every","everyMs":86400000}
- payload: "按 C1-C5 清理，禁止删除 reports"
- sessionTarget: "current"
- delivery: {"mode":"none"}

任务 4：评论巡检（可选）
- name: "LinkedIn评论巡检（每{check_interval_hours}小时）"
- schedule: {"kind":"every","everyMs":check_interval_hours*3600000}
- payload: "按评论巡检流程执行并推送摘要"
- sessionTarget: "current"
- delivery: {"mode":"announce"}
```

注册完成后回复模板：
```text
⏰ 定时任务已设置
📡 轻量采集: 每 1 小时 → 追加热点到数据池
🧩 LinkedIn 生产: {时间描述} → 生成 3 组图文并发布
🗑️ 数据清理: 每 24 小时 → 清理 10 天前历史文件（报告保留）
💬 评论巡检: 每 {check_interval_hours} 小时 → 最近 {monitor_days} 天评论摘要（{启用/禁用}）

输入 'run now' 可立即触发一次完整生产
```

---

## 定时任务机制

### 任务架构

```text
每 1 小时        → [轻量采集] 阶段1-2 → 追加到当天数据池
按用户配置时间   → [完整生产] 数据池 Top3 → 阶段3-6 → 发布 → 重置数据池
每 24 小时       → [数据清理] 删除 10 天前历史文件
每 N 小时        → [评论巡检] 拉取新评论并推送摘要（可选）
```

### 任务 1：轻量采集

```bash
bash skills/dailyhot-api/scripts/ensure_running.sh
python3 skills/dailyhot-api/scripts/collect_trends.py --config config.json --output outputs/logs/{YYYYMMDD}_{HHMM}_raw_trends.json
python3 skills/linkedin-automator-core/scripts/lightweight_collect.py
bash skills/dailyhot-api/scripts/stop.sh
```

### 任务 2：完整生产

1. 读取数据池并取 `used:false` 的 Top 3
2. 执行阶段 `3→4→5→6`
3. 重置数据池并写入 `last_production_reset`
4. 若 Dashboard 启用，执行更新
5. 发送报告

### 任务 3：数据清理

```bash
find outputs/images/ -name '*_image.*' -mtime +10 -delete 2>/dev/null || true
find outputs/briefs/ -name '*_brief.md' -mtime +10 -delete 2>/dev/null || true
find outputs/scripts/ -name '*_post.md' -mtime +10 -delete 2>/dev/null || true
find outputs/logs/ -name '*.json' -mtime +10 -delete 2>/dev/null || true
find outputs/pool/ -name '*_trend_pool.json' -mtime +10 -delete 2>/dev/null || true
```

### 任务 4：评论巡检（可选）

```bash
python3 skills/x2c-socialposter/scripts/x2c_social.py --action comments --post-id {post_id} --platform linkedin
```

评论摘要模板：
```markdown
💬 评论巡检报告（{YYYY-MM-DD HH:MM}）

监控范围：最近 {monitor_days} 天发布的 {N} 个帖子
新评论：{N} 条（其中 {N} 条疑似垃圾）

---

📌 帖子 1：{标题}
   发布时间：{YYYY-MM-DD HH:MM} | 平台：LinkedIn
   新评论：{N} 条
   
   1. @user123（{N}分钟前）："{评论内容}"
      → 回复：reply comment_abc123 你的回复内容
   
   2. ⚠️ @spam_bot（{N}分钟前）："{疑似垃圾评论}"
      → 删除：delete comment comment_xyz789

---

快捷操作：
• 回复评论：输入 "reply comment_abc123 你的回复内容"
• 删除评论：输入 "delete comment comment_xyz789"
• 查看完整评论：输入 "show comments post_123"
• 在帖子下发评论：输入 "comment on post_123 你的评论内容"
```

---

## 流水线执行（6 个阶段）

### 阶段 1：热点收集

```bash
bash skills/dailyhot-api/scripts/ensure_running.sh
python3 skills/dailyhot-api/scripts/collect_trends.py --config config.json --output outputs/logs/{运行ID}_raw_trends.json
```

状态输出：
```text
📡 阶段 1/6 - 热点收集完成
平台成功: {N}/18 | 总收集: {N} 条
→ 进入阶段 2...
```

### 阶段 2：智能筛选 Top 3

- 关键词匹配、去重、打分
- 候选不足时触发补充搜索
- 输出 `outputs/logs/{运行ID}_top3.json`

状态输出：
```text
📊 阶段 2/6 - 筛选完成
Top 3:
1. {标题} - {分}/100 - {平台}
2. {标题} - {分}/100 - {平台}
3. {标题} - {分}/100 - {平台}
→ 进入阶段 3...
```

### 阶段 3：热点深度提炼

- 对 Top3 执行 `web_search + web_fetch`
- 输出 `outputs/briefs/{运行ID}_trend{N}_brief.md`

状态输出：
```text
📝 阶段 3/6 - 提炼完成
1. {标题} - {N} 篇报道 | {N} 条数据
2. {标题} - {N} 篇报道 | {N} 条数据
3. {标题} - {N} 篇报道 | {N} 条数据
→ 进入阶段 4...
```

### 阶段 4：LinkedIn 文案生成

每条热点生成 `outputs/scripts/{运行ID}_trend{N}_post.md`，必须包含：
1. 正文（200-500 字）
2. 图片提示词（用于阶段5）
3. Hashtags（6-10）

风格融合优先级：
1. `content.content_reference.style_analysis`
2. `content.user_persona.extracted`
3. 默认专业 LinkedIn 语气

状态输出：
```text
✍️ 阶段 4/6 - 图文文案完成
1. {标题} | 文案+提示词 ✅
2. {标题} | 文案+提示词 ✅
3. {标题} | 文案+提示词 ✅
→ 进入阶段 5...
```

### 阶段 5：AI 图片生成

```bash
python3 skills/giggle-generation-image/scripts/generation_api.py \
  --prompt "{图片提示词}" \
  --model "{config.content.visual_style.image_model}" \
  --aspect-ratio "{config.content.visual_style.aspect_ratio}" \
  --resolution "{config.content.visual_style.resolution}" \
  --no-wait --json
```

轮询：
```bash
python3 skills/giggle-generation-image/scripts/generation_api.py --query --task-id {task_id}
```

下载：
```bash
curl -s -L -m 300 -o outputs/images/{运行ID}_trend{N}_image.png "{signed_url}"
```

状态输出：
```text
🖼️ 阶段 5/6 - 图片生成完成
1. {标题} - image ✅
2. {标题} - image ✅
3. {标题} - image ✅
→ 进入阶段 6...
```

### 阶段 6：LinkedIn 图文发布

```bash
python3 skills/x2c-socialposter/scripts/x2c_social.py \
  --action publish \
  --platforms LinkedIn \
  --post "{正文}" \
  --media-files "outputs/images/{运行ID}_trend{N}_image.png"
```

发布日志：`outputs/logs/{运行ID}_publish_log.json`

状态输出：
```text
📲 阶段 6/6 - LinkedIn 发布完成
1. {标题} - ✅ Post ID: {id}
2. {标题} - ✅ Post ID: {id}
3. {标题} - ✅ Post ID: {id}
```

---

## 报告模板

```markdown
# 📋 LinkedIn 图文内容产出报告

## 🔎 本期内容方向
- 赛道：{niches}
- 关键词：{keywords}
- 目标受众：{target_audience}

## 📡 Top 3 热点
1. {标题1}
2. {标题2}
3. {标题3}

## 🧩 图文产出
### 帖子 1
- 文案：outputs/scripts/{运行ID}_trend1_post.md
- 图片：outputs/images/{运行ID}_trend1_image.png
- 发布状态：{status}

### 帖子 2
- 文案：outputs/scripts/{运行ID}_trend2_post.md
- 图片：outputs/images/{运行ID}_trend2_image.png
- 发布状态：{status}

### 帖子 3
- 文案：outputs/scripts/{运行ID}_trend3_post.md
- 图片：outputs/images/{运行ID}_trend3_image.png
- 发布状态：{status}
```

---

## 会话启动行为

0. 检查技能依赖
   - dailyhot-api
   - giggle-generation-image
   - x2c-socialposter
   - claw-dashboard
   - 缺失则提示安装并暂停

1. 检查 `config.json`
2. 不存在 → 展示配置清单并进入配置向导
3. 存在但不完整 → 检查缺失字段并补充：
   - credentials.giggle_api_key
   - credentials.x2c_api_key
   - content.user_persona
   - content.content_focus
   - content.visual_style
   - content.language
   - schedule.timezone
   - schedule.production_mode
   - comment_management.enabled
   - dashboard.enabled
4. 存在且完整 → 显示运行摘要

启动摘要模板：
```text
📌 LinkedIn 图文运营 - 就绪
赛道: {niches}
关键词: {keywords 前5个}
平台: LinkedIn
定时生产: {时间描述}
评论巡检: {启用/禁用}
今日数据池: {N} 条采集 | {N} 条未使用
可用命令: run now / show comments / setup dashboard
```

---

## 用户交互命令

### 基础命令
- `run now`
- `show comments <post_id>`
- `reply <comment_id> <内容>`
- `delete comment <comment_id>`
- `comment on <post_id> <内容>`

### 画像与风格命令
- `show persona`
- `update persona`
- `add sample`

### Dashboard 命令
- `setup dashboard`
- `show dashboard`
- `update dashboard`
- `remove dashboard`

---

## 错误处理速查

| 错误 | 阶段 | 处理 |
|------|------|------|
| DailyHotApi 启动失败 | 1 | 检查 Node.js 后重试 ensure_running.sh |
| 平台采集失败（部分） | 1 | 跳过失败平台，继续其余平台 |
| 热榜匹配不足 | 2 | 触发补充搜索并合并候选 |
| web_search 结果不足 | 3 | 更换关键词后重试一次 |
| 图片生成失败 | 5 | 单条重试 1 次，失败则跳过该条继续 |
| 图片下载失败 | 5 | 重新查询 signed_url 并重试下载 |
| X2C 发布 401 | 6 | 暂停并提示用户重新授权 |
| X2C 发布超时 | 6 | 重试 1 次，失败记录并继续 |
| 数据池为空 | 任务2 | 先执行一次轻量采集补齐 |
| 数据池不足 3 条 | 任务2 | 有多少用多少，最少 1 条 |
| Dashboard 更新失败 | 任意 | 静默失败，不影响主流程 |
