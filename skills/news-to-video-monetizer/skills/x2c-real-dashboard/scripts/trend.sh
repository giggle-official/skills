#!/bin/bash
# dashboard/trend — 收益趋势
# Auto-loads X2C_API_KEY from workspace config.json
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_URL="https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api"
DAYS="${1:-7}"

# Validate days
if ! [[ "$DAYS" =~ ^[0-9]+$ ]] || [ "$DAYS" -lt 1 ] || [ "$DAYS" -gt 90 ]; then
  echo '{"success":false,"error":"DAYS must be 1-90"}' >&2
  exit 1
fi

# Auto-load API key from workspace config if not set
if [ -z "${X2C_API_KEY:-}" ]; then
  CONFIG_PATH="$HOME/.openclaw/workspace-news-to-video-monetizer/config.json"
  if [ -f "$CONFIG_PATH" ]; then
    X2C_API_KEY=$(python3 -c "import json,sys; print(json.load(open('$CONFIG_PATH')).get('x2c',{}).get('api_key',''))" 2>/dev/null || echo "")
  fi
fi

API_KEY="${X2C_API_KEY:-}"

if [ -z "$API_KEY" ]; then
  echo '{"success":false,"error":"X2C_API_KEY not configured in workspace config.json"}' >&2
  exit 1
fi

curl -sS -X POST "$API_URL" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"dashboard/trend\",\"days\":$DAYS}"
