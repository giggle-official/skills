#!/bin/bash
# DailyHotApi 停止脚本

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$SKILL_DIR/.data"
PID_FILE="$DATA_DIR/dailyhot.pid"

if [ -f "$PID_FILE" ]; then
  pid=$(cat "$PID_FILE")
  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null
    echo "✅ DailyHotApi 服务已停止 (PID: $pid)"
  else
    echo "⚠️ 进程 $pid 已不存在"
  fi
  rm -f "$PID_FILE"
else
  echo "⚠️ 未找到运行中的 DailyHotApi 服务"
fi
