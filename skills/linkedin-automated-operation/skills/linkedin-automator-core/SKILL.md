---
name: linkedin-automator-core
description: "LinkedIn image-content automation core module."
version: "2.0.0"
license: MIT
author: linkedin-image-trend-automator
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY, X2C_API_KEY]
  pip: [requests]
---

# LinkedIn Automator Core Skill

> 当前能力为 LinkedIn 图文流程核心模块。

## 功能

- 热点轻量采集：`scripts/lightweight_collect.py`
- Dashboard 初始化/更新：`scripts/setup_dashboard.py`、`scripts/dashboard_integration.py`
- 安装验证：`scripts/verify_installation.py`
- 评论管理相关辅助脚本

## 依赖技能

- `dailyhot-api`
- `giggle-generation-image`
- `x2c-socialposter`
- `claw-dashboard`

## 说明

- 本 Skill 不再包含视频生产链路。
- 图片生产请调用 `skills/giggle-generation-image/scripts/generation_api.py`。
