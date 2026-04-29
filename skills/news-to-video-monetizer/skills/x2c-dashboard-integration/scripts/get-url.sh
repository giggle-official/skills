#!/bin/bash
# get-url.sh - 获取 Dashboard URL
set -e

if [ ! -f ~/.claw/config/tunnel.json ]; then
  echo "❌ Dashboard 未初始化" >&2
  exit 1
fi

python3 -c "import json,os; print(json.load(open(os.path.expanduser('~/.claw/config/tunnel.json')))['public_url'])"
