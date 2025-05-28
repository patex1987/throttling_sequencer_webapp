ENDPOINT="http://127.0.0.1:8080/graphql"
AUTH_TOKEN="YOUR_BEARER_TOKEN"    # leave empty if none
QUERY_FILE="testing_payloads/simple_path_call.gql"

# 1) Read & JSON-escape the query (requires jq; see notes below)
ESCAPED_QUERY=$(jq -Rs . < "$QUERY_FILE")

# 2) Build the JSON payload
PAYLOAD=$(printf '{"query": %s}' "$ESCAPED_QUERY")


# basic token call
curl -X POST "$ENDPOINT" \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic Z2Fib3I6eHl6" \
     -d "$PAYLOAD"

# bearer token call
curl -X POST "$ENDPOINT" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $AUTH_TOKEN" \
     -d "$PAYLOAD"