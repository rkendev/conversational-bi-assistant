#!/usr/bin/env bash
set -euo pipefail

SID=$(./get_sid.sh)
echo "SID=$SID"

###############################################################################
# 1) INITIALISE THE SESSION (blocking HTTP call, no stream yet)
###############################################################################
curl -s -H 'Content-Type: application/json' \
     --data-binary @/tmp/init.json \
     "http://localhost:4000/messages/?session_id=${SID}"
echo        # pretty newline

###############################################################################
# 2) NOW open the event stream ─ the session is valid so it will stay open
###############################################################################
curl -sN "http://localhost:4000/messages/?session_id=${SID}" \
     -H 'Accept: text/event-stream' |
     sed -u -n 's/^data: //p' &
listener_pid=$!

###############################################################################
# 3) helper to POST follow-up requests
###############################################################################
post () {
  curl -s -H 'Content-Type: application/json' \
       --data-binary @"$1" \
       "http://localhost:4000/messages/?session_id=${SID}"
  echo
}

post /tmp/tlist.json
post /tmp/schemas.json

###############################################################################
# 4) keep script alive so you can watch the replies scroll by
###############################################################################
wait "$listener_pid"   # Ctrl-C to quit
