# FLIP PROCESS:
#- drain db1, wait 10 seconds, make db2 ready
#- drain db2, wait 10 seconds, make db1 ready
#- force both dbs down
#- drain db1, wait 10 seconds, make db2 ready


# run against the running fastapi service
# fancy output
# USE `testing_payloads/graphql_api_poller.sh` from another session


# flip the db in the ui of haproxy (or through the commands)


# Drain DB1; make DB2 ready
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Drain DB1"
printf "set server pg_pool/pg-backend-1 state drain\n" | nc 127.0.0.1 9999
docker exec -it -e PGPASSWORD=postgres pgbouncer \
  psql -h 127.0.0.1 -p 6432 -U postgres pgbouncer \
  -c  "SHOW SERVERS;" \
  -c "RECONNECT postgres" > /dev/null
sleep 10
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Make DB2 ready"
printf "set server pg_pool/pg-backend-2 state ready\n" | nc 127.0.0.1 9999




# Drain DB2; make DB1 ready
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Drain DB2"
printf "set server pg_pool/pg-backend-2 state drain\n" | nc 127.0.0.1 9999
docker exec -it -e PGPASSWORD=postgres pgbouncer \
  psql -h 127.0.0.1 -p 6432 -U postgres pgbouncer \
  -c  "SHOW SERVERS;" \
  -c "RECONNECT postgres" > /dev/null
sleep 10
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Make DB1 ready"
printf "set server pg_pool/pg-backend-1 state ready\n" | nc 127.0.0.1 9999
sleep 10


# Force both down
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] force both dbs down"
printf "set server pg_pool/pg-backend-1 state maint\n" | nc 127.0.0.1 9999
printf "set server pg_pool/pg-backend-2 state maint\n" | nc 127.0.0.1 9999
docker exec -it -e PGPASSWORD=postgres pgbouncer \
  psql -h 127.0.0.1 -p 6432 -U postgres pgbouncer \
  -c  "SHOW SERVERS;" \
  -c "RECONNECT postgres" > /dev/null


# Drain DB1; make DB2 ready
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Drain DB1"
printf "set server pg_pool/pg-backend-1 state drain\n" | nc 127.0.0.1 9999
docker exec -it -e PGPASSWORD=postgres pgbouncer \
  psql -h 127.0.0.1 -p 6432 -U postgres pgbouncer \
  -c  "SHOW SERVERS;" \
  -c "RECONNECT postgres" > /dev/null
sleep 10
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Make DB2"
printf "set server pg_pool/pg-backend-2 state ready\n" | nc 127.0.0.1 9999