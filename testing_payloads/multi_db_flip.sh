
# run against the running fastapi service

# Simple output
for i in {1..120}; do
  echo "[$(date '+%Y-%m-%d %H:%M:%S')]"
  curl -s -X POST "$ENDPOINT" \
       -H "Content-Type: application/json" \
       -H "Authorization: Basic Z2Fib3I6eHl6" \
       -d "$PAYLOAD"
  echo    # newline for readability
  sleep 2
done

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
  sleep 0.2
done


# flip the db in the ui of haproxy (or through the commands)


# Drain DB1; make DB2 ready
printf "set server pg_pool/pg-backend-1 state drain\n" | nc 127.0.0.1 9999
docker exec -it -e PGPASSWORD=postgres pgbouncer \
  psql -h 127.0.0.1 -p 6432 -U postgres pgbouncer \
  -c  "SHOW SERVERS;" \
  -c "RECONNECT postgres"
sleep 5
printf "set server pg_pool/pg-backend-2 state ready\n" | nc 127.0.0.1 9999




# Drain DB2; make DB1 ready
printf "set server pg_pool/pg-backend-2 state drain\n" | nc 127.0.0.1 9999
docker exec -it -e PGPASSWORD=postgres pgbouncer \
  psql -h 127.0.0.1 -p 6432 -U postgres pgbouncer \
  -c  "SHOW SERVERS;" \
  -c "RECONNECT postgres"
sleep 5
printf "set server pg_pool/pg-backend-1 state ready\n" | nc 127.0.0.1 9999


# Force both down
printf "set server pg_pool/pg-backend-1 state maint\n" | nc 127.0.0.1 9999
printf "set server pg_pool/pg-backend-2 state maint\n" | nc 127.0.0.1 9999
docker exec -it -e PGPASSWORD=postgres pgbouncer \
  psql -h 127.0.0.1 -p 6432 -U postgres pgbouncer \
  -c  "SHOW SERVERS;" \
  -c "RECONNECT postgres"
