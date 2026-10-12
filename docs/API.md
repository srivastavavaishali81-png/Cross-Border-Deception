# OZARK — API Reference

Base URL: `http://localhost:8000`

## Authentication

> To be implemented. Planned: JWT Bearer tokens via `python-jose`.

---

## Health

### `GET /health`

Liveness probe.

**Response `200`:**
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

## API v1 — `GET /api/v1/ping`

Simple ping endpoint.

**Response `200`:**
```json
{
  "ping": "pong"
}
```

---

## Planned Endpoints

> These will be implemented as business logic is added.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/auth/login` | Obtain access token |
| `POST` | `/api/v1/auth/refresh` | Refresh access token |
| `GET` | `/api/v1/users` | List users |
| `GET` | `/api/v1/users/{id}` | Get user by ID |
| `POST` | `/api/v1/users` | Create user |
| `GET` | `/api/v1/graph/nodes` | List graph nodes |
| `GET` | `/api/v1/graph/paths` | Find paths between nodes |

---

## Error Format

All errors follow FastAPI's default format:

```json
{
  "detail": "Human-readable error message"
}
```

| Status | Meaning |
|--------|---------|
| `400` | Bad request / validation error |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Not found |
| `422` | Unprocessable entity (Pydantic validation) |
| `500` | Internal server error |
