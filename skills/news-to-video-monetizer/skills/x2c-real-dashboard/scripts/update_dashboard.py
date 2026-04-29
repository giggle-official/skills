#!/usr/bin/env python3
"""
X2CReel Dashboard 数据更新脚本（增强版）
包含所有数据源和优化的布局
"""

import sqlite3
import json
import os
import subprocess
import sys
import uuid

def get_x2c_data(api_key, script_name, *args):
    """调用 x2c-real-dashboard 脚本"""
    env = os.environ.copy()
    env['X2C_API_KEY'] = api_key
    
    script_path = os.path.expanduser(f'~/.openclaw/skills/x2c-real-dashboard/scripts/{script_name}')
    cmd = ['bash', script_path] + list(args)
    
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error calling {script_name}: {result.stderr}", file=sys.stderr)
        return None
    
    try:
        data = json.loads(result.stdout)
        if not data.get('success'):
            print(f"❌ API error: {data.get('error')}", file=sys.stderr)
            return None
        return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}", file=sys.stderr)
        return None

def update_dashboard(api_key):
    """更新所有 Dashboard 组件"""
    
    print("📊 正在获取 X2C 数据...")
    
    # 获取所有数据
    overview = get_x2c_data(api_key, 'overview.sh')
    trend_30d = get_x2c_data(api_key, 'trend.sh', '30')
    platforms = get_x2c_data(api_key, 'platform-breakdown.sh')
    projects = get_x2c_data(api_key, 'earning-projects.sh', '1', '15')
    activity = get_x2c_data(api_key, 'recent-activity.sh', '10')
    
    if not all([overview, trend_30d, platforms, projects, activity]):
        return False
    
    # 连接数据库
    db_path = os.path.expanduser('~/.claw/shared/shared.db')
    db = sqlite3.connect(db_path)
    
    # 查找模块
    cursor = db.execute("SELECT id FROM dashboard_modules WHERE agent_id = ?", ("news-to-video-monetizer",))
    row = cursor.fetchone()
    if not row:
        print("❌ 模块未找到", file=sys.stderr)
        return False
    
    module_id = row[0]
    
    # 提取数据
    revenue = overview['revenue']
    projects_data = overview['projects']
    views = overview['views']
    production = overview['production']
    mining = overview['mining']
    x2c_price = overview['x2c_price']
    
    # 1. 更新 KPI 卡片
    kpi_updates = [
        ("总收入", [round(revenue['historical_usd'], 2)], 
         {"prefix": "$", "trend": "up", "subtitle": f"ROI {production['roi_percent']}%"}),
        ("今日收益", [round(revenue['today_usd'], 2)], 
         {"prefix": "$", "trend": "up" if revenue['vs_yesterday_percent'] >= 0 else "down", 
          "subtitle": f"{revenue['vs_yesterday_percent']:+.1f}% vs 昨日"}),
        ("总播放量", [views['total']], 
         {"suffix": "次", "trend": "up", "subtitle": "全平台"}),
        ("活跃项目", [projects_data['active_earning']], 
         {"suffix": "个", "subtitle": f"共 {projects_data['total']} 个项目"}),
    ]
    
    for title, new_data, new_config in kpi_updates:
        cursor = db.execute("SELECT id, config FROM dashboard_widgets WHERE module_id = ? AND title = ?", 
                           (module_id, title))
        row = cursor.fetchone()
        if row:
            widget_id, old_config = row
            merged_config = json.loads(old_config)
            merged_config.update(new_config)
            db.execute(
                "UPDATE dashboard_widgets SET data = ?, config = ?, updated_at = datetime('now') WHERE id = ?",
                (json.dumps(new_data), json.dumps(merged_config), widget_id)
            )
    
    # 2. 更新 30日趋势图
    trend_data = trend_30d['trend']
    labels_30d = [t['date'][5:] for t in trend_data]
    values_30d = [round(t['revenue_usd'], 2) for t in trend_data]
    
    cursor = db.execute("SELECT id FROM dashboard_widgets WHERE module_id = ? AND widget_type = 'line_chart'", 
                       (module_id,))
    row = cursor.fetchone()
    if row:
        widget_id = row[0]
        db.execute(
            "UPDATE dashboard_widgets SET data = ?, config = ?, updated_at = datetime('now') WHERE id = ?",
            (json.dumps(values_30d), 
             json.dumps({"labels": labels_30d, "color": "#10b981", "dataset_label": "每日收益", "prefix": "$"}), 
             widget_id)
        )
    
    # 3. 更新收益对比柱状图
    monthly_avg = revenue['monthly_usd'] / 30
    comparison_labels = ["今日", "昨日", "月均"]
    comparison_values = [
        round(revenue['today_usd'], 2),
        round(revenue['yesterday_usd'], 2),
        round(monthly_avg, 2)
    ]
    
    cursor = db.execute("SELECT id FROM dashboard_widgets WHERE module_id = ? AND widget_type = 'bar_chart'", 
                       (module_id,))
    row = cursor.fetchone()
    if row:
        widget_id = row[0]
        db.execute(
            "UPDATE dashboard_widgets SET data = ?, config = ?, updated_at = datetime('now') WHERE id = ?",
            (json.dumps(comparison_values), 
             json.dumps({"labels": comparison_labels, "color": "#3b82f6"}), 
             widget_id)
        )
    
    # 4. 更新平台播放饼图
    platform_labels = [p['service'] for p in platforms['platforms'] if p['views'] > 0]
    platform_values = [p['views'] for p in platforms['platforms'] if p['views'] > 0]
    platform_colors = ["#3b82f6", "#ef4444", "#8b5cf6", "#f59e0b", "#10b981"]
    
    cursor = db.execute("SELECT id FROM dashboard_widgets WHERE module_id = ? AND widget_type = 'pie_chart'", 
                       (module_id,))
    row = cursor.fetchone()
    if row:
        widget_id = row[0]
        db.execute(
            "UPDATE dashboard_widgets SET data = ?, config = ?, updated_at = datetime('now') WHERE id = ?",
            (json.dumps(platform_values), 
             json.dumps({"labels": platform_labels, "colors": platform_colors[:len(platform_labels)]}), 
             widget_id)
        )
    
    # 5. 更新挖矿状态
    mining_stats = [
        {"label": "待释放", "value": f"{mining['pending_x2c']:,.0f} X2C (${mining['pending_usd']:.2f})"},
        {"label": "已释放", "value": f"{mining['released_x2c']:,.0f} X2C (${mining['released_usd']:.2f})"},
        {"label": "锁定中", "value": f"{mining['locked_x2c']:,.0f} X2C (${mining['locked_x2c'] * x2c_price:.2f})"},
    ]
    
    cursor = db.execute("SELECT id FROM dashboard_widgets WHERE module_id = ? AND title = '挖矿状态'", 
                       (module_id,))
    row = cursor.fetchone()
    if row:
        widget_id = row[0]
        db.execute(
            "UPDATE dashboard_widgets SET data = ?, updated_at = datetime('now') WHERE id = ?",
            (json.dumps(mining_stats), widget_id)
        )
    
    # 6. 更新成本与收益
    cost_revenue_stats = [
        {"label": "总支出", "value": f"${production['net_expense_usd']:.2f}"},
        {"label": "总收入", "value": f"${revenue['historical_usd']:.2f}"},
        {"label": "净利润", "value": f"${revenue['historical_usd'] - production['net_expense_usd']:.2f}"},
        {"label": "ROI", "value": f"{production['roi_percent']}%"},
    ]
    
    cursor = db.execute("SELECT id FROM dashboard_widgets WHERE module_id = ? AND title = '成本与收益'", 
                       (module_id,))
    row = cursor.fetchone()
    if row:
        widget_id = row[0]
        db.execute(
            "UPDATE dashboard_widgets SET data = ?, updated_at = datetime('now') WHERE id = ?",
            (json.dumps(cost_revenue_stats), widget_id)
        )
    
    # 7. 更新项目统计
    project_stats = [
        {"label": "总项目", "value": f"{projects_data['total']} 个"},
        {"label": "已发行", "value": f"{projects_data['distributed']} 个"},
        {"label": "正在赚钱", "value": f"{projects_data['active_earning']} 个"},
        {"label": "本周新增", "value": f"{projects_data['weekly_new']} 个"},
    ]
    
    cursor = db.execute("SELECT id FROM dashboard_widgets WHERE module_id = ? AND title = '项目统计'", 
                       (module_id,))
    row = cursor.fetchone()
    if row:
        widget_id = row[0]
        db.execute(
            "UPDATE dashboard_widgets SET data = ?, updated_at = datetime('now') WHERE id = ?",
            (json.dumps(project_stats), widget_id)
        )
    
    # 8. 更新最近交易
    tx_type_map = {
        "mining_income": "挖矿",
        "x2c_release": "释放",
        "commission": "佣金",
        "referral": "推荐",
        "royalty": "版税",
        "production": "制作",
        "production_refund": "退款"
    }
    
    activity_data = []
    for item in activity['items'][:5]:
        tx_time = item['transaction_at'][:16].replace('T', ' ')[5:]
        activity_data.append({
            "time": tx_time,
            "action": tx_type_map.get(item['tx_type'], item['tx_type']),
            "symbol": item['currency'],
            "qty": f"{item['amount']:.2f}",
            "price": "",
            "strategy": item['title'],
            "logic": f"{item['direction']} | {item['tx_type']}"
        })
    
    cursor = db.execute("SELECT id FROM dashboard_widgets WHERE module_id = ? AND widget_type = 'activity_log'", 
                       (module_id,))
    row = cursor.fetchone()
    if row:
        widget_id = row[0]
        db.execute(
            "UPDATE dashboard_widgets SET data = ?, updated_at = datetime('now') WHERE id = ?",
            (json.dumps(activity_data), widget_id)
        )
    
    # 9. 更新赚钱作品列表
    items = projects['items']
    table_data = []
    for item in items:
        avg_7d = sum(item['trend7d']) / len(item['trend7d'])
        trend_emoji = "📈" if item['today_usd'] >= avg_7d else "📉"
        
        pv = item['platform_views']
        
        table_data.append({
            "作品": item['title'][:18] + "..." if len(item['title']) > 18 else item['title'],
            "今日": f"${item['today_usd']:.2f}",
            "总收益": f"${item['total_usd']:.2f}",
            "播放": f"{item['total_views']:,}",
            "趋势": trend_emoji,
            "TikTok": f"{pv['tiktok']:,}" if pv['tiktok'] > 0 else "-",
            "YouTube": f"{pv['youtube']:,}" if pv['youtube'] > 0 else "-",
            "Instagram": f"{pv['instagram']:,}" if pv['instagram'] > 0 else "-"
        })
    
    cursor = db.execute("SELECT id FROM dashboard_widgets WHERE module_id = ? AND title LIKE '%作品%'", 
                       (module_id,))
    row = cursor.fetchone()
    if row:
        widget_id = row[0]
        db.execute(
            "UPDATE dashboard_widgets SET data = ?, updated_at = datetime('now') WHERE id = ?",
            (json.dumps(table_data), widget_id)
        )
    
    db.commit()
    db.close()
    
    print("✅ Dashboard 数据已更新！\n")
    print(f"📊 总收入: ${revenue['historical_usd']:.2f}")
    print(f"💰 今日收益: ${revenue['today_usd']:.2f} ({revenue['vs_yesterday_percent']:+.1f}%)")
    print(f"📈 ROI: {production['roi_percent']}%")
    print(f"🎬 活跃项目: {projects_data['active_earning']}/{projects_data['total']}")
    print(f"👀 总播放量: {views['total']:,}")
    print(f"⛏️  挖矿锁定: {mining['locked_x2c']:,.0f} X2C")
    
    return True

def get_dashboard_url():
    """获取 Dashboard 公共 URL"""
    config_path = os.path.expanduser('~/.claw/config/tunnel.json')
    if not os.path.exists(config_path):
        return None
    
    with open(config_path) as f:
        config = json.load(f)
    
    return config.get('public_url')

if __name__ == '__main__':
    # 读取 API key
    workspace_config_path = os.path.expanduser('~/.openclaw/workspace-news-to-video-monetizer/config.json')
    
    if not os.path.exists(workspace_config_path):
        print("❌ Workspace config not found", file=sys.stderr)
        sys.exit(1)
    
    with open(workspace_config_path) as f:
        config = json.load(f)
    
    api_key = config.get('x2c', {}).get('api_key')
    if not api_key:
        print("❌ X2C API Key not configured", file=sys.stderr)
        sys.exit(1)
    
    # 更新 Dashboard
    if update_dashboard(api_key):
        url = get_dashboard_url()
        if url:
            print(f"\n📊 Dashboard: {url}")
        sys.exit(0)
    else:
        sys.exit(1)
