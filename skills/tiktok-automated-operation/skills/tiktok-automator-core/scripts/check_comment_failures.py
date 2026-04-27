#!/usr/bin/env python3
"""
检查自动首评失败通知并发送给用户
"""

import json
import os
from pathlib import Path

def check_and_notify():
    notify_file = 'outputs/logs/auto_comment_failures.json'
    
    if not os.path.exists(notify_file):
        return None
    
    with open(notify_file) as f:
        failures = json.load(f)
    
    if not failures:
        return None
    
    # 生成通知消息
    msg = "⚠️ **自动首评失败通知**\n\n"
    msg += f"以下 {len(failures)} 个视频的自动首评失败：\n\n"
    
    for i, fail in enumerate(failures, 1):
        msg += f"{i}. **{fail['trend_title']}**\n"
        msg += f"   - 时间: {fail['timestamp']}\n"
        msg += f"   - 原因: {fail['error']}\n\n"
    
    msg += "💡 **建议**：\n"
    msg += "- 可以手动访问视频链接发布评论\n"
    msg += "- 或等待下次定时生产时自动重试\n"
    
    # 清空失败文件
    os.remove(notify_file)
    
    return msg

if __name__ == '__main__':
    msg = check_and_notify()
    if msg:
        print(msg)
