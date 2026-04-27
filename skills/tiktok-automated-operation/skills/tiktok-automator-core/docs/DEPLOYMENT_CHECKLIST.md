# 部署检查清单

在分享给其他用户之前，请确保以下所有项目都已完成。

---

## ✅ 必需文件

- [ ] `AGENTS.md` - 完整的操作规范
- [ ] `config.template.json` - 配置模板
- [ ] `TROUBLESHOOTING.md` - 故障排查指南
- [ ] `skills/tiktok-automator-core/scripts/lightweight_collect.py` - 轻量采集脚本
- [ ] `skills/tiktok-automator-core/scripts/setup_dashboard.py` - Dashboard 设置脚本
- [ ] `skills/tiktok-automator-core/scripts/dashboard_integration.py` - Dashboard 集成脚本

---

## ✅ 技能依赖

确保以下技能已安装：

- [ ] `dailyhot-api` - 全网热榜采集
- [ ] `giggle-generation-drama` - AI 视频生成
- [ ] `x2c-socialposter` - TikTok 发布
- [ ] `claw-dashboard` - 可视化数据面板

**安装命令：**
```bash
openclaw skills install dailyhot-api
openclaw skills install giggle-generation-drama
openclaw skills install x2c-socialposter
openclaw skills install claw-dashboard
```

---

## ✅ 配置完整性

确保 `config.template.json` 包含所有必需字段：

- [ ] `credentials.giggle_api_key`
- [ ] `credentials.x2c_api_key`
- [ ] `content.user_persona`
- [ ] `content.content_reference`
- [ ] `content.content_focus`
- [ ] `content.video_style`
- [ ] `schedule`
- [ ] `comment_management`
- [ ] `auto_first_comment`
- [ ] `dashboard`

---

## ✅ AGENTS.md 约束规则

确保 AGENTS.md 包含以下关键约束：

- [ ] 轻量采集任务的数据结构说明
- [ ] 视频生成的严格约束（禁止跳过）
- [ ] Dashboard 设置流程
- [ ] 错误处理规则
- [ ] 配置完整性检查清单

---

## ✅ 测试验证

### 1. 轻量采集测试
```bash
# 执行轻量采集
bash skills/dailyhot-api/scripts/ensure_running.sh
python3 skills/dailyhot-api/scripts/collect_trends.py \
  --config config.json \
  --output outputs/logs/$(date +%Y%m%d_%H%M)_raw_trends.json
python3 skills/tiktok-automator-core/scripts/lightweight_collect.py
bash skills/dailyhot-api/scripts/stop.sh

# 验证结果
python3 << 'EOF'
import json
with open('outputs/pool/$(date +%Y%m%d)_trend_pool.json', 'r') as f:
    pool = json.load(f)
unused = sum(1 for c in pool['collections'] for t in c['trends'] if not t['used'])
print(f"✅ 未使用条目: {unused}")
assert unused > 0, "❌ 轻量采集失败：未追加任何热点"
EOF
```

### 2. Dashboard 设置测试
```bash
# 执行 Dashboard 设置
python3 skills/tiktok-automator-core/scripts/setup_dashboard.py

# 验证结果
python3 skills/tiktok-automator-core/scripts/dashboard_integration.py check

# 应该返回：
# {
#   "hub_running": true,
#   "tunnel_running": true,
#   "public_url": "https://device-xxx.clawln.app",
#   "healthy": true
# }
```

### 3. 视频生成测试（可选，耗时较长）
```bash
# 手动触发一次完整生产
# 注意：这会消耗 Giggle API 余额
# 验证：
# - 是否生成了 3 个视频
# - 是否没有擅自跳过视频 2 和 3
```

---

## ✅ 文档完整性

- [ ] README.md 包含快速开始指南
- [ ] AGENTS.md 包含完整的操作规范
- [ ] TROUBLESHOOTING.md 包含常见问题解决方案
- [ ] 所有脚本都有注释说明

---

## ✅ 用户友好性

- [ ] 首次配置向导清晰易懂
- [ ] 错误信息有明确的解决建议
- [ ] Dashboard 设置有详细说明
- [ ] 所有命令都有示例

---

## ✅ 安全性

- [ ] API Key 不硬编码在代码中
- [ ] config.json 在 .gitignore 中
- [ ] 敏感信息不出现在日志中

---

## ✅ 兼容性

- [ ] 支持 Python 3.8+
- [ ] 支持 Linux/macOS
- [ ] 依赖项都在 requirements.txt 中

---

## ✅ 最终检查

- [ ] 删除所有测试数据
- [ ] 删除 config.json（保留 config.template.json）
- [ ] 清空 outputs/ 目录
- [ ] 更新版本号
- [ ] 更新 CHANGELOG.md

---

## 打包发布

```bash
# 1. 清理测试数据
rm -f config.json
rm -rf outputs/videos/*
rm -rf outputs/logs/*
rm -rf outputs/pool/*

# 2. 打包
tar -czf tiktok-automator-$(date +%Y%m%d).tar.gz \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  --exclude='.git' \
  --exclude='outputs/videos' \
  --exclude='outputs/logs' \
  --exclude='*.pyc' \
  .

# 3. 验证打包
tar -tzf tiktok-automator-$(date +%Y%m%d).tar.gz | head -20
```

---

## 用户安装验证

让一个新用户按照以下步骤安装：

1. 解压文件
2. 安装依赖
3. 运行首次配置向导
4. 执行一次轻量采集
5. 设置 Dashboard
6. 等待第一次自动生产

**预期结果：**
- 所有步骤都能顺利完成
- 没有遇到本文档未记录的问题
- Dashboard 能正常访问和显示数据

---

**检查完成日期**：________

**检查人**：________

**版本号**：________
