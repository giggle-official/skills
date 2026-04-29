#!/bin/bash

PACKAGE_NAME="instagram-automator-cn-2026-v1.0.0"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${PACKAGE_NAME}_${TIMESTAMP}.tar.gz"

echo "📦 开始打包 Instagram Automator Agent..."
echo ""

# 创建临时目录
TEMP_DIR="/tmp/${PACKAGE_NAME}"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# 复制文件
echo "📋 复制文件..."

# 核心文档
cp AGENTS.md README.md SOUL.md IDENTITY.md USER.md TOOLS.md HEARTBEAT.md "$TEMP_DIR/"
cp TROUBLESHOOTING.md DEPLOYMENT_CHECKLIST.md RELEASE_NOTES.md FIXES_SUMMARY.md "$TEMP_DIR/"

# 配置模板
cp config.template.json "$TEMP_DIR/"
cp .gitignore "$TEMP_DIR/"

# 核心脚本
mkdir -p "$TEMP_DIR/skills/instagram-automator-core/scripts"
cp -r skills/instagram-automator-core/scripts/*.py "$TEMP_DIR/skills/instagram-automator-core/scripts/"

# 文档
mkdir -p "$TEMP_DIR/skills/instagram-automator-core/docs"
cp -r skills/instagram-automator-core/docs/*.md "$TEMP_DIR/skills/instagram-automator-core/docs/" 2>/dev/null || true

# 输出目录结构
mkdir -p "$TEMP_DIR/outputs"/{briefs,scripts,videos,logs,pool,reports}

# 创建 README
cat > "$TEMP_DIR/outputs/README.md" << 'INNER_EOF'
# 输出目录说明

此目录用于存储 Agent 运行时生成的所有文件。

## 目录结构

- `briefs/` - 热点提炼卡
- `scripts/` - 视频脚本
- `videos/` - 生成的视频文件
- `logs/` - 运行日志
- `pool/` - 热点数据池
- `reports/` - 生产报告（永久保留）

## 注意事项

- 除 `reports/` 外，其他目录的文件会在 10 天后自动清理
- 视频文件较大，建议定期备份到外部存储
INNER_EOF

echo "✅ 文件复制完成"

# 打包
echo ""
echo "🗜️ 压缩打包..."
cd /tmp
tar -czf "$OUTPUT_FILE" "${PACKAGE_NAME}"

# 移动到原目录
mv "$OUTPUT_FILE" ~/.openclaw/workspace-instagram-automator-cn-2026/

# 清理临时目录
rm -rf "$TEMP_DIR"

echo "✅ 打包完成"
echo ""
echo "📦 输出文件: $OUTPUT_FILE"
echo "📊 文件大小: $(du -h ~/.openclaw/workspace-instagram-automator-cn-2026/$OUTPUT_FILE | cut -f1)"
echo ""
echo "🎉 Agent 已准备好上传到 TalentHub 市场！"
