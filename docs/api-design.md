<!-- 
FILE_TYPE: Project Documentation (API Spec)
CATEGORY: Technical Design
ENTRIES: 5 Endpoints (v1)
DATE_RANGE: 2026-05-07
KEYWORDS: REST, Webhook, Versioning, Rate Limiting, Error IDs, JSON
SUMMARY: Detailed API specification for the Remote PC Controller. Includes versioned endpoints, error standards, and session management.
-->
# API Design - Remote PC Controller

**Base URL:** `http://{PC_IP}:8000/api/v1`
**Auth Header:** `X-API-Key: {your_api_key}`

---

## 1. Webhook Endpoint

### `POST /api/v1/webhook`
Executes an intent-based command.

**Request Body:**
```json
{
  "intent": "open slack",
  "source": "voice" | "type" | "click"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Command executed successfully",
  "data": {
    "action": "launched_app",
    "target": "C:\\Path\\To\\Slack.exe",
    "execution_time_ms": 120
  }
}
```

---

## 2. Session Management

### `GET /api/v1/status`
Fetches current active session.

### `POST /api/v1/sessions/start`
Starts a work session.

### `POST /api/v1/sessions/stop`
Stops the active session and returns duration.

---

## 3. Reports & Analytics

### `GET /api/v1/reports/summary`
Weekly work totals, daily breakdown, and top app usage.

### `GET /api/v1/reports/history?limit=20`
Paginated command audit logs.

---

## 4. Mappings Management (Admin)

### `GET /api/v1/mappings`
List all configured mappings.

### `POST /api/v1/mappings`
Add a new intent mapping.

### `DELETE /api/v1/mappings/{id}`
Remove a mapping.

---

## 5. Error Standards (Rule 48)
| HTTP | Error ID | Message |
|------|----------|---------|
| 401 | `ERR-401-001` | Invalid or missing API Key |
| 404 | `ERR-404-001` | Intent not found in mappings |
| 429 | `ERR-429-001` | Rate limit exceeded (10 req/sec) |
| 500 | `ERR-500-001` | Internal server error |
