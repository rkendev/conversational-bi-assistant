#!/usr/bin/env bash
set -euo pipefail

# 1. get session id (trim CR/LF, silence stderr)
SID=$(
  (curl -sS --max-time 3 http://localhost:4000/sse 2>/dev/null || true) \
  | awk -F= '/session_id/{gsub(/\r/,"");print $2;exit}'
)
echo "SID=$SID"

# 2. write JSON-RPC requests
cat >/tmp/init.json <<'JSON'
{"jsonrpc":"2.0","id":0,"method":"initialize",
 "params":{"protocolVersion":"2024-11-05","capabilities":{},
           "clientInfo":{"name":"cli","version":"0.1"}}}
JSON

cat >/tmp/tlist.json <<'JSON'
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
JSON

cat >/tmp/schemas.json <<'JSON'
{"jsonrpc":"2.0","id":2,"method":"tools/call",
 "params":{"name":"list_schemas","arguments":{}}}
JSON

# 3. POST them in order
for f in /tmp/init.json /tmp/tlist.json /tmp/schemas.json; do
  printf '\n>>> POSTing %s\n' "$(basename "$f")"
  curl -sS -H 'Content-Type: application/json' \
       --data-binary @"$f" \
       "http://localhost:4000/messages/?session_id=${SID}"
  echo                          # just a newline
done
