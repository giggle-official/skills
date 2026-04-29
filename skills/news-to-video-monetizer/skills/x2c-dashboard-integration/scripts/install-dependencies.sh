#!/bin/bash
# install-dependencies.sh - 安装依赖 skills（从 workspace 内置）
set -e

echo "📦 检查并安装依赖 skills..."

WORKSPACE_SKILLS="$HOME/.openclaw/workspace-news-to-video-monetizer/skills"

# x2c-real-dashboard 已内置在 workspace/skills/ 中，无需安装
if [ -d "$WORKSPACE_SKILLS/x2c-real-dashboard" ]; then
  echo "  ✅ x2c-real-dashboard (内置)"
else
  echo "  ❌ x2c-real-dashboard 未找到"
  exit 1
fi

# 安装 claw-dashboard-skill
if [ ! -d ~/.openclaw/skills/claw-dashboard-skill ]; then
  echo "  → 安装 claw-dashboard-skill..."
  cd ~/.openclaw/skills && git clone https://github.com/yshi0730/claw-dashboard-skill.git
  echo "  ✅ claw-dashboard-skill 已安装"
else
  echo "  ✅ claw-dashboard-skill 已存在"
fi

echo "✅ 所有依赖已就绪"
