# 定时任务配置指南

本文档说明如何正确配置 Instagram Automator 的定时任务，避免会话 token 耗尽问题。

## ⚠️ 重要：使用 isolated 模式

**所有定时任务必须使用 `isolated` 模式**，避免在主会话中累积 token 消耗。

### 错误配置 ❌
```json
{
  "sessionTarget": "session:agent:instagram-automator-cn-2026:main",
  "payload": {
    "kind": "agentTurn",
    "message": "执行任务..."
  }
}
```
- 在主会话中执行，会累积 token
- 5天后会话耗尽，任务无法执行

### 正确配置 ✅
```json
{
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行任务...",
    "timeoutSeconds": 600
  },
  "delivery": {
    "mode": "none"  // 或 "announce"
  }
}
```
- 每次在独立会话中执行
- 任务完成后会话自动销毁
- 不会累积 token

---

## 📋 必需的 4 个定时任务

### 1. 热点轻量采集（每1小时）

**作用**: 每小时采集全网热点，写入数据池

```bash
openclaw cron add --job '{
  "name": "热点轻量采集（每1小时）",
  "schedule": {
    "kind": "every",
    "everyMs": 3600000
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行定时轻量采集任务：运行阶段1和阶段2，将Top 10候选写入今天的数据池。只执行阶段1和2，不执行阶段3-7。静默执行。",
    "timeoutSeconds": 600
  },
  "delivery": {
    "mode": "none"
  }
}'
```

### 2. 完整内容生产（每天 10:00）

**作用**: 从数据池选取 Top 3，生成视频并发布到 Instagram

```bash
openclaw cron add --job '{
  "name": "Instagram内容生产（每天 10:00）",
  "schedule": {
    "kind": "cron",
    "expr": "0 10 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行定时完整生产任务：严格按照 AGENTS.md「任务2：完整生产」步骤B1-B6执行。重点：步骤B5数据池重置必须执行，完成后将报告发送给用户。",
    "timeoutSeconds": 7200
  },
  "delivery": {
    "mode": "announce"
  }
}'
```

### 3. 评论巡检（每8小时）

**作用**: 拉取最近7天发布帖子的新评论，过滤垃圾评论

```bash
openclaw cron add --job '{
  "name": "Instagram评论巡检（每8小时）",
  "schedule": {
    "kind": "every",
    "everyMs": 28800000
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行定时评论巡检任务：按 AGENTS.md「任务4：评论巡检」步骤D1-D7执行，拉取最近 7 天发布帖子的新评论，生成摘要推送给用户。",
    "timeoutSeconds": 300
  },
  "delivery": {
    "mode": "announce"
  }
}'
```

### 4. 历史数据清理（每24小时）

**作用**: 清理10天前的历史文件，保留 reports/ 永久保存

```bash
openclaw cron add --job '{
  "name": "历史数据清理（每24小时）",
  "schedule": {
    "kind": "every",
    "everyMs": 86400000
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行定时数据清理任务，按 AGENTS.md「任务3：数据清理」步骤C1-C6执行。绝对禁止删除 outputs/reports/ 目录。静默执行。",
    "timeoutSeconds": 120
  },
  "delivery": {
    "mode": "none"
  }
}'
```

---

## 🔧 首次安装时自动注册

在 `scripts/setup_cron.py` 中实现自动注册逻辑：

```python
import subprocess
import json

def register_cron_tasks():
    """首次安装时自动注册所有定时任务"""
    
    tasks = [
        {
            "name": "热点轻量采集（每1小时）",
            "schedule": {"kind": "every", "everyMs": 3600000},
            "sessionTarget": "isolated",
            "payload": {
                "kind": "agentTurn",
                "message": "执行定时轻量采集任务...",
                "timeoutSeconds": 600
            },
            "delivery": {"mode": "none"}
        },
        # ... 其他任务
    ]
    
    for task in tasks:
        subprocess.run([
            "openclaw", "cron", "add",
            "--job", json.dumps(task)
        ])
```

---

## 📊 验证定时任务

```bash
# 查看所有任务
openclaw cron list

# 检查任务状态
openclaw cron list | grep -E "(name|sessionTarget|lastRunStatus)"
```

**正确的输出应该是**:
- 所有任务的 `sessionTarget` 都是 `"isolated"`
- 没有重复的任务名称
- `lastRunStatus` 应该是 `"ok"`（不是 `"error"`）

---

## 🚨 常见问题

### Q: 为什么任务报错 "Channel is required"？

A: `delivery.mode = "announce"` 需要配置 channel。有两种解决方案：

1. **方案1**: 改为静默模式（推荐）
   ```json
   "delivery": {"mode": "none"}
   ```

2. **方案2**: 指定 channel
   ```json
   "delivery": {
     "mode": "announce",
     "channel": "webchat"
   }
   ```

### Q: 如何删除重复的任务？

A: 使用任务 ID 删除：
```bash
openclaw cron remove <jobId>
```

### Q: 如何修改现有任务的配置？

A: 先删除旧任务，再添加新任务：
```bash
openclaw cron remove <jobId>
openclaw cron add --job '{...}'
```

---

## 📝 更新日志

- **2026-04-27**: 修复 token 耗尽问题，所有任务改为 isolated 模式
- **2026-04-24**: 初始版本
