#!/usr/bin/env bash
set -euo pipefail

ENDPOINT="http://127.0.0.1:8080/graphql"
AUTH_TOKEN="YOUR_BEARER_TOKEN"    # leave empty if none
QUERY_FILE="./simple_path_call.gql"

# 1) Read & JSON-escape the query (requires jq; see notes below)
ESCAPED_QUERY=$(jq -Rs . < "$QUERY_FILE")

# 2) Build the JSON payload
PAYLOAD=$(printf '{"query": %s}' "$ESCAPED_QUERY")

## Simple output
#for i in {1..120}; do
#  echo "[$(date '+%Y-%m-%d %H:%M:%S')]"
#  curl -s -X POST "$ENDPOINT" \
#       -H "Content-Type: application/json" \
#       -H "Authorization: Basic Z2Fib3I6eHl6" \
#       -d "$PAYLOAD"
#  echo    # newline for readability
#  sleep 2
#done

# fancy output
for i in {1..4800}; do
  ts=$(date '+%Y-%m-%d %H:%M:%S')
  tmp=$(mktemp)

  read http time_total <<<"$(
    curl -sS -o "$tmp" -w '%{http_code} %{time_total}' \
      -X POST "$ENDPOINT" \
      -H 'Content-Type: application/json' \
      -H 'Accept: application/json' \
      -H 'Authorization: Basic Z2Fib3I6eHl6' \
      -d "$PAYLOAD"
  )"

  if [ "$http" -ge 400 ]; then
    echo "[$ts] HTTP $http (${time_total}s) — ERROR"
    cat "$tmp"; echo
  elif jq -e '.errors and (.errors | length > 0)' "$tmp" >/dev/null 2>&1; then
    echo "[$ts] HTTP $http (${time_total}s) — GRAPHQL ERROR"
#    jq '.errors' "$tmp"; echo
  else
    echo "[$ts] HTTP $http (${time_total}s) — SUCCESS"
  fi

  rm -f "$tmp"
  sleep 2
done
