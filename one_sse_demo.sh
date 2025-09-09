#!/usr/bin/env bash
set -euo pipefail

FIFO=$(mktemp -u); mkfifo "$FIFO"
trap 'rm -f "$FIFO"' EXIT

# 0) open SSE and echo everything
curl --no-buffer -sN http://localhost:4000/sse -H 'Accept: text/event-stream' |
while IFS= read -r line; do
  payload=${line#data: }
  echo "$payload"
  [[ $payload == /messages/?session_id=* ]] && \
      printf '%s\n' "${payload#*=}" | tr -d '\r' >"$FIFO"
done &
LISTENER=$!
trap 'kill "$LISTENER" 2>/dev/null || true' EXIT

read -r SID <"$FIFO"
echo "SID=$SID" >&2

post() { curl -s -H 'Content-Type: application/json' --data-binary @"$1" \
        "http://localhost:4000/messages/?session_id=$SID"; echo; }

# 1) handshake -------------------------------------------------
post /tmp/init.json
sleep 0.3
post /tmp/initialized.json
sleep 0.3          # ← keep this short; replace with grep if you like

# 2) real work -------------------------------------------------
post /tmp/resources.json      # first useful call

wait "$LISTENER"              # Ctrl-C to quit
