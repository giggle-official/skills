#!/bin/bash
# DailyHotApi 服务管理脚本 — 确保服务运行
# 安装时自动部署，用户零配置

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$SKILL_DIR/.data"
PID_FILE="$DATA_DIR/dailyhot.pid"
LOG_FILE="$DATA_DIR/dailyhot.log"
PORT="${DAILYHOT_PORT:-6688}"
INSTALL_DIR="$DATA_DIR/service"

mkdir -p "$DATA_DIR"
mkdir -p "$INSTALL_DIR"

# === 检查是否已安装 ===
if [ ! -d "$INSTALL_DIR/node_modules/dailyhot-api" ]; then
  echo "📦 首次运行，正在安装 DailyHotApi..."
  cd "$INSTALL_DIR"
  echo '{"name":"dailyhot-service","version":"1.0.0","private":true}' > package.json
  npm install dailyhot-api --save 2>&1
  echo "✅ DailyHotApi 安装完成"
fi

# === 检查服务是否运行中 ===
is_running() {
  if [ -f "$PID_FILE" ]; then
    local pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
      return 0
    fi
  fi
  return 1
}

check_health() {
  curl -s -m 3 "http://localhost:$PORT/" > /dev/null 2>&1
}

# === 如果已运行且健康，直接返回 ===
if is_running && check_health; then
  echo "✅ DailyHotApi 服务运行中 — http://localhost:$PORT"
  exit 0
fi

# === 清理残留进程 ===
if [ -f "$PID_FILE" ]; then
  old_pid=$(cat "$PID_FILE")
  kill "$old_pid" 2>/dev/null || true
  rm -f "$PID_FILE"
fi

# === 端口占用检测 ===
if ss -tlnp 2>/dev/null | grep -q ":$PORT " || netstat -tlnp 2>/dev/null | grep -q ":$PORT "; then
  echo "⚠️ 端口 $PORT 被占用，尝试备用端口..."
  for alt_port in $(seq 6689 6699); do
    if ! ss -tlnp 2>/dev/null | grep -q ":$alt_port " && ! netstat -tlnp 2>/dev/null | grep -q ":$alt_port "; then
      PORT=$alt_port
      echo "🔄 使用备用端口 $PORT"
      break
    fi
  done
fi

# === 启动服务 ===
echo "🚀 正在启动 DailyHotApi 服务..."
cd "$INSTALL_DIR"
NODE_ENV=development PORT=$PORT node node_modules/dailyhot-api/dist/index.js > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

# === 等待服务就绪 ===
max_wait=15
waited=0
while [ $waited -lt $max_wait ]; do
  if check_health; then
    echo "✅ DailyHotApi 服务已启动 — http://localhost:$PORT"
    echo "$PORT" > "$DATA_DIR/port"
    exit 0
  fi
  sleep 1
  waited=$((waited + 1))
done

echo "❌ DailyHotApi 启动超时，请检查日志：$LOG_FILE"
cat "$LOG_FILE" | tail -10
exit 1
