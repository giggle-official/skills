# X2C Dashboard Integration Guide

## 快速开始

### 1. 安装 skill

```bash
openclaw skills add https://github.com/YOUR_USERNAME/x2c-dashboard-integration
```

或手动安装：

```bash
cd ~/.openclaw/skills
git clone https://github.com/YOUR_USERNAME/x2c-dashboard-integration.git
```

### 2. 首次初始化

```bash
# 安装依赖
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/install-dependencies.sh

# 初始化 Dashboard
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/initialize-dashboard.sh

# 注册模块
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/register-module.sh \
  news-to-video-monetizer "X2CReel 制作发行" "🎬"
```

### 3. 更新数据

```bash
export X2C_API_KEY="your_x2c_api_key"
python3 ~/.openclaw/skills/x2c-dashboard-integration/scripts/update_dashboard.py
```

### 4. 获取 URL

```bash
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/get-url.sh
```

---

## 在 Agent 中集成

### AGENTS.md 示例

```markdown
## Dashboard 可视化面板

### 首次使用

当用户说"查看 Dashboard"时，执行：

\`\`\`bash
# 1. 安装依赖
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/install-dependencies.sh

# 2. 初始化
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/initialize-dashboard.sh

# 3. 注册模块
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/register-module.sh \
  news-to-video-monetizer "X2CReel 制作发行" "🎬"

# 4. 更新数据
X2C_API_KEY="$API_KEY" python3 ~/.openclaw/skills/x2c-dashboard-integration/scripts/update_dashboard.py

# 5. 获取 URL
bash ~/.openclaw/skills/x2c-dashboard-integration/scripts/get-url.sh
\`\`\`

### 后续使用

只需更新数据：

\`\`\`bash
X2C_API_KEY="$API_KEY" python3 ~/.openclaw/skills/x2c-dashboard-integration/scripts/update_dashboard.py
\`\`\`
```

---

## 故障排查

### Hub 未运行

```bash
cd ~/.claw/hub && python3 -m uvicorn app:app --host 0.0.0.0 --port 3000 &
```

### Tunnel 未运行

```bash
TUNNEL_TOKEN=$(python3 -c "import json,os; print(json.load(open(os.path.expanduser('~/.claw/config/tunnel.json')))['tunnel_token'])")
cloudflared tunnel run --token "$TUNNEL_TOKEN" &
```

### 查看日志

```bash
tail -f ~/.claw/hub.log
tail -f ~/.claw/tunnel.log
```

---

## 自定义

### 修改模块信息

编辑 `register-module.sh` 中的参数：

```bash
AGENT_ID="your-agent-id"
NAME="Your Agent Name"
ICON="🚀"
```

### 添加自定义组件

修改 `update_dashboard.py`，添加新的 widget 类型。

---

## 许可

MIT License
