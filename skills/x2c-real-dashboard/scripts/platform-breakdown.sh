#!/bin/bash
# dashboard/platform-breakdown — 各平台播放量
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_URL="https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api"
API_KEY="${X2C_API_KEY:-}"
[ -z "$API_KEY" ] && bash "$SCRIPT_DIR/setup-guide.sh"
curl -sS -X POST "$API_URL" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"action":"dashboard/platform-breakdown"}'
