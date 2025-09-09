#!/usr/bin/env bash
set -euo pipefail

# use existing $1 or grab a fresh one
SID=${1:-$(./get_sid.sh)}
echo "poster SID=$SID"

post() {
  curl -sS -H 'Content-Type: application/json' \
       --data-binary @"$1" \
       "http://localhost:4000/messages/?session_id=${SID}"
}

post /tmp/init.json
post /tmp/tlist.json
post /tmp/schemas.json
