#!/usr/bin/env python3
"""
自动注册定时任务脚本（LinkedIn 图文版）
"""

import subprocess
import json
import sys

def register_cron_task(task_config):
    """注册单个定时任务"""
    try:
        result = subprocess.run(
            ["openclaw", "cron", "add", "--job", json.dumps(task_config)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ 已注册: {task_config['name']}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 注册失败: {task_config['name']}")
        print(f"   错误: {e.stderr}")
        return False

def main():
    """注册所有定时任务"""
    
    print("🔧 开始注册定时任务...")
    print()
    
    # 定义所有任务配置
    tasks = [
        {
            "name": "热点轻量采集（每1小时）",
            "schedule": {
                "kind": "every",
                "everyMs": 3600000
            },
            "sessionTarget": "current",
            "payload": {
                "kind": "agentTurn",
                "message": "执行定时轻量采集任务：运行阶段1和阶段2，将Top 10候选写入今天的数据池。只执行阶段1和2，不执行阶段3-6。静默执行。",
                "timeoutSeconds": 600
            },
            "delivery": {
                "mode": "none"
            }
        },
        {
            "name": "LinkedIn图文生产（每天 10:00）",
            "schedule": {
                "kind": "cron",
                "expr": "0 10 * * *",
                "tz": "Asia/Shanghai"
            },
            "sessionTarget": "current",
            "payload": {
                "kind": "agentTurn",
                "message": "执行定时完整生产任务：严格按照 AGENTS.md「任务2：完整生产」步骤B1-B6执行。重点：步骤B5数据池重置必须执行，完成后将报告发送给用户。",
                "timeoutSeconds": 7200
            },
            "delivery": {
                "mode": "none"  # 改为 none，避免 channel 错误
            }
        },
        {
            "name": "LinkedIn评论巡检（每8小时）",
            "schedule": {
                "kind": "every",
                "everyMs": 28800000
            },
            "sessionTarget": "current",
            "payload": {
                "kind": "agentTurn",
                "message": "执行定时评论巡检任务：按 AGENTS.md「任务4：评论巡检」步骤D1-D7执行，拉取最近 7 天发布帖子的新评论，生成摘要推送给用户。",
                "timeoutSeconds": 300
            },
            "delivery": {
                "mode": "none"  # 改为 none，避免 channel 错误
            }
        },
        {
            "name": "历史数据清理（每24小时）",
            "schedule": {
                "kind": "every",
                "everyMs": 86400000
            },
            "sessionTarget": "current",
            "payload": {
                "kind": "agentTurn",
                "message": "执行定时数据清理任务，按 AGENTS.md「任务3：数据清理」步骤C1-C6执行。绝对禁止删除 outputs/reports/ 目录。静默执行。",
                "timeoutSeconds": 120
            },
            "delivery": {
                "mode": "none"
            }
        }
    ]
    
    # 注册所有任务
    success_count = 0
    for task in tasks:
        if register_cron_task(task):
            success_count += 1
    
    print()
    print(f"✅ 成功注册 {success_count}/{len(tasks)} 个任务")
    
    if success_count < len(tasks):
        print("⚠️ 部分任务注册失败，请检查错误信息")
        sys.exit(1)
    
    print()
    print("📋 查看所有任务: openclaw cron list")
    print("🔍 验证任务状态: openclaw cron list | grep sessionTarget")

if __name__ == "__main__":
    main()
