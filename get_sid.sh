#!/usr/bin/env bash
# Prints a fresh session_id (carriage-return stripped) or exits non-zero.
curl --max-time 10 -s http://localhost:4000/sse \
| awk -F= '/session_id=/{print $2; exit}' \
| tr -d '\r'
