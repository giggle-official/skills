---
name: x2c-dashboard-integration
description: Complete X2C Dashboard integration for news-to-video-monetizer agent. Auto-installs dependencies (claw-dashboard-skill), initializes Hub, registers modules, and provides data update scripts. API key is automatically loaded from workspace config.json.
version: 1.0.0
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["python3","curl","git"]}}}
---

# x2c-dashboard-integration

**一站式 X2C Dashboard 集成方案**

为 `news-to-video-monetizer` agent 提供完整的可视化 Dashboard 支持，包括：
- 自动安装依赖 skills
- 初始化 Dashboard Hub
- 注册模块和组件
- 实时数据更新

---

## 功能

### 1. 自动安装依赖

```bash
bash {baseDir}/scripts/install-dependencies.sh
```

自动安装：
- `x2c-real-dashboard` — 数据源
- `claw-dashboard-skill` — Dashboard 框架

### 2. 初始化 Dashboard

```bash
bash {baseDir}/scripts/initialize-dashboard.sh
```

执行：
- 安装 Python 依赖（fastapi、uvicorn、jinja2、httpx）
- 创建目录结构（`~/.claw/hub`、`~/.claw/shared`、`~/.claw/config`）
- 初始化 SQLite 数据库
- 注册设备并获取 Cloudflared tunnel
- 启动 Hub 和 Tunnel 服务

### 3. 注册模块

```bash
bash {baseDir}/scripts/register-module.sh news-to-video-monetizer "X2CReel 制作发行" "🎬"
```

参数：
- `agent_id`: Agent 标识符
- `name`: 显示名称
- `icon`: Emoji 图标

### 4. 部署自定义模板（Tab 切换功能）

```bash
bash {baseDir}/scripts/deploy-templates.sh
```

部署自定义 Dashboard 模板，包含：
- Tab 切换功能（Agent 运行面板 / X2C Dashboard）
- Widget 分类和渲染
- 自动重启 Hub 服务

### 5. 更新数据

```bash
X2C_API_KEY="your_key" bash {baseDir}/scripts/update-data.sh
```

或使用 Python 脚本：

```bash
X2C_API_KEY="your_key" python3 {baseDir}/scripts/update_dashboard.py
```

### 5. 获取 Dashboard URL

```bash
bash {baseDir}/scripts/get-url.sh
```

---

## 使用流程

### 首次使用

```bash
# 1. 安装依赖
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/install-dependencies.sh

# 2. 初始化 Dashboard
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/initialize-dashboard.sh

# 3. 注册模块
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/register-module.sh \
  news-to-video-monetizer "X2CReel 制作发行" "🎬"

# 4. 更新数据
X2C_API_KEY="your_key" python3 ~/.openclaw/skills/x2c-dashboard-integration/scripts/update_dashboard.py

# 5. 获取 URL
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/get-url.sh
```

### 后续使用

只需更新数据：

```bash
X2C_API_KEY="your_key" python3 ~/.openclaw/skills/x2c-dashboard-integration/scripts/update_dashboard.py
```

---

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `X2C_API_KEY` | ✅ | X2C API Key（格式：`x2c_sk_xxx`）|

---

## 目录结构

```
x2c-dashboard-integration/
├── SKILL.md                      # 本文件
├── scripts/
│   ├── install-dependencies.sh   # 安装依赖 skills
│   ├── initialize-dashboard.sh   # 初始化 Dashboard Hub
│   ├── register-module.sh        # 注册 agent 模块
│   ├── update_dashboard.py       # 更新数据（Python）
│   ├── update-data.sh            # 更新数据（Bash 包装器）
│   └── get-url.sh                # 获取 Dashboard URL
└── docs/
    └── INTEGRATION.md            # 集成指南
```

---

## 错误处理

所有脚本在失败时返回非零退出码，并输出错误信息到 stderr。

检查状态：

```bash
# 检查 Hub 是否运行
pgrep -f "uvicorn app:app" > /dev/null && echo "✅ Hub running" || echo "❌ Hub not running"

# 检查 Tunnel 是否运行
pgrep -f "cloudflared tunnel" > /dev/null && echo "✅ Tunnel running" || echo "❌ Tunnel not running"

# 检查数据库
[ -f ~/.claw/shared/shared.db ] && echo "✅ Database exists" || echo "❌ Database missing"
```

---

## 依赖

- **系统依赖**: Python 3.8+, curl, git, wget
- **Python 依赖**: fastapi, uvicorn, jinja2, httpx
- **Skills**: x2c-real-dashboard, claw-dashboard-skill

---

## 许可

MIT License
