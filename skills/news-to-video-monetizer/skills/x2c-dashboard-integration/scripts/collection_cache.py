#!/usr/bin/env python3
"""
采集数据缓存管理
保存采集结果到 cache/collections/ 目录，保留7天
"""

import json
import os
import glob
from datetime import datetime, timedelta

CACHE_DIR = os.path.expanduser('~/.openclaw/workspace-news-to-video-monetizer/cache/collections')
CACHE_RETENTION_DAYS = 7

def save_collection(collection_id, data):
    """保存采集数据"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    cache_file = os.path.join(CACHE_DIR, f"{collection_id}.json")
    
    cache_data = {
        "collection_id": collection_id,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }
    
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f, indent=2, ensure_ascii=False)
    
    return cache_file

def get_collection(collection_id):
    """获取采集数据"""
    cache_file = os.path.join(CACHE_DIR, f"{collection_id}.json")
    
    if not os.path.exists(cache_file):
        return None
    
    with open(cache_file) as f:
        return json.load(f)

def list_collections(limit=10):
    """列出最近的采集记录"""
    cache_files = glob.glob(os.path.join(CACHE_DIR, "*.json"))
    
    collections = []
    for cache_file in cache_files:
        try:
            with open(cache_file) as f:
                data = json.load(f)
                collections.append(data)
        except:
            continue
    
    # 按时间倒序
    collections.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return collections[:limit]

def cleanup_old_collections():
    """清理过期的采集数据"""
    cutoff_date = datetime.now() - timedelta(days=CACHE_RETENTION_DAYS)
    
    cache_files = glob.glob(os.path.join(CACHE_DIR, "*.json"))
    
    deleted_count = 0
    for cache_file in cache_files:
        try:
            with open(cache_file) as f:
                data = json.load(f)
            
            timestamp = datetime.fromisoformat(data.get('timestamp', ''))
            
            if timestamp < cutoff_date:
                os.remove(cache_file)
                deleted_count += 1
        except:
            continue
    
    return deleted_count

if __name__ == '__main__':
    # 测试
    print("📦 采集数据缓存管理")
    print(f"缓存目录: {CACHE_DIR}")
    print(f"保留天数: {CACHE_RETENTION_DAYS}")
    
    # 清理过期数据
    deleted = cleanup_old_collections()
    print(f"\n🗑️  清理过期数据: {deleted} 个")
    
    # 列出现有缓存
    collections = list_collections()
    print(f"\n📋 现有缓存: {len(collections)} 个")
    for col in collections:
        print(f"  - {col['collection_id']} ({col['timestamp'][:16]})")
