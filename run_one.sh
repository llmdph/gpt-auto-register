#!/bin/bash
# Trigger one CF-temp registration via WebUI API, using WARP proxy.
set -u
BASE="${1:-http://127.0.0.1:8765}"
PROXY="${PROXY:-http://127.0.0.1:40080}"
COUNT="${COUNT:-1}"

for i in $(seq 1 "$COUNT"); do
  echo "[$(date '+%F %T')] start register #$i proxy=$PROXY"
  resp=$(curl -sS -m 30 -X POST "$BASE/api/register" \
    -H 'Content-Type: application/json' \
    -d "{\"email\":null,\"proxy\":\"$PROXY\",\"want_access_token\":true,\"want_session_token\":true,\"want_refresh_token\":true,\"otp_timeout\":180}")
  echo "$resp"
  run_id=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("run_id",""))' <<<"$resp" 2>/dev/null || true)
  if [ -z "$run_id" ]; then
    echo "failed to start"
    exit 1
  fi
  echo "run_id=$run_id ; tail SSE / logs for progress"
done
