# RecallBox – API Documentation

**Project:** RecallBox  
**Version:** V1.0  
**Base URL (Local):** `http://localhost:8000`  
**API Prefix:** `/api/v1`  
**Interactive Swagger UI:** `http://localhost:8000/docs`  
**Interactive ReDoc:** `http://localhost:8000/redoc`  

---

## 1. Overview & Authentication Strategy

RecallBox uses REST APIs for all communication between the React frontend and FastAPI backend.

- **Content-Type:** `application/json`
- **Authentication:** Protected endpoints (from Phase 4 onward) require a Bearer token in the request header:
  ```http
  Authorization: Bearer <access_token>
  ```
- **Error Responses:** Standard JSON format with `detail` error message:
  ```json
  {
    "detail": "Description of the error"
  }
  ```

---

## 2. Implemented Endpoints (Phase 1)

### 2.1 API Root Discovery

Returns basic application identity and links to Swagger UI and health check.

- **Endpoint:** `GET /`
- **Authentication:** None (Public)
- **Response `200 OK`:**
  ```json
  {
    "message": "Welcome to RecallBox API",
    "version": "1.0.0",
    "environment": "development",
    "docs": "/docs",
    "health": "/api/v1/health"
  }
  ```

---

### 2.2 Health Check

Used by frontend, monitoring tools, and Docker health-checks to verify API uptime and environment.

- **Endpoint:** `GET /api/v1/health`
- **Alias:** `GET /health`
- **Authentication:** None (Public)
- **Response `200 OK`:**
  ```json
  {
    "status": "ok",
    "app": "RecallBox API",
    "version": "1.0.0",
    "environment": "development",
    "timestamp": "2026-11-23T11:48:47.075435Z"
  }
  ```

---

## 3. Planned Endpoints Roadmap (Upcoming Phases)

### Phase 4: Workspace Management
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/workspaces` | Create workspace (returns workspace ID & raw access key) |
| `POST` | `/api/v1/workspaces/access` | Validate credentials & issue access token |

### Phase 6: Note Management
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/notes` | List notes for current workspace (with pagination) |
| `POST` | `/api/v1/notes` | Create a new note |
| `GET` | `/api/v1/notes/{id}` | Get note details |
| `PUT` | `/api/v1/notes/{id}` | Update existing note |
| `DELETE` | `/api/v1/notes/{id}` | Delete a note |

### Phase 7: Categories & Tags
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/categories` | List categories in workspace |
| `POST` | `/api/v1/categories` | Create a category |
| `DELETE` | `/api/v1/categories/{id}` | Delete category |
| `GET` | `/api/v1/tags` | List tags in workspace |
| `POST` | `/api/v1/tags` | Create a tag |

### Phase 8: Search & Filtering
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/notes/search?q={query}` | Search notes by title/content & filter by category/tag |
