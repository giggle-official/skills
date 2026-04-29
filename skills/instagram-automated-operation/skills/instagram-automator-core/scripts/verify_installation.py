#!/usr/bin/env python3
"""
Instagram Agent 完整安装验证脚本
检查所有依赖、配置、脚本、定时任务是否完整
"""

import json
import subprocess
import sys
import os
from pathlib import Path

RED   = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW= '\033[1;33m'
NC    = '\033[0m'

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
    except:
        return False

def check_skill(name):
    local = Path('skills') / name
    global_path = Path.home() / '.openclaw' / 'skills' / name
    if local.exists():
        return 'local'
    elif global_path.exists():
        return 'global'
    return None

print("=" * 60)
print("🎬 Instagram Agent 完整安装验证")
print("=" * 60)

# ── 1. 系统依赖 ──────────────────────────────────────────────
print("\n【1】系统依赖")
for cmd in ['node', 'python3', 'pip3']:
    if check_cmd(cmd):
        ok(cmd)
    else:
        fail(f"{cmd} 未安装")

# openclaw
try:
    r = subprocess.run(['openclaw', '--version'], capture_output=True, text=True)
    ok(f"openclaw {r.stdout.strip()}")
except:
    fail("openclaw 未安装")

# ── 2. Skills ────────────────────────────────────────────────
print("\n【2】Skills 依赖")
skills = {
    'dailyhot-api':           '热点采集（必需）',
    'giggle-generation-drama':'视频生成（必需）',
    'x2c-socialposter':       'Instagram 发布（必需）',
    'claw-dashboard':         '可视化面板（可选）',
}
for skill, desc in skills.items():
    loc = check_skill(skill)
    if loc == 'local':
        ok(f"{skill} — {desc} [本地]")
    elif loc == 'global':
        ok(f"{skill} — {desc} [全局]")
    else:
        if '必需' in desc:
            fail(f"{skill} — {desc} 未安装 → 运行: openclaw skills install {skill}")
        else:
            warn(f"{skill} — {desc} 未安装（可选，启用 Dashboard 时需要）")

# claw-dashboard pip 包检查
claw_dash_path = Path.home() / '.openclaw' / 'skills' / 'claw-dashboard'
if claw_dash_path.exists():
    try:
        r = subprocess.run(
            ['python3', '-c', 'import sys; sys.path.insert(0, str(__import__("pathlib").Path.home()/".openclaw"/"skills"/"claw-dashboard")); from src.hub import manager'],
            capture_output=True, text=True
        )
        if r.returncode == 0:
            ok("claw-dashboard Python 包已安装")
        else:
            warn("claw-dashboard Python 包未安装 → cd ~/.openclaw/skills/claw-dashboard && pip install -e .")
    except:
        warn("claw-dashboard Python 包检查失败")

# ── 3. 核心文件 ──────────────────────────────────────────────
print("\n【3】核心文件")
core_files = {
    'AGENTS.md':  '操作规范（必需）',
    'SOUL.md':    '人格设定（必需）',
    'USER.md':    '用户指南（必需）',
    'IDENTITY.md':'身份标识（必需）',
}
for f, desc in core_files.items():
    if Path(f).exists():
        ok(f"{f} — {desc}")
    else:
        fail(f"{f} — {desc} 缺失")

# 检查 skill 文档
skill_docs = {
    'skills/instagram-automator-core/SKILL.md': 'Skill 说明（必需）',
    'skills/instagram-automator-core/docs/README.md': '项目说明',
    'skills/instagram-automator-core/docs/config.template.json': '配置模板',
}
for f, desc in skill_docs.items():
    if Path(f).exists():
        ok(f"{Path(f).name} — {desc}")
    else:
        warn(f"{Path(f).name} — {desc} 缺失")

# config.json
if Path('config.json').exists():
    ok("config.json 已配置")
else:
    warn("config.json 不存在（首次启动时由配置向导创建）")

# ── 4. Scripts 目录 ──────────────────────────────────────────
print("\n【4】核心脚本")
scripts = {
    'skills/instagram-automator-core/scripts/lightweight_collect.py': '轻量采集',
    'skills/instagram-automator-core/scripts/auto_first_comment.py': '自动首评',
    'skills/instagram-automator-core/scripts/dashboard_integration.py': 'Dashboard 集成',
    'skills/instagram-automator-core/scripts/setup_dashboard.py': 'Dashboard 设置',
    'skills/instagram-automator-core/scripts/verify_installation.py': '安装验证',
}
for script, desc in scripts.items():
    if Path(script).exists():
        ok(f"{Path(script).name} — {desc}")
    else:
        fail(f"{Path(script).name} — {desc} 缺失")

# ── 5. 输出目录 ──────────────────────────────────────────────
print("\n【5】输出目录")
output_dirs = ['outputs/briefs', 'outputs/scripts', 'outputs/videos', 
               'outputs/logs', 'outputs/pool', 'outputs/reports']
for d in output_dirs:
    if Path(d).exists():
        ok(d)
    else:
        warn(f"{d} 不存在（首次运行时自动创建）")

# ── 6. 定时任务 ──────────────────────────────────────────────
print("\n【6】定时任务")
if not Path('config.json').exists():
    warn("config.json 不存在，跳过定时任务检查")
else:
    try:
        r = subprocess.run(['openclaw', 'cron', 'list'], capture_output=True, text=True)
        if 'instagram' in r.stdout.lower() or '热点' in r.stdout or '生产' in r.stdout:
            ok("定时任务已注册")
        else:
            warn("定时任务未注册（首次配置时自动注册）")
    except:
        warn("无法检查定时任务")

# ── 总结 ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("验证结果")
print("=" * 60)
print(f"{GREEN}✓{NC} 通过: {ok_count}")
print(f"{YELLOW}⚠{NC} 警告: {warn_count}")
print(f"{RED}✗{NC} 失败: {fail_count}")

if fail_count > 0:
    print(f"\n{RED}❌ 存在 {fail_count} 个错误，请先修复{NC}")
    sys.exit(1)
elif warn_count > 0:
    print(f"\n{YELLOW}⚠️  存在 {warn_count} 个警告，但可以继续{NC}")
    sys.exit(0)
else:
    print(f"\n{GREEN}🎉 所有检查通过！{NC}")
    sys.exit(0)
