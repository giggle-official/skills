#!/usr/bin/env python3
"""
检查自动首评失败通知并发送给用户
"""

import json
import os
import glob
from pathlib import Path

def check_and_notify():
    log_dir = Path('outputs/logs')
    dated_files = sorted(glob.glob(str(log_dir / 'auto_comment_failures_*.json')))
    legacy_file = log_dir / 'auto_comment_failures.json'

    # 优先读取按日期写入的新文件；若不存在则回退旧文件名
    target_files = dated_files if dated_files else ([str(legacy_file)] if legacy_file.exists() else [])
    if not target_files:
        return None

    failures = []
    for file_path in target_files:
        try:
            with open(file_path, encoding='utf-8') as f:
                content = json.load(f)
                if isinstance(content, list):
                    failures.extend(content)
        except Exception:
            continue
    
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
    
    # 清空失败文件（避免重复通知）
    for file_path in target_files:
        try:
            os.remove(file_path)
        except Exception:
            pass
    
    return msg

if __name__ == '__main__':
    msg = check_and_notify()
    if msg:
        print(msg)
