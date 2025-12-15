# Keycloak Token Retrieval Guide

This guide explains how to retrieve authentication tokens from Keycloak for testing the throttling sequencer service.

## Prerequisites

- Keycloak instance running (default: `http://localhost:8082`)
- Realm: `throttling-test`
- Client ID: `throttling-api`
- Client Secret: `test-client-secret`

## Test Users

The following test users are available in the `throttling-test` realm:

| Username | Password | Roles |
|----------|----------|-------|
| `test-user` | `test-password` | `user` |
| `admin-user` | `admin-password` | `admin` |

## Token Endpoint

```
POST http://localhost:8082/realms/throttling-test/protocol/openid-connect/token
```

## Using cURL

### Request a token with password grant

```bash
curl -X POST \
  http://localhost:8082/realms/throttling-test/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=throttling-api" \
  -d "client_secret=test-client-secret" \
  -d "username=test-user" \
  -d "password=test-password"
```

### Response

The response will contain:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ...",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ...",
  "token_type": "Bearer",
  "not-before-policy": 0,
  "session_state": "...",
  "scope": "profile email roles"
}
```

### Using the token

Extract the `access_token` from the response and use it in API calls:

```bash
# For REST API
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d @testing_payloads/game_state.json \
  http://localhost:8080/api/v1/throttle/calculate_throttle_steps

# For GraphQL API
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"query": "{ ... }"}' \
  http://localhost:8080/graphql
```

## Using Python Scripts

See `get_keycloak_token.py` for programmatic token retrieval using environment variables.

### Environment Variables

The Python script supports the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `KEYCLOAK_URL` | `http://localhost:8082` | Keycloak base URL |
| `KEYCLOAK_REALM` | `throttling-test` | Realm name |
| `KEYCLOAK_CLIENT_ID` | `throttling-api` | Client ID |
| `KEYCLOAK_CLIENT_SECRET` | `test-client-secret` | Client secret |
| `KEYCLOAK_USERNAME` | `test-user` | Username for password grant |
| `KEYCLOAK_PASSWORD` | `test-password` | Password for password grant |

### Example Usage

```bash
# Using defaults
python testing_payloads/get_keycloak_token.py

# With custom credentials
KEYCLOAK_USERNAME=admin-user KEYCLOAK_PASSWORD=admin-password \
  python testing_payloads/get_keycloak_token.py

# With custom Keycloak URL
KEYCLOAK_URL=http://keycloak.example.com:8080 \
  python testing_payloads/get_keycloak_token.py
```

## Token Refresh

Tokens expire after a certain period (default: 300 seconds). Use the `refresh_token` to obtain a new access token:

```bash
curl -X POST \
  http://localhost:8082/realms/throttling-test/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=throttling-api" \
  -d "client_secret=test-client-secret" \
  -d "refresh_token=<refresh_token>"
```

## Troubleshooting

### Keycloak not accessible

Ensure Keycloak is running:

```bash
# Check if Keycloak container is running
docker ps | grep keycloak

# Check Keycloak health
curl http://localhost:8082/health
```

### Invalid credentials

Verify the username and password match the test users defined in `keycloak_config/realm-test.json`.

### Token validation errors

Ensure the token is used before expiration. Check the `expires_in` field in the token response.

