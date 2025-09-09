#!/usr/bin/env bash
set -euo pipefail

SID=$(./get_sid.sh) || { echo "failed to grab session_id" >&2; exit 1; }
echo "SID=$SID"

###############################################################################
# 1) open the SSE stream FIRST  (non-blocking, runs in the background)
###############################################################################
curl --no-buffer -sN "http://localhost:4000/sse?session_id=${SID}" \
     -H 'Accept: text/event-stream' \
  | sed -u -n 's/^data: //p' &
listener_pid=$!

###############################################################################
# 2) *optional* initialisation call — not strictly needed for many servers
###############################################################################
curl -s -H 'Content-Type: application/json' \
     --data '{"jsonrpc":"2.0","id":0,"method":"initialize",
              "params":{"protocolVersion":1,"capabilities":{},
                        "clientInfo":{"name":"cli","version":"0.1"}}}' \
     "http://localhost:4000/messages/?session_id=${SID}"

###############################################################################
# 3) fire a couple of demo requests
###############################################################################
for f in  /tmp/tlist.json  /tmp/schemas.json; do
  echo "POST $(basename "$f")"
  curl -s -H 'Content-Type: application/json' \
       --data-binary @"$f" \
       "http://localhost:4000/messages/?session_id=${SID}"
done

###############################################################################
# 4) keep the script alive so you can watch the responses scroll by
###############################################################################
wait "$listener_pid"        # Ctrl-C to quit
