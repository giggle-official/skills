#!/bin/bash
# deploy-templates.sh - 部署自定义 Dashboard 模板

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATES_DIR="$SKILL_DIR/templates"
TARGET_DIR="$HOME/.claw/hub/templates"

echo "📊 部署 Dashboard 模板..."
echo ""

# 检查源文件
if [ ! -f "$TEMPLATES_DIR/module.html" ]; then
    echo "❌ 模板文件不存在: $TEMPLATES_DIR/module.html"
    exit 1
fi

# 确保目标目录存在
mkdir -p "$TARGET_DIR"

# 备份现有文件
if [ -f "$TARGET_DIR/module.html" ]; then
    cp "$TARGET_DIR/module.html" "$TARGET_DIR/module.html.backup.$(date +%Y%m%d_%H%M%S)"
fi

# 复制模板
cp "$TEMPLATES_DIR/module.html" "$TARGET_DIR/module.html"
cp "$TEMPLATES_DIR/widget_render.html" "$TARGET_DIR/widget_render.html"

echo "✅ 模板已部署"
echo ""

# 重启 Hub
echo "🔄 重启 Dashboard Hub..."
pkill -f "uvicorn app:app" 2>/dev/null || true
sleep 2
cd ~/.claw/hub && nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 3000 > ~/.claw/hub.log 2>&1 &
sleep 3

if pgrep -f "uvicorn" > /dev/null; then
    echo "✅ Dashboard Hub 已重启"
else
    echo "❌ Dashboard Hub 启动失败"
    exit 1
fi

echo ""
echo "🎉 部署完成！"
