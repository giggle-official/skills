# x2c-dashboard-integration

**一站式 X2C Dashboard 集成方案**

为 `news-to-video-monetizer` agent 提供完整的可视化 Dashboard 支持。

## 功能

- ✅ 自动安装依赖 skills（x2c-real-dashboard、claw-dashboard-skill）
- ✅ 初始化 Dashboard Hub（FastAPI + SQLite + Cloudflared）
- ✅ 注册 agent 模块和组件
- ✅ 实时数据更新（KPI、图表、表格）
- ✅ 公共 URL 访问

## 快速开始

```bash
# 1. 安装 skill
cd ~/.openclaw/skills
git clone https://github.com/YOUR_USERNAME/x2c-dashboard-integration.git

# 2. 安装依赖
bash x2c-dashboard-integration/scripts/install-dependencies.sh

# 3. 初始化 Dashboard
bash x2c-dashboard-integration/scripts/initialize-dashboard.sh

# 4. 注册模块
bash x2c-dashboard-integration/scripts/register-module.sh \
  news-to-video-monetizer "X2CReel 制作发行" "🎬"

# 5. 更新数据
X2C_API_KEY="your_key" python3 x2c-dashboard-integration/scripts/update_dashboard.py

# 6. 获取 URL
bash x2c-dashboard-integration/scripts/get-url.sh
```

## 文档

- [SKILL.md](SKILL.md) — 完整功能说明
- [docs/INTEGRATION.md](docs/INTEGRATION.md) — 集成指南

## 依赖

- Python 3.8+
- curl, git, wget
- x2c-real-dashboard skill
- claw-dashboard-skill

## 许可

MIT License
