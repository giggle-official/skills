#!/usr/bin/env python3
"""
数据分析和统计模块
提供关键词效果、平台统计、视频效果等分析
"""

import json
import os
import glob
from datetime import datetime, timedelta
from collections import defaultdict

WORKSPACE = os.path.expanduser('~/.openclaw/workspace-news-to-video-monetizer')

def analyze_keywords():
    """分析关键词效果"""
    
    # 读取所有采集缓存
    cache_dir = os.path.join(WORKSPACE, 'cache/collections')
    cache_files = glob.glob(os.path.join(cache_dir, '*.json'))
    
    keyword_stats = defaultdict(lambda: {
        'total_searches': 0,
        'total_matches': 0,
        'match_rate': 0,
        'selected_count': 0
    })
    
    for cache_file in cache_files:
        try:
            with open(cache_file) as f:
                data = json.load(f)
            
            keywords = data['data'].get('keywords', [])
            matched = data['data']['summary'].get('matched_topics', 0)
            
            for keyword in keywords:
                keyword_stats[keyword]['total_searches'] += 1
                keyword_stats[keyword]['total_matches'] += matched
        except:
            continue
    
    # 计算匹配率
    for keyword, stats in keyword_stats.items():
        if stats['total_searches'] > 0:
            stats['match_rate'] = round(stats['total_matches'] / stats['total_searches'] * 100, 2)
    
    # 保存分析结果
    today = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(WORKSPACE, 'analytics/keywords', f'KEYWORD-{today}.json')
    
    with open(output_file, 'w') as f:
        json.dump({
            'date': today,
            'keywords': dict(keyword_stats)
        }, f, indent=2, ensure_ascii=False)
    
    return keyword_stats

def analyze_platforms():
    """分析平台采集统计"""
    
    cache_dir = os.path.join(WORKSPACE, 'cache/collections')
    cache_files = glob.glob(os.path.join(cache_dir, '*.json'))
    
    platform_stats = defaultdict(lambda: {
        'total_collections': 0,
        'total_topics': 0,
        'total_matches': 0,
        'success_count': 0,
        'fail_count': 0,
        'avg_topics': 0,
        'match_rate': 0
    })
    
    for cache_file in cache_files:
        try:
            with open(cache_file) as f:
                data = json.load(f)
            
            platforms = data['data'].get('platforms', {})
            
            for platform, info in platforms.items():
                stats = platform_stats[platform]
                stats['total_collections'] += 1
                stats['total_topics'] += info.get('total', 0)
                stats['total_matches'] += info.get('matched', 0)
                
                if info.get('total', 0) > 0:
                    stats['success_count'] += 1
                else:
                    stats['fail_count'] += 1
        except:
            continue
    
    # 计算平均值和匹配率
    for platform, stats in platform_stats.items():
        if stats['total_collections'] > 0:
            stats['avg_topics'] = round(stats['total_topics'] / stats['total_collections'], 1)
        if stats['total_topics'] > 0:
            stats['match_rate'] = round(stats['total_matches'] / stats['total_topics'] * 100, 2)
    
    # 保存分析结果
    today = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(WORKSPACE, 'analytics/platforms', f'PLATFORM-{today}.json')
    
    with open(output_file, 'w') as f:
        json.dump({
            'date': today,
            'platforms': dict(platform_stats)
        }, f, indent=2, ensure_ascii=False)
    
    return platform_stats

def analyze_video_performance():
    """分析视频效果（需要 X2C API 数据）"""
    
    tasks_dir = os.path.join(WORKSPACE, 'tasks')
    task_files = glob.glob(os.path.join(tasks_dir, '*.json'))
    
    style_stats = defaultdict(lambda: {
        'count': 0,
        'total_cost': 0,
        'total_revenue': 0,
        'avg_roi': 0
    })
    
    for task_file in task_files:
        try:
            with open(task_file) as f:
                task = json.load(f)
            
            if task.get('status') != 'completed':
                continue
            
            style = task['config_snapshot'].get('style', 'unknown')
            cost = task['costs_total'].get('usd', 0)
            
            stats = style_stats[style]
            stats['count'] += 1
            stats['total_cost'] += cost
            # revenue 需要从 X2C API 获取
        except:
            continue
    
    # 保存分析结果
    today = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(WORKSPACE, 'analytics/videos', f'VIDEO-{today}.json')
    
    with open(output_file, 'w') as f:
        json.dump({
            'date': today,
            'styles': dict(style_stats)
        }, f, indent=2, ensure_ascii=False)
    
    return style_stats

def generate_roi_report(month=None):
    """生成成本收益报告"""
    
    if month is None:
        month = datetime.now().strftime('%Y-%m')
    
    tasks_dir = os.path.join(WORKSPACE, 'tasks')
    task_files = glob.glob(os.path.join(tasks_dir, '*.json'))
    
    report = {
        'month': month,
        'total_tasks': 0,
        'completed_tasks': 0,
        'failed_tasks': 0,
        'total_cost_credits': 0,
        'total_cost_usd': 0,
        'total_revenue_usd': 0,
        'net_profit_usd': 0,
        'roi_percent': 0,
        'avg_cost_per_video': 0,
        'avg_revenue_per_video': 0
    }
    
    for task_file in task_files:
        try:
            with open(task_file) as f:
                task = json.load(f)
            
            # 只统计当月的任务
            created_at = task.get('created_at', '')
            if not created_at.startswith(month):
                continue
            
            report['total_tasks'] += 1
            
            if task.get('status') == 'completed':
                report['completed_tasks'] += 1
            elif task.get('status') == 'failed':
                report['failed_tasks'] += 1
            
            report['total_cost_credits'] += task['costs_total'].get('credits', 0)
            report['total_cost_usd'] += task['costs_total'].get('usd', 0)
        except:
            continue
    
    # 计算平均值和 ROI
    if report['completed_tasks'] > 0:
        report['avg_cost_per_video'] = round(report['total_cost_usd'] / report['completed_tasks'], 2)
    
    # revenue 需要从 X2C API 获取
    # 这里暂时使用示例数据
    if report['total_cost_usd'] > 0:
        report['roi_percent'] = round((report['total_revenue_usd'] - report['total_cost_usd']) / report['total_cost_usd'] * 100, 2)
    
    # 保存报告
    output_file = os.path.join(WORKSPACE, 'reports/roi', f'ROI-{month}.json')
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    return report

if __name__ == '__main__':
    print("📊 数据分析模块\n")
    
    print("1️⃣ 关键词效果分析...")
    keywords = analyze_keywords()
    print(f"   分析了 {len(keywords)} 个关键词")
    
    print("\n2️⃣ 平台采集统计...")
    platforms = analyze_platforms()
    print(f"   分析了 {len(platforms)} 个平台")
    
    print("\n3️⃣ 视频效果分析...")
    videos = analyze_video_performance()
    print(f"   分析了 {len(videos)} 种风格")
    
    print("\n4️⃣ 成本收益报告...")
    roi = generate_roi_report()
    print(f"   本月任务: {roi['total_tasks']} 个")
    print(f"   总成本: ${roi['total_cost_usd']:.2f}")
    
    print("\n✅ 分析完成！")
