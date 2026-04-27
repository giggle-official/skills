# 📦 安装指南

本文档详细说明如何安装和配置 TikTok 自媒体运营 Agent。

---

## 系统要求

### 必需软件

| 软件 | 最低版本 | 检查命令 | 安装指南 |
|------|---------|---------|---------|
| **OpenClaw** | 最新版 | `openclaw --version` | [openclaw.ai](https://openclaw.ai) |
| **Node.js** | ≥ 20.0.0 | `node --version` | [nodejs.org](https://nodejs.org) |
| **Python 3** | ≥ 3.8 | `python3 --version` | 系统自带或 [python.org](https://python.org) |
| **pip** | 最新版 | `pip3 --version` | `python3 -m ensurepip` |

### 必需 API 密钥

| 服务 | 用途 | 获取地址 | 费用 |
|------|------|---------|------|
| **Giggle API** | AI 视频生成 | [giggle.pro](https://giggle.pro) | 按量计费 |
| **X2C API** | TikTok 发布 | [x2creel.ai](https://www.x2creel.ai) | 免费/付费套餐 |

---

## 安装步骤

### 方式 1：一键安装（推荐）

```bash
# 1. 下载 Agent
cd ~/.openclaw/
git clone <your-repo-url> workspace-tiktok-automator-cn-2026

# 2. 进入目录
cd workspace-tiktok-automator-cn-2026

# 3. 运行安装脚本
bash scripts/install.sh
```

安装脚本会自动：
1. 检查系统依赖（Node.js, Python3）
2. 安装缺失的 skills
3. 检查 pip 依赖
4. 提示你运行首次配置

---

### 方式 2：手动安装

#### 步骤 1：检查系统依赖

```bash
# 检查 Node.js
node --version  # 应该 ≥ 20.0.0

# 检查 Python3
python3 --version  # 应该 ≥ 3.8

# 检查 pip
pip3 --version
```

如果缺失，请先安装。

#### 步骤 2：安装 Skills



#### Skills 来源

本 Agent 依赖的 skills 托管在 GitHub 上：

| Skill | GitHub 地址 |
|-------|------------|
| dailyhot-api | https://github.com/giggle-official/skills/tree/main/skills/dailyhot-api |
| giggle-generation-drama | https://github.com/giggle-official/skills/tree/main/skills/giggle-generation-drama |
| x2c-socialposter | https://github.com/giggle-official/skills/tree/main/skills/x2c-socialposter |
| claw-dashboard | https://github.com/yshi0730/claw-dashboard-skill |

**install.sh 会自动从 GitHub 克隆这些 skills。**

#### 手动安装 Skills（如果自动安装失败）

```bash
# 安装 dailyhot-api, giggle-generation-drama, x2c-socialposter
git clone https://github.com/giggle-official/skills.git /tmp/giggle-skills
cp -r /tmp/giggle-skills/skills/dailyhot-api ~/.openclaw/skills/
cp -r /tmp/giggle-skills/skills/giggle-generation-drama ~/.openclaw/skills/
cp -r /tmp/giggle-skills/skills/x2c-socialposter ~/.openclaw/skills/
rm -rf /tmp/giggle-skills

# 安装 claw-dashboard
git clone https://github.com/yshi0730/claw-dashboard-skill.git ~/.openclaw/skills/claw-dashboard
```

```bash
# 安装热点采集 skill
openclaw skills install dailyhot-api

# 安装视频生成 skill
openclaw skills install giggle-generation-drama

# 安装 TikTok 发布 skill
openclaw skills install x2c-socialposter

# 安装 Dashboard skill
openclaw skills install claw-dashboard
```

#### 步骤 3：检查 Skills 安装

```bash
# 检查本地 skills
ls -la skills/

# 检查全局 skills
ls -la ~/.openclaw/skills/
```

应该看到：
- `dailyhot-api/`
- `giggle-generation-drama/`
- `x2c-socialposter/`
- `claw-dashboard/` (可能在全局目录)

#### 步骤 4：安装 Python 依赖

```bash
# claw-dashboard 依赖
cd ~/.openclaw/skills/claw-dashboard
pip3 install -e .
```

---

## 首次配置

安装完成后，启动 OpenClaw 并与 Agent 对话，它会自动引导你完成配置。

### 配置流程

#### 第 0 步：用户画像（可选）
提供你的身份、专业背景、内容风格偏好，Agent 会据此优化内容生产。

#### 第 1 步：API 密钥
```
问: "请提供你的 Giggle API Key"
→ 在 https://giggle.pro 账号设置中获取

问: "请提供你的 X2C API Key"
→ 在 https://www.x2creel.ai 注册后获取，并关联 TikTok 账号
```

#### 第 2 步：内容方向
```
问: "你的内容赛道是什么？"
→ 可选：科技数码、财经理财、娱乐八卦、美食探店、健身运动、教育知识、汽车、时尚穿搭、游戏电竞、职场成长

问: "关注哪些关键词？"
→ 如：AI、iPhone、比特币、减肥、考研

问: "需要排除哪些话题？"
→ 如：政治、军事、灾难

问: "你的目标受众是谁？"
→ 如：Z世代、职场白领、宝妈、大学生
```

#### 第 3 步：视频风格
根据赛道自动推荐风格，或自选。

#### 第 4 步：时区
```
问: "你的时区？"
→ 如：Asia/Shanghai, Asia/Singapore
```

#### 第 5 步：发布节奏
```
问: "你希望什么时候自动生产内容并发布到 TikTok？"

方式 A：固定时间点（推荐）
→ 每天在指定时间触发，如"每天 14:30"
→ 可设置多个时间点，如"每天 9:00 和 18:00"

方式 B：固定间隔
→ 每隔 N 小时触发一次（最少 4 小时）
```

#### 第 5.5 步：评论管理（可选）
```
问: "是否启用评论管理功能？"
→ 启用后，Agent 会定时巡检评论并推送摘要
```

#### 第 5.6 步：自动首评（可选）
```
问: "是否启用自动首评功能？"
→ 启用后，视频发布 30 分钟后自动发布首条评论

方式 1：使用预设模板（系统自动选择）
方式 2：自定义固定评论（每个视频都用这条）
```

#### 第 6 步：注册定时任务
配置完成后，Agent 会自动注册 4 个定时任务：
- 热点轻量采集（每 1 小时）
- TikTok 内容生产（按你设置的时间）
- 历史数据清理（每 24 小时）
- 评论巡检（如果启用）

#### 第 6.5 步：Dashboard（可选）
```
问: "是否需要搞建可视化数据面板？"
→ 启用后可在浏览器查看运营数据
```

---

## 验证安装

### 检查配置文件

```bash
cat config.json | jq '.credentials'
```

应该看到你的 API 密钥已配置。

### 检查定时任务

```bash
openclaw cron list
```

应该看到 3-4 个任务（取决于是否启用评论管理）。

### 手动触发测试

在 OpenClaw 会话中输入：
```
run now
```

Agent 会立即执行完整流程，预计 50-60 分钟完成。

---

## 常见安装问题

### Q: Node.js 版本过低
```bash
# 使用 nvm 安装最新版
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
```

### Q: pip 安装 claw-dashboard 失败
```bash
# 升级 pip
python3 -m pip install --upgrade pip

# 重新安装
cd ~/.openclaw/skills/claw-dashboard
pip3 install -e .
```

### Q: skills 安装失败
```bash
# 手动克隆 skill
cd ~/.openclaw/skills/
git clone <skill-repo-url>
```

### Q: 定时任务没有注册
```bash
# 手动注册（在 OpenClaw 会话中）
setup cron
```

---

## 卸载

```bash
# 1. 删除定时任务
openclaw cron list  # 查看任务 ID
openclaw cron remove <job-id>

# 2. 删除 Agent 目录
rm -rf ~/.openclaw/workspace-tiktok-automator-cn-2026

# 3. 删除 skills（可选）
rm -rf ~/.openclaw/skills/dailyhot-api
rm -rf ~/.openclaw/skills/giggle-generation-drama
rm -rf ~/.openclaw/skills/x2c-socialposter
rm -rf ~/.openclaw/skills/claw-dashboard
```

---

## 下一步

安装完成后，查看 [README.md](README.md) 了解使用方法。
