# RecallBox – Development Plan

**Project:** RecallBox  
**Version:** V1.0  
**Document:** Development Plan  
**Status:** Initial Development Plan

---

# 1. Project Overview

RecallBox is a personal note-taking application where users can create a private workspace and manage their notes in one place.

The application will allow users to create, access, organize, search, edit and delete their notes.

The project will be developed as a full-stack web application using React and FastAPI, with PostgreSQL as the database.

The development will be divided into multiple phases. Each phase must be implemented, tested and verified before moving to the next phase.

# 2. Technology Stack

The following technologies are selected for V1.0.

| Area | Technology | Purpose |
|---|---|---|
| Frontend framework | React | Build the user interface |
| Frontend build tool | Vite | Development server and production build |
| Frontend language | TypeScript | Type safety |
| CSS framework | Tailwind CSS | Application styling |
| Frontend routing | React Router | Page navigation |
| Backend language | Python | Backend development |
| Backend framework | FastAPI | REST API development |
| Data validation | Pydantic | Request and response validation |
| ORM | SQLAlchemy | Database operations |
| Database | Supabase PostgreSQL | Persistent data storage |
| API testing | Postman and Swagger UI | API testing |
| Version control | Git and GitHub | Source code management |
| Containerization | Docker | Package applications into containers |
| Container orchestration | Docker Compose | Run frontend and backend together locally |
| Container registry | Docker Hub | Store Docker images |
| Code editor | Visual Studio Code | Development environment |

### Technology decisions

1. Use React with Vite and TypeScript. Do not use Next.js for V1.0.
2. Maintain frontend and backend as separate applications.
3. Use FastAPI as the only backend API layer.
4. Use Supabase as a hosted PostgreSQL database.
5. Frontend application operations must communicate with FastAPI through REST APIs.
6. Frontend must not directly access the PostgreSQL database.
7. Use Docker and Docker Compose for local containerization and deployment preparation.

# 3. Project Folder Structure

Maintain a single Git repository with separate frontend and backend directories.

```text
RecallBox/
│
├── documentation/
│   ├── SRS.md
│   ├── DEVELOPMENT_PLAN.md
│   ├── DATABASE_DESIGN.md
│   ├── API_DOCUMENTATION.md
│   ├── TECHNICAL_DESIGN.md
│   └── DEVELOPMENT_PROGRESS.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── types/
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── db/
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── .gitignore
├── .env.example
├── AI_PROJECT_INSTRUCTIONS.md
└── README.md
```

The structure may be extended when required, but avoid unnecessary folders and abstractions.

# 4. Development Approach

Development must follow an incremental approach.

- Implement one phase at a time.
- Break each phase into small, manageable tasks.
- Complete the backend and frontend requirements for a feature before considering it finished.
- Test every feature before moving forward.
- Follow the approved SRS and technical documentation.
- Do not introduce additional features outside V1.0 scope.
- Update development progress after completing each task.
- Do not generate the entire application in a single AI coding request.

# 5. Development Phases

## Phase 1 – Project Initialization and Setup

**Objective:** Establish the initial project structure and development environment.

### Backend tasks
- Create the Python virtual environment.
- Install FastAPI and initial dependencies.
- Create the FastAPI application entry point.
- Configure the development server.
- Add a basic health-check endpoint.
- Configure environment variable loading.
- Verify that the backend starts successfully.

### Frontend tasks
- Create a React application using Vite and TypeScript.
- Configure Tailwind CSS.
- Install and configure React Router.
- Create the initial application structure.
- Create a basic application layout.
- Verify that the frontend starts successfully.

### Repository tasks
- Initialize Git.
- Create the GitHub repository.
- Add `.gitignore`.
- Add `.env.example`.
- Ensure secrets and environment files are not committed.

**Completion criteria:**
- Frontend runs independently.
- Backend runs independently.
- Frontend and backend folders are separated.
- Both applications can be developed locally.

## Phase 2 – Database Design and Integration

**Objective:** Design and connect the PostgreSQL database.

### Tasks
- Create a Supabase project.
- Configure PostgreSQL connection details.
- Finalize the database schema.
- Define primary keys and foreign keys.
- Define table relationships.
- Create SQLAlchemy models.
- Configure SQLAlchemy database sessions.
- Configure database migrations.
- Verify database connectivity.

### Initial database tables

1. workspaces
2. notes
3. categories
4. tags
5. note_tags

The exact columns, data types, indexes, constraints and relationships must be defined in `DATABASE_DESIGN.md` before implementation.

**Completion criteria:**
- All approved tables are created.
- Relationships and constraints work correctly.
- FastAPI can connect to PostgreSQL.
- Database migrations can be applied successfully.

## Phase 3 – Backend Foundation

**Objective:** Establish a clean and maintainable backend architecture.

### Tasks
- Configure API routing.
- Organize application configuration.
- Implement request and response schemas.
- Configure centralized exception handling.
- Configure CORS for the frontend development origin.
- Establish service and repository responsibilities.
- Configure API versioning using `/api/v1`.
- Configure structured logging.
- Add backend test configuration.

**Completion criteria:**
- API structure is established.
- Validation and error responses are consistent.
- Backend can support subsequent feature development.

## Phase 4 – Workspace Management

**Objective:** Allow users to create and access private workspaces.

### Features
- Create a workspace.
- Generate a unique workspace ID.
- Generate a secure access key.
- Store only the access key hash in the database.
- Access a workspace using its ID and access key.
- Validate workspace credentials.
- Issue a short-lived access token after successful validation.
- Protect workspace-specific API endpoints.
- Enforce workspace-level data isolation.

### Security requirements
- Never store plaintext access keys.
- Never return stored access key hashes.
- Never expose credentials in application logs.
- Use secure token validation.
- Validate workspace ownership or access on every protected operation.
- Do not trust a workspace ID supplied by the frontend as proof of authorization.

**Completion criteria:**
- Workspace creation works.
- Workspace access works.
- Invalid credentials are rejected.
- Protected APIs require valid access.
- One workspace cannot access another workspace's data.

## Phase 5 – Frontend Foundation and Workspace Screens

**Objective:** Build the initial user interface and connect it to the backend.

### Pages
- Welcome page.
- Create Workspace page.
- Open Workspace page.
- Dashboard layout.

### Tasks
- Configure application routing.
- Build reusable UI components.
- Create common layouts.
- Create API service functions.
- Connect frontend to FastAPI.
- Implement workspace creation flow.
- Implement workspace access flow.
- Handle loading, success and error states.
- Handle access-token storage and expiration according to the approved security design.

**Completion criteria:**
- Users can create a workspace from the frontend.
- Users can open an existing workspace.
- Invalid access attempts show suitable errors.
- Successful access takes users to the dashboard.

## Phase 6 – Note Management

**Objective:** Implement the main functionality of RecallBox.

### Backend tasks
- Create note API endpoints.
- Implement note creation.
- Implement note retrieval.
- Implement note updates.
- Implement note deletion.
- Validate all note operations against the authorized workspace.
- Support pagination.

### Frontend tasks
- Create Notes Library page.
- Create Note page.
- View Note page.
- Edit Note page.
- Implement note forms.
- Display notes in the library.
- Implement delete confirmation.
- Show appropriate success and error messages.

### Note fields
- Title – required.
- Content – required.
- Category – optional.
- Tags – optional.
- Created timestamp – automatic.
- Updated timestamp – automatic.

**Completion criteria:**
- Users can create, view, edit and delete notes.
- Notes are persisted in PostgreSQL.
- Notes are visible only within their authorized workspace.
- Form validation works correctly.

## Phase 7 – Categories and Tags

**Objective:** Allow users to organize their notes.

### Categories
- Create categories.
- Retrieve categories.
- Update category names.
- Delete categories.
- Assign a category to a note.
- Filter notes by category.

### Tags
- Create and manage tags.
- Assign multiple tags to a note.
- Remove tags from notes.
- Filter notes by tag.

### Rules
- Categories and tags belong to a workspace.
- A note can have zero or one category.
- A note can have multiple tags.
- Prevent duplicate category or tag names within the same workspace where required.
- Ensure deletion does not leave invalid relationships.

**Completion criteria:**
- Categories and tags work correctly.
- Notes can be organized using categories and tags.
- Workspace isolation is maintained.

## Phase 8 – Search and Filtering

**Objective:** Make it easy to find saved notes.

### Features
- Search notes by title.
- Search notes by content.
- Filter by category.
- Filter by tag.
- Combine search and filters.
- Support pagination.

**Completion criteria:**
- Search returns relevant matching notes.
- Filters work correctly.
- Search and filters can be combined.
- Results are restricted to the authorized workspace.

## Phase 9 – Testing and Quality Assurance

**Objective:** Verify the complete application before containerization.

### Backend testing
- Test workspace creation.
- Test workspace access.
- Test token validation.
- Test note CRUD operations.
- Test category and tag operations.
- Test search and filtering.
- Test workspace isolation.
- Test invalid inputs and error cases.

### Frontend testing
- Test page navigation.
- Test workspace creation and access.
- Test note creation, editing and deletion.
- Test category and tag operations.
- Test search and filtering.
- Test loading and error states.

### Integration testing
- Verify frontend-to-backend communication.
- Verify backend-to-database communication.
- Test complete user workflows.
- Verify unauthorized requests are rejected.

**Completion criteria:**
- Critical application workflows pass.
- No known critical security or data-isolation issues remain.
- The application is ready for Docker setup.

## Phase 10 – Docker and Containerization

**Objective:** Containerize frontend and backend applications.

### Tasks
- Create frontend Dockerfile.
- Create backend Dockerfile.
- Configure production build for React.
- Configure FastAPI production startup.
- Configure Docker Compose.
- Configure environment variables.
- Configure container networking.
- Configure health checks.
- Verify frontend can communicate with backend inside the deployment environment.
- Build and run containers locally.

### Important
- PostgreSQL will remain hosted on Supabase.
- Do not create a PostgreSQL container for the initial deployment.
- Do not include production secrets in Docker images.
- Use appropriate production server configuration.
- Use Docker volumes only where persistent container storage is required.

**Completion criteria:**
- Frontend container builds and runs.
- Backend container builds and runs.
- Docker Compose starts the application successfully.
- Application communicates with Supabase PostgreSQL.

## Phase 11 – Docker Hub and Cloud Deployment

**Objective:** Deploy RecallBox to a cloud environment.

### Tasks
- Create Docker Hub repository.
- Build production images.
- Tag images with appropriate version numbers.
- Push images to Docker Hub.
- Prepare a cloud server.
- Install and configure Docker.
- Configure production environment variables securely.
- Pull images from Docker Hub.
- Start containers using Docker Compose.
- Configure domain and HTTPS if required.
- Verify production frontend and backend communication.
- Perform final application testing.

**Completion criteria:**
- Application is accessible from the deployment environment.
- Frontend and backend work correctly.
- Database connectivity is successful.
- Production configuration is secure.
- Main V1.0 workflows work as expected.

# 6. Development Order and Dependencies

The phases should follow this order:

1. Project initialization.
2. Database design and integration.
3. Backend foundation.
4. Workspace management.
5. Frontend foundation and workspace screens.
6. Note management.
7. Categories and tags.
8. Search and filtering.
9. Testing and quality assurance.
10. Docker and containerization.
11. Docker Hub and cloud deployment.

Some frontend and backend tasks can be developed in parallel once their API contracts and database requirements are finalized. However, dependencies must not be skipped.

# 7. AI Development Instructions

Any AI coding assistant working on RecallBox must follow these rules.

1. Read `SRS.md` and `DEVELOPMENT_PLAN.md` before implementing features.
2. Read the relevant technical and database documents before making architectural decisions.
3. Follow the approved technology stack.
4. Use React, Vite and TypeScript. Do not introduce Next.js.
5. Keep frontend and backend code in separate folders.
6. Use FastAPI for backend API operations.
7. Use Supabase PostgreSQL as the database.
8. Follow the established folder structure and coding conventions.
9. Implement one feature at a time.
10. Do not skip testing.
11. Do not introduce features outside V1.0 scope without approval.
12. Do not hardcode credentials, tokens or secrets.
13. Do not change the database schema without updating the database documentation.
14. Do not introduce unnecessary libraries or architectural complexity.
15. Explain significant architectural decisions before making changes.
16. Update `DEVELOPMENT_PROGRESS.md` after completing each task.
17. If requirements are unclear or contradictory, ask for clarification rather than guessing.
18. Verify that existing functionality continues to work after changes.

# 8. Development Progress Tracking

Maintain `DEVELOPMENT_PROGRESS.md` to track implementation.

Each task should have one of these statuses:

- Not Started
- In Progress
- Completed
- Blocked

For each completed task, record:
- What was implemented.
- Important files created or modified.
- Tests performed.
- Any known issues.
- Next recommended task.

Do not mark a phase complete until its completion criteria have been verified.

# 9. Version Management

The initial target release is V1.0.

| Version | Scope |
|---|---|
| V1.0 | Workspace management, notes, categories, tags, search and Docker deployment |
| V1.1 | Potential improvements to the existing V1 functionality |
| V2.0 | Potential major enhancements such as user accounts, attachments and AI features |

Future versions are not part of the current implementation scope.

# 10. Final Development Goal

The goal of V1.0 is to deliver a working, tested and Dockerized RecallBox application.

A successful V1.0 release must allow users to:

- Create a private workspace.
- Access the workspace securely.
- Create, view, edit and delete notes.
- Organize notes using categories and tags.
- Search and filter notes.
- Access only their own workspace data.
- Run the application using Docker.
- Deploy the application using Docker images.

All implementation decisions must support this goal without unnecessarily increasing project complexity.
