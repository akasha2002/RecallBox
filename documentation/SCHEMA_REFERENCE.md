# RecallBox – Database Schema Reference & Data Dictionary

**Project:** RecallBox  
**Database:** PostgreSQL (Supabase)  
**ORM:** SQLAlchemy 2.0  
**Version:** V1.0  
**Last Updated:** 2026-11-24  

> **Note:** This document is the primary reference for table structures, data types, and constraints. Update this document whenever the schema is modified.

---

## Table Summary

| # | Table Name | Purpose | Model File |
|---|---|---|---|
| 1 | `workspaces` | Workspace root entity and access key hash | `backend/app/models/workspace.py` |
| 2 | `categories` | Workspace-scoped note categories | `backend/app/models/category.py` |
| 3 | `notes` | Primary note entries (title, content, timestamps) | `backend/app/models/note.py` |
| 4 | `tags` | Workspace-scoped reusable tags | `backend/app/models/tag.py` |
| 5 | `note_tags` | Many-to-many junction between notes and tags | `backend/app/models/note_tag.py` |

---

## 1. `workspaces` Table

Stores private workspaces. All user data is isolated by `workspace_id`.

| Column | Data Type | Nullable | Default | Constraints & Keys | Description |
|---|---|:---:|---|---|---|
| `id` | `UUID` | No | `uuid.uuid4` | **PRIMARY KEY**, Index | Unique workspace identifier |
| `name` | `VARCHAR(100)` | No | None | None | Display name of the workspace |
| `access_key_hash` | `VARCHAR(255)` | No | None | None | Hashed workspace access key |
| `created_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | None | Timestamp of workspace creation |
| `updated_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | None | Timestamp of last workspace update |

### Relationships:
- `categories`: One-to-Many (`Category`) &bull; `cascade="all, delete-orphan"`
- `notes`: One-to-Many (`Note`) &bull; `cascade="all, delete-orphan"`
- `tags`: One-to-Many (`Tag`) &bull; `cascade="all, delete-orphan"`

---

## 2. `categories` Table

Stores categories created within a workspace.

| Column | Data Type | Nullable | Default | Constraints & Keys | Description |
|---|---|:---:|---|---|---|
| `id` | `UUID` | No | `uuid.uuid4` | **PRIMARY KEY** | Unique category identifier |
| `workspace_id` | `UUID` | No | None | **FOREIGN KEY** (`workspaces.id`), Index | Owning workspace |
| `name` | `VARCHAR(100)` | No | None | None | Category name (e.g., "FastAPI", "React") |
| `created_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | None | Timestamp of category creation |

### Constraints & Indexes:
- **Foreign Key:** `FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE`
- **Unique Constraint:** `UNIQUE (workspace_id, name)` &bull; Duplicate category names within the same workspace are rejected.
- **Index:** `idx_categories_workspace_id` on `(workspace_id)`

### Relationships:
- `workspace`: Many-to-One (`Workspace`)
- `notes`: One-to-Many (`Note`)

---

## 3. `notes` Table

Stores notes created within a workspace.

| Column | Data Type | Nullable | Default | Constraints & Keys | Description |
|---|---|:---:|---|---|---|
| `id` | `UUID` | No | `uuid.uuid4` | **PRIMARY KEY** | Unique note identifier |
| `workspace_id` | `UUID` | No | None | **FOREIGN KEY** (`workspaces.id`), Index | Owning workspace |
| `category_id` | `UUID` | **Yes** | `NULL` | **FOREIGN KEY** (`categories.id`), Index | Assigned category (optional) |
| `title` | `VARCHAR(255)` | No | None | None | Title of the note |
| `content` | `TEXT` | No | None | None | Note body text |
| `created_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | None | Timestamp of note creation |
| `updated_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | Index | Timestamp of last modification |

### Constraints & Indexes:
- **Foreign Key 1:** `FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE`
- **Foreign Key 2:** `FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL`
- **Index 1:** `idx_notes_workspace_id` on `(workspace_id)`
- **Index 2:** `idx_notes_category_id` on `(category_id)`
- **Index 3:** `idx_notes_updated_at` on `(updated_at DESC)`
- **Index 4:** `idx_notes_workspace_title` on `(workspace_id, title)`

### Relationships:
- `workspace`: Many-to-One (`Workspace`)
- `category`: Many-to-One (`Category`)
- `tags`: Many-to-Many (`Tag`) via `note_tags`

---

## 4. `tags` Table

Stores reusable tags created within a workspace.

| Column | Data Type | Nullable | Default | Constraints & Keys | Description |
|---|---|:---:|---|---|---|
| `id` | `UUID` | No | `uuid.uuid4` | **PRIMARY KEY** | Unique tag identifier |
| `workspace_id` | `UUID` | No | None | **FOREIGN KEY** (`workspaces.id`), Index | Owning workspace |
| `name` | `VARCHAR(50)` | No | None | None | Tag name (e.g., "bug", "v1", "idea") |
| `created_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | None | Timestamp of tag creation |

### Constraints & Indexes:
- **Foreign Key:** `FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE`
- **Unique Constraint:** `UNIQUE (workspace_id, name)` &bull; Duplicate tag names within the same workspace are rejected.
- **Index:** `idx_tags_workspace_id` on `(workspace_id)`

### Relationships:
- `workspace`: Many-to-One (`Workspace`)
- `notes`: Many-to-Many (`Note`) via `note_tags`

---

## 5. `note_tags` Table (Junction / Association Table)

Associates notes with multiple tags (Many-to-Many relationship).

| Column | Data Type | Nullable | Default | Constraints & Keys | Description |
|---|---|:---:|---|---|---|
| `note_id` | `UUID` | No | None | **PRIMARY KEY (Composite)**, **FOREIGN KEY** (`notes.id`) | Reference to note |
| `tag_id` | `UUID` | No | None | **PRIMARY KEY (Composite)**, **FOREIGN KEY** (`tags.id`), Index | Reference to tag |

### Constraints & Indexes:
- **Composite Primary Key:** `PRIMARY KEY (note_id, tag_id)`
- **Foreign Key 1:** `FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE`
- **Foreign Key 2:** `FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE`
- **Index:** `idx_note_tags_tag_id` on `(tag_id)`

---

## Deletion Cascade Summary

| Entity Deleted | Affected Table | Cascade Action | Reason |
|---|---|---|---|
| **Workspace** | `categories`, `notes`, `tags`, `note_tags` | `CASCADE` | Purges all data belonging to the workspace. |
| **Category** | `notes.category_id` | `SET NULL` | Deleting a category does **not** delete notes; simply un-categorizes them. |
| **Note** | `note_tags` | `CASCADE` | Cleans up tag associations for that note. Tags themselves remain. |
| **Tag** | `note_tags` | `CASCADE` | Cleans up association with notes. Notes themselves remain. |
