#!/usr/bin/env python3
"""
LinkedIn 图文 Agent 安装验证脚本
"""

import subprocess
import sys
from pathlib import Path

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
NC = '\033[0m'

ok_count = 0
warn_count = 0
fail_count = 0


def ok(msg):
    global ok_count
    ok_count += 1
    print(f"{GREEN}✓{NC} {msg}")


def warn(msg):
    global warn_count
    warn_count += 1
    print(f"{YELLOW}⚠{NC} {msg}")


def fail(msg):
    global fail_count
    fail_count += 1
    print(f"{RED}✗{NC} {msg}")


def check_cmd(cmd):
    try:
        subprocess.run([cmd, '--version'], capture_output=True, check=True)
        return True
    except Exception:
        return False


def check_skill(name):
    local = Path('skills') / name
    global_path = Path.home() / '.openclaw' / 'skills' / name
    if local.exists():
        return 'local'
    if global_path.exists():
        return 'global'
    return None


print("=" * 60)
print("📌 LinkedIn 图文 Agent 安装验证")
print("=" * 60)

print("\n【1】系统依赖")
for cmd in ['node', 'python3', 'pip3']:
    if check_cmd(cmd):
        ok(cmd)
    else:
        fail(f"{cmd} 未安装")

print("\n【2】Skills 依赖")
skills = {
    'dailyhot-api': '热点采集（必需）',
    'giggle-generation-image': '图片生成（必需）',
    'x2c-socialposter': 'LinkedIn 发布（必需）',
    'claw-dashboard': '可视化面板（可选）',
}
for skill, desc in skills.items():
    loc = check_skill(skill)
    if loc:
        ok(f"{skill} — {desc} [{loc}]")
    elif '必需' in desc:
        fail(f"{skill} — {desc} 未安装 → openclaw skills install {skill}")
    else:
        warn(f"{skill} — {desc} 未安装")

print("\n【3】关键文件")
for file_path in [
    'AGENTS.md',
    'SOUL.md',
    'USER.md',
    'IDENTITY.md',
    'skills/linkedin-automator-core/SKILL.md',
    'skills/linkedin-automator-core/templates/config.template.json',
]:
    if Path(file_path).exists():
        ok(file_path)
    else:
        fail(f"{file_path} 缺失")

print("\n【4】输出目录")
for dir_path in [
    'outputs/briefs',
    'outputs/scripts',
    'outputs/images',
    'outputs/logs',
    'outputs/pool',
    'outputs/reports',
]:
    if Path(dir_path).exists():
        ok(dir_path)
    else:
        warn(f"{dir_path} 不存在（首次运行可自动创建）")

print("\n" + "=" * 60)
print(f"{GREEN}✓{NC} 通过: {ok_count}")
print(f"{YELLOW}⚠{NC} 警告: {warn_count}")
print(f"{RED}✗{NC} 失败: {fail_count}")

if fail_count > 0:
    sys.exit(1)
sys.exit(0)
