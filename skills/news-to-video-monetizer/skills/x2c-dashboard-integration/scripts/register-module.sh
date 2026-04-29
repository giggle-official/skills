#!/bin/bash
# register-module.sh - 注册所有 agent 模块
set -e

AGENT_ID="${1:-news-to-video-monetizer}"

echo "📝 注册模块: $AGENT_ID"

python3 << EOF
import sqlite3, json, os, uuid, sys

db = sqlite3.connect(os.path.expanduser('~/.claw/shared/shared.db'))

# 定义两大模块
modules = [
    {"name": "X2C Dashboard", "icon": "📊", "description": "收益数据可视化"},
    {"name": "Agent 运行面板", "icon": "🤖", "description": "Agent 运行状态和历史"},
]

for mod in modules:
    # 检查模块是否存在
    cursor = db.execute("SELECT id FROM dashboard_modules WHERE agent_id = ? AND name = ?", 
                       ("$AGENT_ID", mod["name"]))
    existing = cursor.fetchone()
    
    if existing:
        print(f"✅ 模块已存在: {mod['icon']} {mod['name']} ({existing[0]})")
        continue
    
    # 创建模块
    module_id = str(uuid.uuid4())[:8]
    db.execute(
        "INSERT INTO dashboard_modules (id, agent_id, name, icon) VALUES (?, ?, ?, ?)",
        (module_id, "$AGENT_ID", mod["name"], mod["icon"])
    )
    print(f"✅ 创建模块: {mod['icon']} {mod['name']} ({module_id})")
    
    # 为每个模块添加初始组件
    if mod["name"] == "X2C Dashboard":
        # 添加初始 KPI 卡片
        for i, (title, config) in enumerate([
            ("总收入", {"prefix": "$", "trend": "up", "subtitle": "累计收益"}),
            ("今日收益", {"prefix": "$", "trend": "up", "subtitle": "+0% vs 昨日"}),
            ("总播放量", {"suffix": "次", "trend": "up", "subtitle": "全平台"}),
            ("活跃项目", {"suffix": "个", "subtitle": "正在赚钱"}),
        ]):
            widget_id = str(uuid.uuid4())[:8]
            db.execute(
                "INSERT INTO dashboard_widgets (id, module_id, widget_type, title, config, data, position) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (widget_id, module_id, "kpi_card", title, json.dumps(config), json.dumps([0]), i)
            )
    
    elif mod["name"] == "Agent 运行面板":
        # 1. 运行状态 KPI
        for i, (title, config) in enumerate([
            ("运行状态", {"subtitle": "正常运行"}),
            ("今日任务", {"suffix": "个", "subtitle": "已完成 0 个"}),
            ("总任务数", {"suffix": "个", "subtitle": "累计执行"}),
            ("成功率", {"suffix": "%", "subtitle": "任务成功率"}),
        ]):
            widget_id = str(uuid.uuid4())[:8]
            db.execute(
                "INSERT INTO dashboard_widgets (id, module_id, widget_type, title, config, data, position) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (widget_id, module_id, "kpi_card", title, json.dumps(config), json.dumps([0]), i)
            )
        
        # 2. 快捷指令说明
        widget_id = str(uuid.uuid4())[:8]
        db.execute(
            "INSERT INTO dashboard_widgets (id, module_id, widget_type, title, config, data, position) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (widget_id, module_id, "text", "快捷指令", json.dumps({}), 
             json.dumps(["在对话中输入数字或名称执行功能：\\n1️⃣ 一键制作 | 2️⃣ 查看热点 | 3️⃣ 指定话题 | 4️⃣ 查看任务 | 5️⃣ 查看收益 | 6️⃣ 修改配置"]), 
             5)
        )
        
        # 3. 当前配置
        config_stats = [
            {"label": "内容赛道", "value": "未配置"},
            {"label": "关键词", "value": "未配置"},
            {"label": "视频时长", "value": "60秒"},
            {"label": "视频比例", "value": "9:16"},
            {"label": "视频风格", "value": "未配置"},
            {"label": "自动发布", "value": "开启"},
        ]
        widget_id = str(uuid.uuid4())[:8]
        db.execute(
            "INSERT INTO dashboard_widgets (id, module_id, widget_type, title, config, data, position) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (widget_id, module_id, "stat_row", "当前配置", json.dumps({}), json.dumps(config_stats), 10)
        )
        
        # 4. 采集统计
        collection_stats = [
            {"label": "今日采集", "value": "0 条"},
            {"label": "本周采集", "value": "0 条"},
            {"label": "采集平台", "value": "7 个"},
            {"label": "去重率", "value": "0%"},
        ]
        widget_id = str(uuid.uuid4())[:8]
        db.execute(
            "INSERT INTO dashboard_widgets (id, module_id, widget_type, title, config, data, position) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (widget_id, module_id, "stat_row", "采集统计", json.dumps({}), json.dumps(collection_stats), 15)
        )
        
        # 5. 历史任务表格
        task_history = []
        widget_id = str(uuid.uuid4())[:8]
        db.execute(
            "INSERT INTO dashboard_widgets (id, module_id, widget_type, title, config, data, position) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (widget_id, module_id, "table", "历史任务", json.dumps({}), json.dumps(task_history), 20)
        )

db.commit()
db.close()

print(f"\\n✅ 所有模块已注册")
EOF
