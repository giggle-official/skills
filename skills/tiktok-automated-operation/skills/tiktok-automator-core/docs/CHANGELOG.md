# 更新日志

## v5.1 (2026-04-23)

### 🎉 新增
- ✨ 添加 `scripts/skill_sources.json` 配置文件，记录所有 skills 的 GitHub 地址
- ✨ 更新 `install.sh`，支持从 GitHub 自动克隆 skills
- ✨ 更新 README.md 和 INSTALL.md，添加 skills 来源说明

### 📝 Skills 来源
- **dailyhot-api**: https://github.com/giggle-official/skills/tree/main/skills/dailyhot-api
- **giggle-generation-drama**: https://github.com/giggle-official/skills/tree/main/skills/giggle-generation-drama
- **x2c-socialposter**: https://github.com/giggle-official/skills/tree/main/skills/x2c-socialposter
- **claw-dashboard**: https://github.com/yshi0730/claw-dashboard-skill

### 🔧 改进
- 🔧 install.sh 现在会自动从 GitHub 克隆 skills（需要 git）
- 🔧 添加手动安装 skills 的详细说明
- 🔧 打包文件不再包含 skills（体积从 129KB 降至 51KB）

### 📦 打包文件
- **tiktok-agent-v5.1.tar.gz** (51KB) - 推荐版本
  - 不含 skills
  - install.sh 会自动从 GitHub 安装
  - 需要 git 和网络连接

- **tiktok-agent-v5.0-with-skills.tar.gz** (129KB) - 备用版本
  - 包含 skills
  - 适合无网络环境或 GitHub 访问受限的用户

---

## v5.0 (2026-04-23)

### 🎉 新增
- ✨ 自动首评功能（等待30分钟）
- ✨ Dashboard 可视化面板
- ✨ 评论管理功能
- ✨ 完善安装自动化（install.sh）
- ✨ 完善文档（README, INSTALL, PACKAGING）

### 🐛 修复
- 🐛 修复视频压缩问题
- 🐛 修复步骤编号混乱问题

### 📝 文档
- 📝 新增 README.md - 项目说明
- 📝 新增 INSTALL.md - 安装指南
- 📝 新增 PACKAGING.md - 打包指南
- 📝 新增 config.template.json - 配置模板
- 📝 新增 .gitignore - Git 排除规则

### 🔧 改进
- 🔧 优化 AGENTS.md 步骤编号
- 🔧 添加 verify_installation.py 验证脚本
- 🔧 添加 install.sh 一键安装脚本
