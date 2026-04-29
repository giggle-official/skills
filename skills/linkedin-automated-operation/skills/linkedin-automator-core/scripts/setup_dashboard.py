#!/usr/bin/env python3
"""
Dashboard 完整设置脚本
用于首次配置或修复 Dashboard
"""

import sys
import json
import os
import time
import uuid
from pathlib import Path

def main():
    print("📊 开始 Dashboard 设置...")
    print()
    
    # 1. 检查 claw-dashboard skill
    skill_path = Path.home() / ".openclaw" / "skills" / "claw-dashboard"
    if not skill_path.exists():
        print("❌ claw-dashboard skill 未安装")
        print("请运行: openclaw skills install claw-dashboard")
        sys.exit(1)
    
    sys.path.insert(0, str(skill_path))
    
    try:
        from src.hub import manager
        from src.storage.db import get_db
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保 claw-dashboard 已正确安装")
        sys.exit(1)
    
    # 2. 启动 Hub 和 Tunnel
    print("🚀 启动 Hub 服务...")
    status = manager.get_status()
    
    if not status.get("hub", {}).get("running"):
        manager.start_hub()
        time.sleep(2)
    
    if not status.get("tunnel", {}).get("running"):
        manager.start_tunnel()
        time.sleep(3)
    
    status = manager.get_status()
    
    if not status.get("hub", {}).get("healthy"):
        print("❌ Hub 启动失败")
        sys.exit(1)
    
    print(f"✅ Hub 已启动: {status.get('hub', {}).get('local_url')}")
    print(f"✅ Tunnel 已启动: {status.get('public_url')}")
    print()
    
    # 3. 注册模块
    print("📝 注册 Dashboard 模块...")
    db = get_db()
    
    existing = db.execute(
        "SELECT id FROM dashboard_modules WHERE agent_id = ?",
        ("linkedin-automator",)
    ).fetchone()
    
    if existing:
        module_id = existing[0]
        print(f"  ✅ 模块已存在: {module_id}")
    else:
        module_id = str(uuid.uuid4())[:8]
        db.execute(
            "INSERT INTO dashboard_modules (id, agent_id, name, icon) VALUES (?, ?, ?, ?)",
            (module_id, "linkedin-automator", "LinkedIn 运营中心", "📌")
        )
        db.commit()
        print(f"  ✅ 模块已创建: {module_id}")
    
    # 4. 注册 Widgets
    print("📊 注册 Widgets...")
    
    widget_defs = [
        ("total_videos", "kpi_card", "累计视频", {"value": 0, "trend": "up"}),
        ("today_trends", "kpi_card", "今日热点", {"value": 0}),
        ("pending_comments", "kpi_card", "待处理评论", {"value": 0}),
        ("production_trend", "line_chart", "7天生产趋势", {
            "labels": ["周一","周二","周三","周四","周五","周六","周日"],
            "dataset_label": "视频数",
            "color": "#6366f1",
            "bg_color": "rgba(99,102,241,0.1)"
        }),
        ("niche_distribution", "pie_chart", "赛道分布", {
            "labels": ["科技数码","职场成长","教育知识"],
            "colors": ["#6366f1", "#22c55e", "#eab308"]
        }),
        ("recent_videos", "table", "最近发布", {
            "columns": ["标题","发布时间","状态","PostID"],
            "rows": []
        }),
        ("recent_comments", "table", "最新评论", {
            "columns": ["帖子","评论者","内容","时间"],
            "rows": []
        }),
        ("stats", "stat_row", "运营统计", [
            {"label": "平均耗时", "value": "--"},
            {"label": "成功率", "value": "--"},
            {"label": "风格指纹", "value": "学习中"}
        ])
    ]
    
    widget_ids = {}
    for key, wtype, title, default_data in widget_defs:
        existing_w = db.execute(
            "SELECT id FROM dashboard_widgets WHERE module_id = ? AND title = ?",
            (module_id, title)
        ).fetchone()
        
        if existing_w:
            widget_ids[key] = existing_w[0]
            print(f"  ✅ Widget 已存在: {title}")
        else:
            wid = str(uuid.uuid4())[:8]
            db.execute(
                "INSERT INTO dashboard_widgets (id, module_id, widget_type, title, data, config) VALUES (?, ?, ?, ?, ?, ?)",
                (wid, module_id, wtype, title, json.dumps(default_data, ensure_ascii=False), "{}")
            )
            widget_ids[key] = wid
            print(f"  ✅ Widget 已创建: {title}")
    
    db.commit()
    print()
    
    # 5. 更新 config.json
    print("💾 更新 config.json...")
    
    config_file = Path("config.json")
    if not config_file.exists():
        print("❌ config.json 不存在")
        sys.exit(1)
    
    with open(config_file, "r") as f:
        config = json.load(f)
    
    config["dashboard"] = {
        "enabled": True,
        "file": "outputs/dashboard/index.html",
        "module_id": module_id,
        "widget_ids": widget_ids,
        "public_url": status.get("public_url", ""),
        "local_url": status.get("hub", {}).get("local_url", "http://localhost:3000")
    }
    
    with open(config_file, "w") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ config.json 已更新")
    print()
    
    # 6. 完成
    print("=" * 60)
    print("✅ Dashboard 设置完成！")
    print()
    print(f"📊 公网地址: {status.get('public_url')}")
    print(f"🏠 本地地址: {status.get('hub', {}).get('local_url')}")
    print()
    print("💡 提示:")
    print("  - Dashboard 需要等第一次内容生产完成后才会显示数据")
    print("  - 运行 'python3 skills/linkedin-automator-core/scripts/dashboard_integration.py update' 手动更新数据")
    print("=" * 60)

if __name__ == '__main__':
    main()
