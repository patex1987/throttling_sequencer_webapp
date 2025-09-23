#!/usr/bin/env bash
set -euo pipefail

PROFILE=console_app_access_admin
INSTANCE_ID=i-03f36d71c87fcd755
CLUSTER_ID=rds-aurora-failover-1
REGION=eu-central-1
#HOST=rds-aurora-failover-1.cluster-cvi8qy2gksxh.eu-central-1.rds.amazonaws.com
LOCAL_PORT=5432
REMOTE_PORT=5432

resolve_writer() {
  AWS_PROFILE=$PROFILE aws rds describe-db-clusters \
    --db-cluster-identifier "$CLUSTER_ID" \
    --region "$REGION" \
    --query "DBClusters[0].DBClusterMembers[?IsClusterWriter==\`true\`].DBInstanceIdentifier" \
    --output text
}

resolve_writer_endpoint() {
  WRITER=$(resolve_writer)
  AWS_PROFILE=$PROFILE aws rds describe-db-instances \
    --db-instance-identifier "$WRITER" \
    --region "$REGION" \
    --query "DBInstances[0].Endpoint.Address" \
    --output text
}

# Function: start SSM port forward in background
start_tunnel() {
  HOST=$(resolve_writer_endpoint)   # resolves to the cluster endpoint hostname
  echo "[INFO] Starting SSM tunnel to $HOST."
  AWS_PROFILE=$PROFILE aws ssm start-session \
    --target "$INSTANCE_ID" \
    --document-name AWS-StartPortForwardingSessionToRemoteHost \
    --parameters "host=$HOST,portNumber=$REMOTE_PORT,localPortNumber=$LOCAL_PORT" &
  TUNNEL_PID=$!
  echo "[INFO] Tunnel PID: $TUNNEL_PID"
}
# Function: stop tunnel
stop_tunnel() {
  echo "[INFO] Killing tunnel PID $TUNNEL_PID"
  kill "$TUNNEL_PID" || true
  kill "$TUNNEL_PID" 2>/dev/null || true
  # Wait until process fully exits
  wait "$TUNNEL_PID" 2>/dev/null || true
  # Extra guard: give the kernel a moment to free the port
  sleep 2
}

run_failover() {
  echo "[INFO] Triggering failover on cluster $CLUSTER_ID ..."
  AWS_PROFILE=$PROFILE aws rds failover-db-cluster \
    --db-cluster-identifier "$CLUSTER_ID" \
    --region "$REGION" > /dev/null
#  echo "[INFO] Failover triggered."
}


# Start tunnel, wait 30s, then failover
start_tunnel
echo "[INFO] Sleeping 30s before failover..."
sleep 30

run_failover

echo "[INFO] Sleeping 60s to let failover complete..."
sleep 60

# Restart tunnel
for i in {1..10}; do
  echo "[INFO] Restarting tunnel..."
  stop_tunnel
  start_tunnel
  echo "[INFO] Sleeping 40s before restarting tunnel..."
  sleep 40
done

echo "[INFO] New tunnel started. Now you can run psql or your app again."
wait
