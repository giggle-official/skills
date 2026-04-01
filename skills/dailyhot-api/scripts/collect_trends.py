#!/usr/bin/env python3
"""
全网热点趋势收集脚本
从 DailyHotApi 批量获取多平台热榜数据，汇总后输出 JSON

用法:
  python3 collect_trends.py
  python3 collect_trends.py --platforms douyin weibo toutiao
  python3 collect_trends.py --top 20
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

# 默认采集平台及权重
DEFAULT_PLATFORMS = {
    "douyin":       {"name": "抖音",     "weight": 1.5, "category": "短视频"},
    "weibo":        {"name": "微博",     "weight": 1.3, "category": "社交媒体"},
    "toutiao":      {"name": "今日头条", "weight": 1.2, "category": "新闻资讯"},
    "zhihu":        {"name": "知乎",     "weight": 1.1, "category": "社交媒体"},
    "bilibili":     {"name": "B站",      "weight": 1.0, "category": "短视频"},
    "baidu":        {"name": "百度",     "weight": 1.0, "category": "搜索引擎"},
    "kuaishou":     {"name": "快手",     "weight": 0.9, "category": "短视频"},
    "qq-news":      {"name": "腾讯新闻", "weight": 0.8, "category": "新闻资讯"},
    "thepaper":     {"name": "澎湃新闻", "weight": 0.8, "category": "新闻资讯"},
    "36kr":         {"name": "36氪",     "weight": 0.7, "category": "科技财经"},
}

def fetch_platform(base_url, platform_key, timeout=15):
    """获取单个平台的热榜数据"""
    url = f"{base_url}/{platform_key}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DailyHot-Collector/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("code") == 200:
                return data
    except Exception as e:
        print(f"⚠️ {platform_key} 采集失败: {e}", file=sys.stderr)
    return None

def collect_all(base_url, platforms, top_per_platform=10, content_focus=None):
    """批量采集多平台热榜，支持内容方向过滤"""
    all_trends = []
    filtered_out = 0
    success_count = 0
    fail_count = 0

    # 解析内容方向配置
    niches = []
    keywords = []
    exclude_keywords = []
    if content_focus:
        niches = [n.lower() for n in content_focus.get("niches", [])]
        keywords = [k.lower() for k in content_focus.get("keywords", [])]
        exclude_keywords = [k.lower() for k in content_focus.get("exclude_keywords", [])]

    for key, meta in platforms.items():
        result = fetch_platform(base_url, key)
        if result and result.get("data"):
            success_count += 1
            for i, item in enumerate(result["data"][:top_per_platform]):
                title = item.get("title", "")
                title_lower = title.lower()

                # 排除关键词过滤
                if exclude_keywords and any(ek in title_lower for ek in exclude_keywords):
                    filtered_out += 1
                    continue

                # 计算内容匹配分
                keyword_score = 0
                matched_keywords = []
                matched_niches = []

                for kw in keywords:
                    if kw in title_lower:
                        keyword_score += 15
                        matched_keywords.append(kw)

                for niche in niches:
                    if niche in title_lower:
                        keyword_score += 10
                        matched_niches.append(niche)

                trend = {
                    "title": title,
                    "platform": key,
                    "platform_name": meta["name"],
                    "category": meta["category"],
                    "hot": item.get("hot", 0),
                    "rank_in_platform": i + 1,
                    "url": item.get("url", ""),
                    "cover": item.get("cover", ""),
                    "weight": meta["weight"],
                    "keyword_score": keyword_score,
                    "matched_keywords": matched_keywords,
                    "matched_niches": matched_niches,
                }
                all_trends.append(trend)
        else:
            fail_count += 1

    # 按加权热度 + 关键词匹配分排序
    for t in all_trends:
        raw_hot = t["hot"] if isinstance(t["hot"], (int, float)) else 0
        t["weighted_score"] = raw_hot * t["weight"]
        # 综合分 = 归一化热度分 + 关键词匹配分
        t["relevance_score"] = t["keyword_score"]

    all_trends.sort(key=lambda x: (x["relevance_score"], x["weighted_score"]), reverse=True)

    return {
        "collect_time": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "platforms_success": success_count,
        "platforms_failed": fail_count,
        "total_trends": len(all_trends),
        "filtered_out": filtered_out,
        "content_focus_applied": bool(content_focus),
        "trends": all_trends,
    }

def main():
    parser = argparse.ArgumentParser(description="全网热点趋势收集")
    parser.add_argument("--port", type=int, default=6688, help="DailyHotApi 端口 (默认 6688)")
    parser.add_argument("--platforms", nargs="+", help="指定采集平台 (默认全部)")
    parser.add_argument("--top", type=int, default=10, help="每个平台取前 N 条 (默认 10)")
    parser.add_argument("--output", type=str, help="输出到文件 (默认 stdout)")
    parser.add_argument("--config", type=str, help="config.json 路径，读取 content_focus 进行内容过滤")
    args = parser.parse_args()

    # 读取实际端口
    import os
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    port_file = os.path.join(skill_dir, ".data", "port")
    if os.path.exists(port_file):
        with open(port_file) as f:
            args.port = int(f.read().strip())

    base_url = f"http://localhost:{args.port}"

    # 筛选平台
    if args.platforms:
        platforms = {k: v for k, v in DEFAULT_PLATFORMS.items() if k in args.platforms}
    else:
        platforms = DEFAULT_PLATFORMS

    # 读取用户内容方向配置
    content_focus = None
    if args.config and os.path.exists(args.config):
        try:
            with open(args.config, "r", encoding="utf-8") as f:
                config = json.load(f)
                content_focus = config.get("content", {}).get("content_focus")
                if content_focus:
                    print(f"📌 已加载内容方向配置: 赛道={content_focus.get('niches', [])}, 关键词={content_focus.get('keywords', [])[:5]}..., 排除={content_focus.get('exclude_keywords', [])}", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ 配置文件读取失败: {e}", file=sys.stderr)

    # 采集
    result = collect_all(base_url, platforms, args.top, content_focus=content_focus)

    # 输出
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 结果已保存到 {args.output}", file=sys.stderr)
    else:
        print(output)

if __name__ == "__main__":
    main()
