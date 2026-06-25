#!/usr/bin/env python3
"""
Dashboard Setup Script - 使用 claw-dashboard skill
"""

import sys
import json
from pathlib import Path

# 添加 skill 路径
skill_path = Path.home() / ".openclaw" / "skills" / "claw-dashboard"
sys.path.insert(0, str(skill_path))

from src.hub import installer, manager

def setup():
    """执行完整的 dashboard 设置"""
    print("📊 开始设置 Dashboard...")
    
    # 1. 安装 hub
    print("\n1️⃣ 安装 hub...")
    result = installer.install_hub()
    print(f"   {result}")
    
    # 2. 安装 cloudflared
    print("\n2️⃣ 安装 cloudflared...")
    if not installer.is_cloudflared_installed():
        result = installer.install_cloudflared()
        print(f"   {result}")
    else:
        print("   cloudflared 已安装")
    
    # 3. 注册设备
    print("\n3️⃣ 注册设备...")
    if not installer.is_tunnel_configured():
        try:
            serial = installer.get_device_serial()
            print(f"   设备序列号: {serial}")
            data = installer.register_device(serial)
            print(f"   ✅ 注册成功")
            print(f"   公网地址: {data.get('public_url')}")
        except Exception as e:
            print(f"   ⚠️ 自动获取序列号失败: {e}")
            print("   请手动提供设备序列号（12位字符）")
            return
    else:
        config = installer.get_tunnel_config()
        print(f"   已注册，公网地址: {config.get('public_url')}")
    
    # 4. 启动 hub
    print("\n4️⃣ 启动 hub...")
    hub_result = manager.start_hub()
    print(f"   {hub_result}")
    
    # 5. 启动 tunnel
    print("\n5️⃣ 启动 tunnel...")
    tunnel_result = manager.start_tunnel()
    print(f"   {tunnel_result}")
    
    # 6. 获取最终状态
    print("\n6️⃣ 最终状态:")
    status = manager.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # 7. 保存到 config.json
    config_file = Path("config.json")
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
        
        config['dashboard'] = {
            'enabled': True,
            'type': 'claw-dashboard',
            'public_url': status.get('public_url'),
            'local_url': 'http://localhost:3000'
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print("\n✅ Dashboard 设置完成！")
        print(f"📊 公网访问: {status.get('public_url')}")
        print(f"🏠 本地访问: http://localhost:3000")

def status():
    """检查 dashboard 状态"""
    status = manager.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 scripts/dashboard_setup.py [setup|status]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == 'setup':
        setup()
    elif cmd == 'status':
        status()
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
