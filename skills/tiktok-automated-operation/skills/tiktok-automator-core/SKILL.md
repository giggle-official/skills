---
name: tiktok-automator-core
description: "TikTok automation core module for trend collection, auto first-comment posting, dashboard updates, comment failure checks, and installation verification."
version: "1.0.1"
license: MIT
author: tiktok-drama-trend-automator
homepage: https://github.com/storyclaw-official/skills
repository: https://github.com/storyclaw-official/skills
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY, X2C_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "📡",
      "requires": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY", "X2C_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "X2C_API_KEY",
      "installSpec": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY", "X2C_API_KEY"],
        "pip": ["requests"]
      }
    }
  }
---

# TikTok Automator Core Skill

**Skill ID**: tiktok-automator-core  
**Version**: 1.0.0  
**Description**: TikTok 自动化运营核心功能模块

---

## 功能说明

本 Skill 提供 TikTok 自动化运营的核心功能：

### 1. 轻量采集
- **脚本**: `scripts/lightweight_collect.py`
- **功能**: 从数据池中筛选和追加热点
- **调用**: 定时任务每小时执行

### 2. 自动首评
- **脚本**: `scripts/auto_first_comment.py`
- **功能**: 视频发布后自动发布首条评论
- **特性**: 智能等待机制，精确时间匹配

### 3. Dashboard 集成
- **脚本**: `scripts/dashboard_integration.py`
- **功能**: 更新可视化数据面板
- **脚本**: `scripts/setup_dashboard.py`
- **功能**: 一键设置 Dashboard

### 4. 评论管理
- **脚本**: `scripts/check_comment_failures.py`
- **功能**: 检查首评失败通知
- **脚本**: `scripts/configure_auto_comment.py`
- **功能**: 配置自动首评

### 5. 安装验证
- **脚本**: `scripts/verify_installation.py`
- **功能**: 验证技能依赖和配置

---

## 依赖

### 外部技能
- `dailyhot-api` - 全网热榜采集
- `giggle-generation-drama` - AI 视频生成
- `x2c-socialposter` - TikTok 发布
- `claw-dashboard` - 可视化数据面板

### Python 包
- `requests`
- `json`
- `pathlib`

---

## 配置文件

### config.json
主配置文件，包含：
- API 密钥（Giggle, X2C）
- 用户画像
- 内容方向
- 视频风格
- 发布节奏
- 评论管理
- Dashboard 设置

### config.template.json
配置模板，首次运行时会引导用户创建 config.json

---

## 文档

### docs/auto_comment_optimization.md
自动首评功能优化说明，包含：
- 问题分析
- 优化方案
- 使用方法
- 性能提升

---

## 使用方法

### 验证安装
```bash
python3 skills/tiktok-automator-core/scripts/verify_installation.py
```

### 手动更新 Dashboard
```bash
python3 skills/tiktok-automator-core/scripts/dashboard_integration.py update
```

### 手动补发首评
```bash
python3 skills/tiktok-automator-core/scripts/auto_first_comment.py \
  "v_pub_url~xxx" "1" "视频标题" "2026-04-24T12:17:00+08:00"
```

---

## 注意事项

1. 所有脚本必须在 Agent 根目录下执行
2. 需要先完成首次配置才能使用
3. API Key 必须有效
4. 技能依赖必须已安装

---

**维护者**: Kiro  
**最后更新**: 2026-04-24
