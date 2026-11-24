# RecallBox – Database Design & Architecture

**Project:** RecallBox  
**Document:** Database Design Specification  
**Version:** V1.0  
**Database:** PostgreSQL (Hosted on Supabase)  
**ORM:** SQLAlchemy 2.0  
**Migration Tool:** Alembic  
**Status:** Approved for Implementation  

---

## 1. Overview & Data Isolation Strategy

RecallBox is a workspace-based personal note-taking system. The database architecture is designed with **strict workspace-level data isolation**:

- Every operational record (`notes`, `categories`, `tags`) belongs directly to a `workspace_id`.
- Foreign key constraints with `ON DELETE CASCADE` ensure that deleting a workspace removes all its associated data without leaving orphaned records.
- Composite uniqueness constraints prevent duplicate category and tag names within the same workspace.

---

## 2. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    WORKSPACES ||--o{ CATEGORIES : "has"
    WORKSPACES ||--o{ NOTES : "owns"
    WORKSPACES ||--o{ TAGS : "has"
    CATEGORIES ||--o{ NOTES : "classifies"
    NOTES ||--o{ NOTE_TAGS : "contains"
    TAGS ||--o{ NOTE_TAGS : "applied to"

    WORKSPACES {
        uuid id PK
        varchar(100) name
        varchar(255) access_key_hash
        timestamptz created_at
        timestamptz updated_at
    }

    CATEGORIES {
        uuid id PK
        uuid workspace_id FK
        varchar(100) name
        timestamptz created_at
    }

    NOTES {
        uuid id PK
        uuid workspace_id FK
        uuid category_id FK "nullable"
        varchar(255) title
        text content
        timestamptz created_at
        timestamptz updated_at
    }

    TAGS {
        uuid id PK
        uuid workspace_id FK
        varchar(50) name
        timestamptz created_at
    }

    NOTE_TAGS {
        uuid note_id PK,FK
        uuid tag_id PK,FK
    }
```

---

## 3. Table Specifications

### 3.1 `workspaces` Table
Stores private workspaces and hashed access keys.

| Column Name | Data Type | Nullable | Default | Description |
|---|---|---|---|---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key (Unique workspace identifier) |
| `name` | `VARCHAR(100)` | No | None | Display name of the workspace |
| `access_key_hash` | `VARCHAR(255)` | No | None | Securely hashed access key (Argon2 / bcrypt) |
| `created_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | Workspace creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | Last updated timestamp |

- **Primary Key:** `PRIMARY KEY (id)`
- **Security Rule:** Plaintext access keys are never stored. Only `access_key_hash` is persisted.

---

### 3.2 `categories` Table
Stores workspace-specific topic categories for notes (e.g. "FastAPI", "React", "Personal").

| Column Name | Data Type | Nullable | Default | Description |
|---|---|---|---|---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key |
| `workspace_id` | `UUID` | No | None | Foreign Key referencing `workspaces.id` |
| `name` | `VARCHAR(100)` | No | None | Category name |
| `created_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | Creation timestamp |

- **Primary Key:** `PRIMARY KEY (id)`
- **Foreign Key:** `FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE`
- **Constraints:** `UNIQUE (workspace_id, name)` – Category names must be unique within a workspace.
- **Index:** `CREATE INDEX idx_categories_workspace_id ON categories (workspace_id);`

---

### 3.3 `notes` Table
Stores note entries belonging to an authorized workspace.

| Column Name | Data Type | Nullable | Default | Description |
|---|---|---|---|---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key |
| `workspace_id` | `UUID` | No | None | Foreign Key referencing `workspaces.id` |
| `category_id` | `UUID` | Yes | `NULL` | Foreign Key referencing `categories.id` |
| `title` | `VARCHAR(255)` | No | None | Note title |
| `content` | `TEXT` | No | None | Main note markdown or plain text content |
| `created_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | Creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | Last modified timestamp |

- **Primary Key:** `PRIMARY KEY (id)`
- **Foreign Keys:**
  - `FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE`
  - `FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL`
- **Indexes:**
  - `CREATE INDEX idx_notes_workspace_id ON notes (workspace_id);`
  - `CREATE INDEX idx_notes_category_id ON notes (category_id);`
  - `CREATE INDEX idx_notes_updated_at ON notes (updated_at DESC);`
  - `CREATE INDEX idx_notes_title ON notes (workspace_id, title);`

---

### 3.4 `tags` Table
Stores reusable labels within a workspace.

| Column Name | Data Type | Nullable | Default | Description |
|---|---|---|---|---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key |
| `workspace_id` | `UUID` | No | None | Foreign Key referencing `workspaces.id` |
| `name` | `VARCHAR(50)` | No | None | Tag label (e.g. "bugs", "ideas", "v1") |
| `created_at` | `TIMESTAMPTZ` | No | `CURRENT_TIMESTAMP` | Creation timestamp |

- **Primary Key:** `PRIMARY KEY (id)`
- **Foreign Key:** `FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE`
- **Constraints:** `UNIQUE (workspace_id, name)` – Tag names must be unique within a workspace.
- **Index:** `CREATE INDEX idx_tags_workspace_id ON tags (workspace_id);`

---

### 3.5 `note_tags` Table (Association Table)
Manages the many-to-many relationship between `notes` and `tags`.

| Column Name | Data Type | Nullable | Default | Description |
|---|---|---|---|---|
| `note_id` | `UUID` | No | None | Foreign Key referencing `notes.id` |
| `tag_id` | `UUID` | No | None | Foreign Key referencing `tags.id` |

- **Primary Key:** `PRIMARY KEY (note_id, tag_id)`
- **Foreign Keys:**
  - `FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE`
  - `FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE`
- **Index:** `CREATE INDEX idx_note_tags_tag_id ON note_tags (tag_id);`

---

## 4. Integrity and Deletion Rules

1. **Workspace Deletion:**
   - When a workspace is deleted, all associated `categories`, `tags`, `notes`, and `note_tags` are deleted automatically (`ON DELETE CASCADE`).
2. **Category Deletion:**
   - If a category is deleted, notes assigned to it are **not** deleted; instead, their `category_id` is safely set to `NULL` (`ON DELETE SET NULL`).
3. **Note Deletion:**
   - When a note is deleted, its associations in `note_tags` are removed (`ON DELETE CASCADE`). The `tags` themselves remain available for other notes.
4. **Tag Deletion:**
   - When a tag is deleted, only the link entries in `note_tags` are deleted (`ON DELETE CASCADE`). The `notes` remain untouched.

---

## 5. PostgreSQL & SQLAlchemy Configuration

### Connection String Format:
```text
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
```

### Alembic Migrations:
- Migrations will be tracked under `backend/alembic/`.
- Every schema change must have a corresponding Alembic migration script.
