#!/usr/bin/env bash
#
# LinkedIn 图文运营 Agent - 安装脚本
# 自动检查依赖、安装 skills、配置环境
#

set -e

echo "=========================================="
echo "📌 LinkedIn 图文运营 Agent - 安装向导"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查函数
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 已安装"
        return 0
    else
        echo -e "${RED}✗${NC} $1 未安装"
        return 1
    fi
}

check_version() {
    local cmd=$1
    local min_version=$2
    local current_version=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    
    if [ -z "$current_version" ]; then
        echo -e "${YELLOW}⚠${NC} 无法检测 $cmd 版本"
        return 1
    fi
    
    echo -e "${GREEN}✓${NC} $cmd 版本: $current_version"
    return 0
}

# 步骤 1: 检查系统依赖
echo "步骤 1/5: 检查系统依赖"
echo "---"

all_deps_ok=true

if ! check_command "openclaw"; then
    echo -e "${RED}错误: OpenClaw 未安装${NC}"
    echo "请访问 https://openclaw.ai 安装 OpenClaw"
    exit 1
fi

if ! check_command "node"; then
    echo -e "${RED}错误: Node.js 未安装${NC}"
    echo "请访问 https://nodejs.org 安装 Node.js ≥ 20"
    all_deps_ok=false
else
    check_version "node" "20.0.0"
fi

if ! check_command "python3"; then
    echo -e "${RED}错误: Python3 未安装${NC}"
    echo "请安装 Python 3.8 或更高版本"
    all_deps_ok=false
else
    check_version "python3" "3.8.0"
fi

if ! check_command "pip3"; then
    echo -e "${YELLOW}⚠ pip3 未安装，尝试安装...${NC}"
    python3 -m ensurepip --upgrade
fi

if ! check_command "git"; then
    echo -e "${RED}错误: git 未安装${NC}"
    echo "请安装 git（用于从 GitHub 下载 skills）"
    all_deps_ok=false
fi

if [ "$all_deps_ok" = false ]; then
    echo ""
    echo -e "${RED}依赖检查失败，请先安装缺失的软件${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ 所有系统依赖已满足${NC}"
echo ""

# 步骤 2: 检查并安装 Skills
echo "步骤 2/5: 检查 Skills"
echo "---"

SKILLS_DIR="$HOME/.openclaw/skills"
LOCAL_SKILLS_DIR="./skills"

check_skill() {
    local skill_name=$1
    if [ -d "$LOCAL_SKILLS_DIR/$skill_name" ] || [ -d "$SKILLS_DIR/$skill_name" ]; then
        echo -e "${GREEN}✓${NC} $skill_name 已安装"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $skill_name 未安装"
        return 1
    fi
}

# 从 GitHub 安装 skill
install_skill_from_github() {
    local skill_name=$1
    local clone_url=$2
    local subdirectory=$3
    
    echo "正在从 GitHub 安装 $skill_name..."
    
    # 创建临时目录
    local temp_dir=$(mktemp -d)
    
    # 克隆仓库
    if git clone --depth 1 "$clone_url" "$temp_dir" > /dev/null 2>&1; then
        # 如果有子目录，复制子目录；否则复制整个仓库
        if [ -n "$subdirectory" ]; then
            if [ -d "$temp_dir/$subdirectory" ]; then
                mkdir -p "$LOCAL_SKILLS_DIR"
                cp -r "$temp_dir/$subdirectory" "$LOCAL_SKILLS_DIR/$skill_name"
                echo -e "${GREEN}✓${NC} $skill_name 安装成功"
            else
                echo -e "${RED}✗${NC} $skill_name 子目录不存在: $subdirectory"
                rm -rf "$temp_dir"
                return 1
            fi
        else
            mkdir -p "$LOCAL_SKILLS_DIR"
            cp -r "$temp_dir" "$LOCAL_SKILLS_DIR/$skill_name"
            echo -e "${GREEN}✓${NC} $skill_name 安装成功"
        fi
        
        rm -rf "$temp_dir"
        return 0
    else
        echo -e "${RED}✗${NC} $skill_name 克隆失败"
        rm -rf "$temp_dir"
        return 1
    fi
}

# 读取 skill 配置
if [ -f "scripts/skill_sources.json" ]; then
    skills_to_install=()
    
    # 检查每个 skill
    for skill in dailyhot-api giggle-generation-image x2c-socialposter claw-dashboard; do
        if ! check_skill "$skill"; then
            skills_to_install+=("$skill")
        fi
    done
    
    if [ ${#skills_to_install[@]} -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}需要安装以下 skills:${NC}"
        for skill in "${skills_to_install[@]}"; do
            echo "  - $skill"
        done
        echo ""
        read -p "是否自动从 GitHub 安装？(y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # 安装 dailyhot-api, giggle-generation-image, x2c-socialposter
            if [[ " ${skills_to_install[@]} " =~ " dailyhot-api " ]] || \
               [[ " ${skills_to_install[@]} " =~ " giggle-generation-image " ]] || \
               [[ " ${skills_to_install[@]} " =~ " x2c-socialposter " ]]; then
                echo "从 https://github.com/giggle-official/skills 安装..."
                install_skill_from_github "giggle-skills-temp" \
                    "https://github.com/giggle-official/skills.git" \
                    ""
                
                # 复制需要的 skills
                for skill in dailyhot-api giggle-generation-image x2c-socialposter; do
                    if [[ " ${skills_to_install[@]} " =~ " $skill " ]]; then
                        if [ -d "$LOCAL_SKILLS_DIR/giggle-skills-temp/skills/$skill" ]; then
                            cp -r "$LOCAL_SKILLS_DIR/giggle-skills-temp/skills/$skill" "$LOCAL_SKILLS_DIR/"
                            echo -e "${GREEN}✓${NC} $skill 已安装"
                        fi
                    fi
                done
                
                # 清理临时目录
                rm -rf "$LOCAL_SKILLS_DIR/giggle-skills-temp"
            fi
            
            # 安装 claw-dashboard
            if [[ " ${skills_to_install[@]} " =~ " claw-dashboard " ]]; then
                install_skill_from_github "claw-dashboard" \
                    "https://github.com/yshi0730/claw-dashboard-skill.git" \
                    ""
            fi
        else
            echo -e "${YELLOW}跳过自动安装，请手动安装:${NC}"
            echo ""
            echo "从 GitHub 安装 skills:"
            echo "  git clone https://github.com/giggle-official/skills.git"
            echo "  cp -r skills/skills/dailyhot-api $LOCAL_SKILLS_DIR/"
            echo "  cp -r skills/skills/giggle-generation-image $LOCAL_SKILLS_DIR/"
            echo "  cp -r skills/skills/x2c-socialposter $LOCAL_SKILLS_DIR/"
            echo ""
            echo "  git clone https://github.com/yshi0730/claw-dashboard-skill.git $LOCAL_SKILLS_DIR/claw-dashboard"
        fi
    else
        echo -e "${GREEN}✓ 所有 Skills 已安装${NC}"
    fi
else
    echo -e "${YELLOW}⚠ skill_sources.json 不存在，跳过自动安装${NC}"
fi

echo ""

# 步骤 3: 安装 Python 依赖
echo "步骤 3/5: 安装 Python 依赖"
echo "---"

# 安装视频处理依赖
echo "安装视频处理依赖 (imageio-ffmpeg)..."
pip3 install imageio-ffmpeg --quiet && echo -e "${GREEN}✓${NC} imageio-ffmpeg 已安装" || echo -e "${YELLOW}⚠${NC} 安装失败"

if [ -d "$SKILLS_DIR/claw-dashboard" ] || [ -d "$LOCAL_SKILLS_DIR/claw-dashboard" ]; then
    echo "安装 claw-dashboard 依赖..."
    if [ -d "$LOCAL_SKILLS_DIR/claw-dashboard" ]; then
        cd "$LOCAL_SKILLS_DIR/claw-dashboard"
    else
        cd "$SKILLS_DIR/claw-dashboard"
    fi
    pip3 install -e . > /dev/null 2>&1 && echo -e "${GREEN}✓${NC} claw-dashboard 依赖已安装" || echo -e "${YELLOW}⚠${NC} 安装失败"
    cd - > /dev/null
else
    echo -e "${YELLOW}⚠ claw-dashboard 未找到，跳过${NC}"
fi

echo ""

# 步骤 4: 检查配置文件
echo "步骤 4/5: 检查配置文件"
echo "---"

if [ -f "config.json" ]; then
    echo -e "${GREEN}✓${NC} config.json 已存在"
    
    # 检查是否已配置 API 密钥
    if grep -q '"giggle_api_key": ""' config.json && grep -q '"x2c_api_key": ""' config.json; then
        echo -e "${YELLOW}⚠ API 密钥未配置${NC}"
        echo "请在 OpenClaw 会话中与 Agent 对话完成首次配置"
    else
        echo -e "${GREEN}✓${NC} API 密钥已配置"
    fi
else
    echo -e "${YELLOW}⚠ config.json 不存在${NC}"
    echo "首次启动时 Agent 会自动创建"
fi

echo ""

# 步骤 5: 完成
echo "步骤 5/5: 安装完成"
echo "---"

echo ""
echo "=========================================="
echo -e "${GREEN}✓ 安装完成！${NC}"
echo "=========================================="
echo ""
echo "下一步:"
echo ""
echo "1. 启动 OpenClaw:"
echo "   openclaw"
echo ""
echo "2. 与 Agent 对话，完成首次配置:"
echo "   (Agent 会自动引导你配置 API 密钥、内容方向等)"
echo ""
echo "3. 或手动触发生产:"
echo "   run now"
echo ""
echo "4. 查看 Dashboard (如果已启用):"
echo "   show dashboard"
echo ""
echo "详细文档:"
echo "  - README.md: 功能概述和使用指南"
echo "  - INSTALL.md: 详细安装说明"
echo "  - AGENTS.md: 完整操作规范"
echo ""
echo "=========================================="
