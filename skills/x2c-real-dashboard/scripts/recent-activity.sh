#!/bin/bash
# dashboard/recent-activity — 最近动态
# Usage: bash recent-activity.sh [LIMIT]  LIMIT: 1–50, default 5
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_URL="https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api"
API_KEY="${X2C_API_KEY:-}"
LIMIT="${1:-5}"
[ -z "$API_KEY" ] && bash "$SCRIPT_DIR/setup-guide.sh"
if ! [[ "$LIMIT" =~ ^[0-9]+$ ]] || [ "$LIMIT" -lt 1 ] || [ "$LIMIT" -gt 50 ]; then
  echo '{"success":false,"error":"LIMIT must be between 1 and 50"}' >&2; exit 1
fi
curl -sS -X POST "$API_URL" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"dashboard/recent-activity\",\"limit\":$LIMIT}"
