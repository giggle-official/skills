#!/usr/bin/env python3
"""
轻量采集任务 - 每小时执行
运行阶段1和阶段2，将Top 10候选写入今天的数据池
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    # 读取配置
    config_file = Path("config.json")
    if not config_file.exists():
        print("❌ config.json 不存在", file=sys.stderr)
        sys.exit(1)
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    keywords = config['content']['content_focus']['keywords']
    niches = config['content']['content_focus']['niches']
    exclude_keywords = config['content']['content_focus']['exclude_keywords']
    
    # 读取最新的采集结果
    run_id = datetime.now().strftime('%Y%m%d_%H%M')
    raw_file = Path(f"outputs/logs/{run_id}_raw_trends.json")
    
    if not raw_file.exists():
        print(f"❌ 采集结果文件不存在: {raw_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(raw_file, 'r') as f:
        raw_data = json.load(f)
    
    # 采集脚本已经做了关键词匹配和打分
    # 数据结构: raw_data['trends'] 是一个列表，每个元素包含:
    # - title, platform, platform_name, hot, keyword_score, matched_keywords, matched_niches
    all_trends = raw_data.get('trends', [])
    
    if not all_trends:
        print("⚠️ 采集结果为空", file=sys.stderr)
        sys.exit(0)
    
    # 筛选出有关键词匹配分的热点（keyword_score > 0）
    matched_trends = [t for t in all_trends if t.get('keyword_score', 0) > 0]
    
    print(f"📊 总热点数: {len(all_trends)}", file=sys.stderr)
    print(f"📊 匹配关键词/赛道: {len(matched_trends)}", file=sys.stderr)
    
    # 按 relevance_score（关键词匹配分）排序，取 Top 10
    top10 = sorted(matched_trends, key=lambda x: x.get('relevance_score', 0), reverse=True)[:10]
    
    if not top10:
        print("⚠️ 没有匹配的热点，跳过本次采集", file=sys.stderr)
        sys.exit(0)
    
    # 转换为数据池格式
    pool_trends = []
    for t in top10:
        pool_trends.append({
            'title': t['title'],
            'score': t.get('keyword_score', 0),
            'platform': t['platform'],
            'platform_name': t['platform_name'],
            'url': t.get('url', ''),
            'matched_keywords': t.get('matched_keywords', []),
            'matched_niches': t.get('matched_niches', []),
            'used': False
        })
    
    # 追加到数据池
    today = datetime.now().strftime('%Y%m%d')
    pool_file = Path(f"outputs/pool/{today}_trend_pool.json")
    
    if pool_file.exists():
        with open(pool_file, 'r') as f:
            pool = json.load(f)
    else:
        pool = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'last_production_reset': None,
            'collections': []
        }
    
    # 追加新采集
    pool['collections'].append({
        'collect_time': datetime.now().astimezone().isoformat(),
        'trends': pool_trends
    })
    
    # 写回文件
    with open(pool_file, 'w') as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)
    
    # 统计未使用条目
    unused_count = sum(1 for c in pool['collections'] for t in c['trends'] if not t['used'])
    
    print(f"✅ 轻量采集完成 | 数据池未使用条目: {unused_count}", file=sys.stderr)

if __name__ == '__main__':
    main()
