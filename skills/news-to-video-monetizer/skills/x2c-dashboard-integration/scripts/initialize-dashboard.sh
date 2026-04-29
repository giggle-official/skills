#!/bin/bash
# initialize-dashboard.sh - 初始化 Dashboard Hub
set -e

echo "🎬 初始化 Dashboard Hub..."

# 检查是否已初始化
if [ -d ~/.claw/hub ] && [ -f ~/.claw/config/tunnel.json ]; then
  echo "✅ Dashboard 已初始化"
  
  # 检查服务状态
  if ! pgrep -f "uvicorn app:app" > /dev/null; then
    echo "  → 启动 Hub 服务..."
    cd ~/.claw/hub && nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 3000 > ~/.claw/hub.log 2>&1 &
    sleep 2
  fi
  
  if ! pgrep -f "cloudflared tunnel" > /dev/null; then
    echo "  → 启动 Tunnel 服务..."
    TUNNEL_TOKEN=$(python3 -c "import json,os; print(json.load(open(os.path.expanduser('~/.claw/config/tunnel.json')))['tunnel_token'])")
    nohup cloudflared tunnel run --token "$TUNNEL_TOKEN" > ~/.claw/tunnel.log 2>&1 &
    sleep 2
  fi
  
  exit 0
fi

# 1. 安装 Python 依赖
echo "  → 安装 Python 依赖..."
pip3 install -q fastapi uvicorn jinja2 httpx

# 2. 创建目录结构
echo "  → 创建目录结构..."
mkdir -p ~/.claw/{hub,config,shared}

# 3. 复制 Hub 应用
echo "  → 复制 Hub 应用..."
cp -R ~/.openclaw/skills/claw-dashboard-skill/hub-app/* ~/.claw/hub/

# 4. 初始化数据库
echo "  → 初始化数据库..."
python3 << 'EOF'
import sqlite3, os
os.makedirs(os.path.expanduser('~/.claw/shared'), exist_ok=True)
db = sqlite3.connect(os.path.expanduser('~/.claw/shared/shared.db'))
db.executescript('''
    CREATE TABLE IF NOT EXISTS dashboard_modules (
        id TEXT PRIMARY KEY, agent_id TEXT NOT NULL, name TEXT NOT NULL,
        icon TEXT DEFAULT '📊', config TEXT DEFAULT '{}',
        created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS dashboard_widgets (
        id TEXT PRIMARY KEY, module_id TEXT NOT NULL, widget_type TEXT NOT NULL,
        title TEXT NOT NULL, config TEXT DEFAULT '{}', data TEXT DEFAULT '[]',
        position INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS dashboard_kv (
        namespace TEXT NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL,
        updated_at TEXT DEFAULT (datetime('now')), PRIMARY KEY (namespace, key)
    );
''')
db.commit()
print('✅ Database initialized')
EOF

# 5. 注册设备
echo "  → 注册设备..."
SERIAL=$(echo "DEMO$(date +%s)" | tail -c 13)
curl -s -X POST https://api.clawln.app/devices/register \
  -H "Content-Type: application/json" \
  -d "{\"serial\": \"$SERIAL\"}" > ~/.claw/config/tunnel.json

# 6. 安装 cloudflared
if ! command -v cloudflared &> /dev/null; then
  echo "  → 安装 cloudflared..."
  wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -O /usr/local/bin/cloudflared
  chmod +x /usr/local/bin/cloudflared
fi

# 7. 启动 Hub 服务
echo "  → 启动 Hub 服务..."
cd ~/.claw/hub && nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 3000 > ~/.claw/hub.log 2>&1 &
sleep 2

# 8. 启动 Tunnel
echo "  → 启动 Tunnel..."
TUNNEL_TOKEN=$(python3 -c "import json,os; print(json.load(open(os.path.expanduser('~/.claw/config/tunnel.json')))['tunnel_token'])")
nohup cloudflared tunnel run --token "$TUNNEL_TOKEN" > ~/.claw/tunnel.log 2>&1 &
sleep 2

echo "✅ Dashboard Hub 初始化完成"

# 显示 URL
PUBLIC_URL=$(python3 -c "import json,os; print(json.load(open(os.path.expanduser('~/.claw/config/tunnel.json')))['public_url'])")
echo "📊 Dashboard URL: $PUBLIC_URL"
