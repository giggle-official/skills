# YouTube Automator - 全自动 YouTube 内容运营系统

**最自律的 YouTube 内容机器** — 它比你早起，追踪全网热点，深度提炼，写脚本拍视频，自动发 YouTube。你只管看播放量涨。

---

## 🎯 核心功能

### 📡 全网热点追踪
- 自动抓取 40+ 平台热搜（抖音、微博、知乎、B站、百度、今日头条等）
- 按你设定的赛道和关键词智能过滤
- 每小时自动采集，确保热点新鲜度

### 📝 热点深度提炼
- 对 Top 3 热点进行背景调研
- 提取关键数据、多角度观点、行业影响分析
- 输出结构化「热点提炼卡」

### 🎬 人设化视频生成
- 根据你的人设和受众画像编写 60 秒短视频脚本
- 通过 Giggle API 自动渲染高质量视频
- 支持 9 个赛道风格（科技、娱乐、美食等）

### 📲 YouTube 全流程管理
- 自动发布视频到 YouTube
- 自动首评（可选）
- 评论巡检（可选）
- 完整报告推送

### 📊 可视化数据面板
- 实时数据监控
- 趋势分析
- 内容回顾

---

## 🚀 快速开始

### 前置要求

- Python 3.8+
- Node.js 16+（用于 DailyHotApi）
- OpenClaw 已安装

### 1. 安装技能依赖

```bash
openclaw skills install dailyhot-api
openclaw skills install giggle-generation-drama
openclaw skills install x2c-socialposter
openclaw skills install claw-dashboard
```

### 2. 首次配置

运行首次配置向导，系统会引导你完成 11 个配置步骤：

```bash
# 在 OpenClaw 中对话
"开始配置 YouTube Automator"
```

**配置步骤包括：**
1. 用户画像与受众分析
2. API 密钥（Giggle + X2C）
3. 文案参考库（可选）
4. 内容方向确认
5. 视频风格
6. 时区
7. 发布节奏
8. 评论管理设置
9. 自动首评设置
10. 注册定时任务
11. Dashboard 设置（可选）

### 3. 获取 API 密钥

**Giggle API Key**（视频生成）：
1. 访问 https://giggle.pro
2. 注册/登录账号
3. 进入账号设置 → API Key
4. 复制 API Key

**X2C API Key**（YouTube 发布）：
1. 访问 https://www.x2creel.ai
2. 注册/登录账号
3. 关联 YouTube 账号
4. 获取 Developer API Key

### 4. 验证安装

```bash
# 测试轻量采集
bash skills/dailyhot-api/scripts/ensure_running.sh
python3 skills/dailyhot-api/scripts/collect_trends.py \
  --config config.json \
  --output outputs/logs/$(date +%Y%m%d_%H%M)_raw_trends.json
python3 skills/youtube-automator-core/scripts/lightweight_collect.py
bash skills/dailyhot-api/scripts/stop.sh

# 检查数据池
python3 << 'EOF'
import json
with open('outputs/pool/$(date +%Y%m%d)_trend_pool.json', 'r') as f:
    pool = json.load(f)
unused = sum(1 for c in pool['collections'] for t in c['trends'] if not t['used'])
print(f"✅ 数据池未使用条目: {unused}")
EOF
```

### 5. 设置 Dashboard（可选）

```bash
python3 skills/youtube-automator-core/scripts/setup_dashboard.py
```

---

## 📋 运行方式

### 自动运行（推荐）

配置完成后，系统会自动运行：

- **轻量采集**：每 1 小时采集热点，写入数据池
- **定时生产**：按你设定的时间自动生产 3 个视频并发布
- **数据清理**：每 24 小时清理 10 天前的历史文件
- **评论巡检**：每 N 小时检查新评论（可选）

### 手动触发

```bash
# 在 OpenClaw 中对话
"run now"
```

---

## 📂 目录结构

```
youtube-automator/
├── AGENTS.md                    # 操作规范（核心文档）
├── config.json                  # 配置文件（首次运行后生成）
├── config.template.json         # 配置模板
├── TROUBLESHOOTING.md           # 故障排查指南
├── DEPLOYMENT_CHECKLIST.md      # 部署检查清单
├── skills/
│   ├── dailyhot-api/            # 热点采集技能
│   ├── giggle-generation-drama/ # 视频生成技能
│   ├── x2c-socialposter/        # YouTube 发布技能
│   ├── claw-dashboard/          # Dashboard 技能
│   └── youtube-automator-core/   # 核心脚本
│       └── scripts/
│           ├── lightweight_collect.py      # 轻量采集脚本
│           ├── setup_dashboard.py          # Dashboard 设置脚本
│           └── dashboard_integration.py    # Dashboard 集成脚本
└── outputs/
    ├── briefs/                  # 热点提炼卡
    ├── scripts/                 # 视频脚本
    ├── videos/                  # 生成的视频
    ├── logs/                    # 运行日志
    ├── pool/                    # 热点数据池
    └── reports/                 # 生产报告
```

---

## 🔧 常见问题

### 1. 轻量采集追加 0 条热点

**原因**：数据结构解析错误

**解决**：使用专用脚本 `lightweight_collect.py`

详见 [TROUBLESHOOTING.md](TROUBLESHOOTING.md#问题-1轻量采集任务追加-0-条热点)

### 2. 视频生成被跳过

**原因**：Agent 擅自终止视频生成

**解决**：已在 AGENTS.md 中添加严格约束，禁止跳过视频

详见 [TROUBLESHOOTING.md](TROUBLESHOOTING.md#问题-2视频生成被擅自跳过)

### 3. Dashboard 显示 Error 1033

**原因**：Hub 服务未运行或配置不完整

**解决**：运行 `setup_dashboard.py`

详见 [TROUBLESHOOTING.md](TROUBLESHOOTING.md#问题-3dashboard-显示-error-1033)

---

## 📊 Dashboard

访问 Dashboard 查看运营数据：

- **公网地址**：`https://device-xxx.clawln.app`
- **本地地址**：`http://localhost:3000`

**⚠️ 重要提示**：Dashboard 需要等第一次内容生产完成后才会显示数据。

---

## 🛠️ 高级配置

### 调整热点来源

编辑 `config.json`：

```json
{
  "trend_sources": {
    "primary": ["36kr", "huxiu", "ithome", "juejin", "sspai", "zhihu"],
    "secondary": ["bilibili", "douyin", "weibo"],
    "top_per_platform": 10
  }
}
```

### 调整视频时长

编辑 `config.json`：

```json
{
  "advanced": {
    "video_duration": 30
  }
}
```

### 调整发布节奏

编辑 `config.json`：

```json
{
  "schedule": {
    "production_mode": "daily_fixed",
    "production_time": ["9:00", "18:00"]
  }
}
```

---

## 📖 文档

- [AGENTS.md](AGENTS.md) - 完整的操作规范
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 故障排查指南
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - 部署检查清单

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [DailyHotApi](https://github.com/imsyy/DailyHotApi) - 全网热榜 API
- [Giggle.pro](https://giggle.pro) - AI 视频生成
- [X2C Reel](https://www.x2creel.ai) - 社交媒体发布
- [OpenClaw](https://openclaw.ai) - AI Agent 平台

---

**最后更新**：2026-04-24
