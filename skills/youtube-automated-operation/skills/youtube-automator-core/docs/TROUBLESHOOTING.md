# 故障排查指南

本文档记录了 YouTube Automator 运行过程中可能遇到的问题及解决方案。

---

## 问题 1：轻量采集任务追加 0 条热点

### 症状
- 轻量采集任务执行后，数据池未使用条目显示为 0
- 采集日志显示成功采集了热点，但没有追加到数据池

### 根本原因
- 轻量采集任务中的数据结构解析错误
- 采集脚本返回的是 `raw_data['trends']`（扁平列表）
- 但错误地使用了 `raw_data.get('platforms', [])`（不存在的字段）

### 解决方案
✅ 已修复：使用专用脚本 `skills/youtube-automator-core/scripts/lightweight_collect.py`

**正确的执行步骤：**
```bash
# 步骤 1：启动 DailyHotApi
bash skills/dailyhot-api/scripts/ensure_running.sh

# 步骤 2：采集热点
python3 skills/dailyhot-api/scripts/collect_trends.py \
  --config config.json \
  --output outputs/logs/$(date +%Y%m%d_%H%M)_raw_trends.json

# 步骤 3：使用专用脚本追加到数据池
python3 skills/youtube-automator-core/scripts/lightweight_collect.py

# 步骤 4：停止 DailyHotApi
bash skills/dailyhot-api/scripts/stop.sh
```

**验证修复：**
```bash
# 检查数据池未使用条目数
python3 << 'EOF'
import json
with open('outputs/pool/$(date +%Y%m%d)_trend_pool.json', 'r') as f:
    pool = json.load(f)
unused = sum(1 for c in pool['collections'] for t in c['trends'] if not t['used'])
print(f"未使用条目: {unused}")
EOF
```

---

## 问题 2：视频生成被擅自跳过

### 症状
- 完整生产任务只生成了 1 个视频
- 视频 2 和 3 被跳过，报告中显示"因时间限制未完成"

### 根本原因
- Agent 错误地判断任务会超时
- 擅自使用 `process kill` 终止了视频生成进程
- 实际上定时任务没有硬性超时限制

### 解决方案
✅ 已修复：在 AGENTS.md 中添加严格约束

**绝对禁止的行为：**
1. ❌ 禁止擅自终止视频生成
2. ❌ 禁止跳过视频 2 和 3
3. ❌ 禁止假设任务超时
4. ❌ 禁止主动 kill 进程

**正确的执行方式：**
```python
# 使用 for 循环依次生成 3 个视频
for N in [1, 2, 3]:
    # 生成视频
    result = generate_video(trend_N)
    
    # 等待完成（timeout=900000，即 15 分钟）
    wait_until_complete(timeout=900000)
    
    # 下载视频
    download_video(result)
    
    # ⚠️ 不停止，直接继续下一个视频
```

**验证修复：**
- 下次完整生产任务应该生成 3 个视频
- 即使总耗时 30-40 分钟也必须完成

---

## 问题 3：Dashboard 显示 Error 1033

### 症状
- Dashboard 公网地址无法访问
- 显示 "Error 1033" 或空白页面
- 数据更新失败

### 根本原因
1. Hub 服务没有运行
2. Tunnel 服务没有运行
3. Dashboard 配置不完整（缺少 `module_id` 和 `widget_ids`）

### 解决方案
✅ 已修复：创建一键设置脚本

**执行修复：**
```bash
# 运行一键设置脚本
python3 skills/youtube-automator-core/scripts/setup_dashboard.py
```

**手动修复步骤：**
```bash
# 1. 检查 Hub 状态
python3 skills/youtube-automator-core/scripts/dashboard_integration.py check

# 2. 如果 Hub 未运行，启动服务
cd ~/.openclaw/skills/claw-dashboard
python3 -c "from src.hub import manager; manager.start_hub(); manager.start_tunnel()"

# 3. 等待 3 秒后重新检查
sleep 3
python3 skills/youtube-automator-core/scripts/dashboard_integration.py check

# 4. 如果配置不完整，运行设置脚本
python3 skills/youtube-automator-core/scripts/setup_dashboard.py

# 5. 更新数据
python3 skills/youtube-automator-core/scripts/dashboard_integration.py update
```

**验证修复：**
```bash
# 检查 Dashboard 状态
python3 skills/youtube-automator-core/scripts/dashboard_integration.py check

# 应该返回：
# {
#   "hub_running": true,
#   "tunnel_running": true,
#   "public_url": "https://device-xxx.clawln.app",
#   "healthy": true
# }
```

**访问 Dashboard：**
- 公网地址：`https://device-xxx.clawln.app`
- 本地地址：`http://localhost:3000`

**⚠️ 重要提示：**
- Dashboard 需要等第一次内容生产完成后才会显示数据
- 在此之前，页面可能显示空白或默认数据
- 建议等明天自动生产完成后再访问

---

## 问题 4：热点匹配率低

### 症状
- 数据池中 100 条热点均未匹配用户关键词/赛道
- 触发补充搜索

### 根本原因
- 热榜热点多为社会新闻、娱乐八卦
- 与用户关注的"科技数码、职场成长、教育知识"不匹配

### 解决方案
✅ 已内置：自动触发补充搜索

**优化建议：**
1. 调整 `trend_sources` 配置，增加科技类平台权重
2. 降低娱乐类平台权重

**修改 config.json：**
```json
{
  "trend_sources": {
    "primary": ["36kr", "huxiu", "ithome", "juejin", "sspai", "zhihu"],
    "secondary": ["bilibili", "douyin", "weibo"],
    "top_per_platform": 10
  }
}
```

---

## 问题 5：视频文件过大（>50MB）

### 症状
- 视频大小超过 50MB
- 发布时可能超时

### 根本原因
- ffmpeg 未安装，无法压缩视频

### 解决方案
**安装 ffmpeg：**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y ffmpeg

# macOS
brew install ffmpeg

# 验证安装
ffmpeg -version
```

**压缩视频：**
```bash
# 手动压缩
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -preset fast output.mp4
```

---

## 问题 6：定时任务没有执行

### 症状
- 轻量采集任务没有每小时执行
- 完整生产任务没有在指定时间执行

### 根本原因
- Cron 任务没有正确注册
- OpenClaw Gateway 服务没有运行

### 解决方案
**检查 Cron 任务：**
```bash
# 列出所有 Cron 任务
openclaw cron list
```

**重新注册任务：**
- 删除 `config.json`
- 重新运行首次配置向导
- 确保第 6 步（注册定时任务）成功执行

**检查 Gateway 服务：**
```bash
# 检查状态
openclaw gateway status

# 如果未运行，启动服务
openclaw gateway start
```

---

## 问题 7：Giggle API 余额不足

### 症状
- 视频生成失败
- 错误信息：Insufficient balance

### 解决方案
1. 访问 https://giggle.pro
2. 登录账号
3. 充值余额
4. 重新运行生产任务

---

## 问题 8：X2C API 401 错误

### 症状
- YouTube 发布失败
- 错误信息：401 Unauthorized

### 解决方案
1. 访问 https://www.x2creel.ai
2. 重新授权 YouTube 账号
3. 获取新的 API Key
4. 更新 `config.json` 中的 `x2c_api_key`

---

## 通用排查步骤

### 1. 检查日志
```bash
# 查看最近的采集日志
ls -lt outputs/logs/*_raw_trends.json | head -1

# 查看最近的发布日志
ls -lt outputs/logs/*_publish_log.json | head -1

# 查看数据池状态
python3 << 'EOF'
import json
with open('outputs/pool/$(date +%Y%m%d)_trend_pool.json', 'r') as f:
    pool = json.load(f)
print(f"采集批次: {len(pool['collections'])}")
print(f"总条目: {sum(len(c['trends']) for c in pool['collections'])}")
print(f"未使用: {sum(1 for c in pool['collections'] for t in c['trends'] if not t['used'])}")
EOF
```

### 2. 检查服务状态
```bash
# 检查 DailyHotApi
curl http://localhost:6688/health

# 检查 Dashboard Hub
python3 skills/youtube-automator-core/scripts/dashboard_integration.py check

# 检查 OpenClaw Gateway
openclaw gateway status
```

### 3. 重启服务
```bash
# 重启 DailyHotApi
bash skills/dailyhot-api/scripts/stop.sh
bash skills/dailyhot-api/scripts/ensure_running.sh

# 重启 Dashboard
cd ~/.openclaw/skills/claw-dashboard
python3 -c "from src.hub import manager; manager.stop_hub(); manager.stop_tunnel()"
python3 -c "from src.hub import manager; manager.start_hub(); manager.start_tunnel()"

# 重启 OpenClaw Gateway
openclaw gateway restart
```

---

## 获取帮助

如果以上方法都无法解决问题，请：

1. 收集以下信息：
   - 错误日志
   - `config.json` 内容（隐藏 API Key）
   - 系统信息（`uname -a`）
   - OpenClaw 版本（`openclaw --version`）

2. 提交 Issue：
   - GitHub: https://github.com/your-repo/youtube-automator
   - 或联系技术支持

---

**最后更新**：2026-04-24
