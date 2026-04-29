#!/usr/bin/env python3
"""
自动首评配置向导
"""

import json
from pathlib import Path

def configure_auto_comment():
    print("\n" + "="*60)
    print("🤖 自动首评功能配置")
    print("="*60)
    
    print("\n视频发布到 YouTube 后，系统会自动发布第一条评论，帮助引导互动。")
    print("\n⚠️  注意：由于 YouTube 发布规则，视频发布后需要等待 30 分钟才能获取真实视频 ID。")
    print("系统会在后台自动等待并完成首评，不影响其他流程。")
    
    print("\n是否启用自动首评功能？")
    print("  A. 启用（推荐）")
    print("  B. 不启用")
    
    choice = input("\n你的选择 (A/B): ").strip().upper()
    
    if choice != 'A':
        print("\n✅ 已跳过自动首评配置")
        return {
            "enabled": False,
            "max_wait_minutes": 35,
            "check_interval_minutes": 2,
            "templates": [
                "欢迎大家讨论！你怎么看这个话题？👇",
                "这个观点你认同吗？评论区聊聊 💬",
                "有不同看法的朋友可以在评论区交流 🤔"
            ],
            "use_random_template": True,
            "custom_comment": ""
        }
    
    print("\n请选择首评方式：")
    print("\n方式 1：使用预设模板（系统自动选择）")
    print("  • 欢迎大家讨论！你怎么看这个话题？👇")
    print("  • 这个观点你认同吗？评论区聊聊 💬")
    print("  • 有不同看法的朋友可以在评论区交流 🤔")
    print("\n方式 2：自定义固定评论（每个视频都用这条）")
    print("  • 输入你的评论内容")
    
    mode = input("\n你的选择 (1/2): ").strip()
    
    config = {
        "enabled": True,
        "max_wait_minutes": 35,
        "check_interval_minutes": 2,
        "templates": [
            "欢迎大家讨论！你怎么看这个话题？👇",
            "这个观点你认同吗？评论区聊聊 💬",
            "有不同看法的朋友可以在评论区交流 🤔"
        ],
        "use_random_template": True,
        "custom_comment": ""
    }
    
    if mode == '2':
        custom = input("\n请输入你的自定义评论内容: ").strip()
        if custom:
            config['custom_comment'] = custom
            config['use_random_template'] = False
            print(f"\n✅ 已设置自定义评论: {custom}")
        else:
            print("\n⚠️  未输入内容，将使用预设模板")
    else:
        print("\n✅ 已选择使用预设模板（随机选择）")
    
    return config

if __name__ == '__main__':
    config_file = 'config.json'
    
    if not Path(config_file).exists():
        print("❌ config.json 不存在")
        exit(1)
    
    with open(config_file) as f:
        config = json.load(f)
    
    auto_comment_config = configure_auto_comment()
    config['auto_first_comment'] = auto_comment_config
    
    with open(config_file, 'w') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("✅ 配置已保存到 config.json")
    print("="*60)
