#!/usr/bin/env python3
"""
自动首评任务 - 后台执行（优化版）
智能等待 TikTok 视频 ID 生成后自动发布首条评论
"""

import sys, os, json, time, subprocess
from datetime import datetime, timedelta
from pathlib import Path

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def get_real_video_id_smart(publish_time_iso, x2c_key, max_wait_minutes=35, check_interval_minutes=2):
    """
    智能轮询获取真实视频 ID
    
    Args:
        publish_time_iso: 视频发布时间（ISO 格式）
        x2c_key: X2C API Key
        max_wait_minutes: 最大等待时间（分钟）
        check_interval_minutes: 检查间隔（分钟）
    
    Returns:
        video_id: 真实视频 ID，失败返回 None
    """
    publish_time = datetime.fromisoformat(publish_time_iso.replace('Z', '+00:00'))
    now = datetime.now(publish_time.tzinfo)
    elapsed_minutes = (now - publish_time).total_seconds() / 60
    
    log(f"视频发布时间: {publish_time_iso}")
    log(f"当前已过时间: {elapsed_minutes:.1f} 分钟")
    
    # 如果已经过了 30 分钟，立即开始检查
    if elapsed_minutes >= 30:
        log("✅ 已超过 30 分钟，立即开始检查")
        initial_wait = 0
    else:
        # 否则等待到 30 分钟
        initial_wait = 30 - elapsed_minutes
        log(f"⏳ 还需等待 {initial_wait:.1f} 分钟后开始检查")
        time.sleep(initial_wait * 60)
    
    # 开始轮询检查
    attempts = 0
    max_attempts = int((max_wait_minutes - 30) / check_interval_minutes) + 1
    
    while attempts < max_attempts:
        attempts += 1
        log(f"🔍 尝试获取真实 ID (第 {attempts}/{max_attempts} 次)...")
        
        env = {**os.environ, 'X2C_API_KEY': x2c_key}
        result = subprocess.run(
            ['python3', 'skills/x2c-socialposter/scripts/x2c_social.py',
             '--action', 'posts', '--platform', 'tiktok'],
            capture_output=True, text=True, env=env, timeout=30
        )
        
        try:
            data = json.loads(result.stdout)
            if data.get('success') and data.get('posts'):
                # 查找发布时间最接近的视频
                posts = data['posts']
                
                # 按创建时间排序
                posts_sorted = sorted(posts, 
                                    key=lambda x: x.get('created', ''), 
                                    reverse=True)
                
                # 检查最新的 5 个视频
                for post in posts_sorted[:5]:
                    post_created = post.get('created', '')
                    video_id = post.get('id') or post.get('itemId')
                    
                    if not video_id or not str(video_id).isdigit():
                        continue
                    
                    # 检查创建时间是否在发布时间前后 5 分钟内
                    try:
                        post_time = datetime.fromisoformat(post_created.replace('Z', '+00:00'))
                        time_diff = abs((post_time - publish_time).total_seconds())
                        
                        if time_diff <= 300:  # 5 分钟内
                            log(f"✅ 找到匹配视频 ID: {video_id}")
                            log(f"   视频创建时间: {post_created}")
                            log(f"   时间差: {time_diff:.0f} 秒")
                            return video_id
                    except Exception as e:
                        log(f"   时间解析失败: {e}")
                        continue
                
                log(f"   未找到匹配的视频（检查了 {len(posts_sorted[:5])} 个）")
        except Exception as e:
            log(f"❌ 解析失败: {e}")
        
        if attempts < max_attempts:
            log(f"⏳ {check_interval_minutes} 分钟后重试...")
            time.sleep(check_interval_minutes * 60)
    
    log("❌ 达到最大重试次数，放弃获取")
    return None

def post_comment(video_id, comment_text, x2c_key):
    """发布评论"""
    log(f"💬 正在发布评论: {comment_text[:50]}...")
    
    env = {**os.environ, 'X2C_API_KEY': x2c_key}
    result = subprocess.run(
        ['python3', 'skills/x2c-socialposter/scripts/x2c_social.py',
         '--action', 'comment',
         '--post-id', str(video_id),
         '--platforms', 'tiktok',
         '--comment', comment_text],
        capture_output=True, text=True, env=env, timeout=30
    )
    
    try:
        data = json.loads(result.stdout)
        if data.get('success'):
            log("✅ 评论发布成功")
            return True, None
        else:
            error_msg = data.get('message', '未知错误')
            log(f"❌ 评论发布失败: {error_msg}")
            return False, error_msg
    except Exception as e:
        log(f"❌ 评论发布异常: {e}")
        return False, str(e)

def notify_failure(trend_index, trend_title, error_msg):
    """写入失败通知文件"""
    notify_file = f'outputs/logs/auto_comment_failures_{datetime.now().strftime("%Y%m%d")}.json'
    Path('outputs/logs').mkdir(parents=True, exist_ok=True)
    
    failures = []
    if Path(notify_file).exists():
        with open(notify_file, 'r') as f:
            failures = json.load(f)
    
    failures.append({
        'timestamp': datetime.now().isoformat(),
        'trend_index': trend_index,
        'trend_title': trend_title,
        'error': error_msg
    })
    
    with open(notify_file, 'w') as f:
        json.dump(failures, f, ensure_ascii=False, indent=2)

def main():
    if len(sys.argv) < 5:
        print("用法: python3 auto_first_comment.py <temp_post_id> <trend_index> <trend_title> <publish_time_iso>")
        print("示例: python3 auto_first_comment.py v_pub_url~xxx 1 '标题' '2026-04-24T12:17:00+08:00'")
        sys.exit(1)
    
    temp_post_id = sys.argv[1]
    trend_index = sys.argv[2]
    trend_title = sys.argv[3]
    publish_time_iso = sys.argv[4]
    
    log(f"=== 自动首评任务启动 (trend{trend_index}: {trend_title}) ===")
    log(f"临时 Post ID: {temp_post_id}")
    
    # 读取配置
    with open('config.json') as f:
        config = json.load(f)
    
    auto_comment = config.get('auto_first_comment', {})
    if not auto_comment.get('enabled', False):
        log("⚠️ 自动首评功能未启用，退出")
        return
    
    x2c_key = config['credentials']['x2c_api_key']
    max_wait = auto_comment.get('max_wait_minutes', 35)
    check_interval = auto_comment.get('check_interval_minutes', 2)
    
    # 智能获取真实 ID
    video_id = get_real_video_id_smart(publish_time_iso, x2c_key, max_wait, check_interval)
    if not video_id:
        error_msg = f"trend{trend_index} ({trend_title}) 无法获取真实视频 ID"
        log(error_msg)
        notify_failure(trend_index, trend_title, error_msg)
        return
    
    # 准备评论内容
    custom = auto_comment.get('custom_comment', '').strip()
    if custom:
        comment_text = custom
    else:
        templates = auto_comment.get('templates', [
            "欢迎大家讨论！你怎么看这个话题？👇",
            "这个观点你认同吗？评论区聊聊 💬",
            "有不同看法的朋友可以在评论区交流 🤔"
        ])
        use_random = auto_comment.get('use_random_template', True)
        if use_random:
            import random
            comment_text = random.choice(templates)
        else:
            idx = (int(trend_index) - 1) % len(templates)
            comment_text = templates[idx]
    
    log(f"📝 评论内容: {comment_text}")
    
    # 发布评论
    success, error = post_comment(video_id, comment_text, x2c_key)
    
    # 记录结果
    log_file = f'outputs/logs/auto_comment_{datetime.now().strftime("%Y%m%d")}.json'
    Path('outputs/logs').mkdir(parents=True, exist_ok=True)
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'trend_index': trend_index,
        'trend_title': trend_title,
        'temp_post_id': temp_post_id,
        'video_id': video_id,
        'publish_time': publish_time_iso,
        'comment': comment_text,
        'success': success,
        'error': error
    }
    
    # 追加到日志文件
    logs = []
    if Path(log_file).exists():
        with open(log_file, 'r') as f:
            logs = json.load(f)
    logs.append(log_entry)
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    
    if success:
        log(f"🎉 trend{trend_index} 首评任务完成")
    else:
        log(f"❌ trend{trend_index} 首评任务失败")
        notify_failure(trend_index, trend_title, error or "评论发布失败")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f"❌ 任务异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
