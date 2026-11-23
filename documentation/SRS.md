# RecallBox – Software Requirements Specification (SRS)

**Document Version:** 1.0  
**Project Name:** RecallBox  
**Release:** V1.0 – Initial Release  
**Document Status:** Initial Specification  
**Architecture:** React + FastAPI + Supabase PostgreSQL + Docker

---

## 1. Project Overview

### 1.1 Introduction

RecallBox is a simple, workspace-based personal note management application.

The application allows users to create their own workspace and save, organize, search, edit, and manage personal notes in one centralized location.

The primary objective is to provide users with a simple place to store their knowledge, learning materials, technical explanations, and personal notes.

### 1.2 Problem Statement

People often save their knowledge across different platforms, documents, applications, and files.

This makes it difficult to organize information and retrieve previously saved knowledge.

RecallBox aims to solve this problem by providing a centralized platform for personal note management.

### 1.3 Project Objectives

- Provide a centralized location for personal notes.
- Allow users to create and access their own workspaces.
- Make note creation and management simple.
- Organize notes using categories and tags.
- Provide search functionality to retrieve saved information.
- Maintain data separation between different workspaces.

---

## 2. Project Scope

### 2.1 Features Included in V1.0

1. Workspace creation.
2. Workspace access using workspace ID and access key.
3. Dashboard.
4. Create notes.
5. View notes.
6. Edit notes.
7. Delete notes.
8. Categories.
9. Tags.
10. Search notes.

### 2.2 Features Excluded from V1.0

The following features are explicitly excluded from the initial release:

- User registration and traditional login.
- Google authentication.
- Bookmark management.
- Code snippet management.
- File and PDF uploads.
- AI-powered features.
- Collaboration and shared editing.
- Public note sharing.
- Advanced analytics.
- Mobile applications.

These features may be considered for future releases.

---

## 3. User and Workspace Management

### 3.1 Workspace Creation

The application must allow a visitor to create a new workspace without registering an account.

The user must provide a workspace name.

The system must automatically generate:

- A unique workspace ID.
- A secure access key.

The application must display the workspace ID and access key after successful creation.

The user must be informed to save these credentials because they will be required to access the workspace later.

### 3.2 Workspace Access

Users must be able to access an existing workspace by providing:

- Workspace ID.
- Access key.

The backend must validate these credentials before granting access.

If the credentials are valid, the user can access the corresponding workspace.

If the credentials are invalid, the application must display an appropriate error message.

### 3.3 Workspace Security

- Workspace IDs must be unique.
- Access keys must be generated securely.
- Access keys must never be stored as plain text in the database.
- The backend must store only securely hashed access keys.
- Workspace access must be validated by the backend.
- Users must not be able to access another workspace's notes.
- Workspace access credentials must not be exposed in application logs or API responses unnecessarily.

The backend should issue a short-lived access token after successful workspace validation. Protected operations must require this token.

V1.0 does not include account recovery or password reset functionality.

---

## 4. Dashboard

After successfully accessing a workspace, the user must be redirected to the dashboard.

The dashboard should provide:

- Workspace name.
- Total number of notes.
- Recently created or updated notes.
- Quick access to create a new note.
- Quick access to the complete notes library.

The dashboard should remain simple and easy to navigate.

---

## 5. Note Management

Note management is the primary functionality of RecallBox.

### 5.1 Create Note

Users must be able to create a new note.

Each note must contain the following information:

| Field | Description | Required |
|---|---|---|
| Title | Title of the note | Yes |
| Content | Main note content | Yes |
| Category | Category assigned to the note | No |
| Tags | Labels associated with the note | No |
| Created At | Creation timestamp | Automatic |
| Updated At | Last modification timestamp | Automatic |

Expected workflow:

1. User selects Create Note.
2. Application displays the note creation form.
3. User enters a title and content.
4. User optionally selects a category and adds tags.
5. User clicks Save.
6. Backend validates the request.
7. Note is saved in the database.
8. Application displays a success message.

### 5.2 View Notes

Users must be able to view all notes belonging to their workspace.

The notes library should display:

- Note title.
- Short content preview.
- Category.
- Tags.
- Last updated date.

Users must be able to open a note to view its complete content.

### 5.3 Edit Note

Users must be able to update an existing note.

They should be able to modify:

- Title.
- Content.
- Category.
- Tags.

The updated timestamp must change whenever a note is modified.

### 5.4 Delete Note

Users must be able to delete notes.

Before deletion, the application should display a confirmation message.

Once confirmed, the note must be deleted from the database.

### 5.5 Note Validation

- Title is mandatory.
- Content is mandatory.
- Empty or whitespace-only titles must not be accepted.
- Empty or whitespace-only content must not be accepted.
- The note must belong to a valid workspace.
- Only authorized workspace users can modify or delete their notes.

---

## 6. Category Management

Categories allow users to organize their notes based on topics.

Examples:

- Python
- JavaScript
- React
- FastAPI
- Docker
- Database
- Personal

V1.0 requirements:

- Users must be able to assign a category to a note.
- Users must be able to select an existing category.
- Users must be able to create a category when needed.
- Categories must belong to a workspace.
- Users must be able to filter notes by category.

A note can belong to one category. Category selection is optional.

---

## 7. Tag Management

Tags provide another way to organize notes.

For example, a Python note could contain:

- Advanced Python
- Decorators
- Functions
- Programming

V1.0 requirements:

- Users must be able to add multiple tags to a note.
- Users must be able to reuse existing tags.
- Users must be able to create new tags.
- Users must be able to filter notes using tags.

Tags are optional.

---

## 8. Search Functionality

Users must be able to search their saved notes.

The search functionality should initially support searching by:

- Note title.
- Note content.

Users must also be able to filter results by category.

Search results must only include notes belonging to the currently accessed workspace.

---

## 9. Application Pages

The application must contain the following pages:

| Page | Responsibility |
|---|---|
| Welcome Page | Create or access a workspace |
| Create Workspace | Create a new personal workspace |
| Open Workspace | Enter workspace ID and access key |
| Dashboard | Display workspace overview |
| Notes Library | Display all saved notes |
| Create Note | Create a new note |
| View Note | Display complete note information |
| Edit Note | Update an existing note |

The application must provide consistent navigation between these pages.

---

## 10. Database Requirements

The application will use Supabase PostgreSQL as its database.

The initial database design will contain three main entities.

### 10.1 Workspaces

Stores workspace information.

Expected fields:

- id
- name
- access_key_hash
- created_at

### 10.2 Categories

Stores workspace-specific categories.

Expected fields:

- id
- workspace_id
- name
- created_at

### 10.3 Notes

Stores all notes.

Expected fields:

- id
- workspace_id
- category_id (nullable)
- title
- content
- created_at
- updated_at

### 10.4 Tags

Tags will be maintained through two tables:

**Tags**
- id
- workspace_id
- name
- created_at

**Note_Tags**
- note_id
- tag_id

This relationship allows multiple tags to be assigned to a note and allows tags to be reused across notes.

All workspace-related relationships must enforce data isolation.

The final schema must include appropriate primary keys, foreign keys, uniqueness constraints, and indexes.

---

## 11. Technology Stack

### Frontend
- React
- Vite
- Tailwind CSS
- React Router
- Fetch API or Axios for backend communication

### Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy or an appropriate PostgreSQL database integration

### Database
- Supabase PostgreSQL

### Deployment and Infrastructure
- Docker
- Docker Compose
- Docker Hub
- Cloud server

### Source Code Management
- Git
- GitHub

The frontend and backend must communicate through REST APIs.

The backend will be responsible for business logic, validation, workspace access, and database operations.

The frontend must not connect directly to the database for application operations.

---

## 12. Non-Functional Requirements

### 12.1 Security

- Workspace data must remain isolated.
- All protected API endpoints must validate workspace authorization.
- Access keys must be securely hashed.
- Database credentials must be stored in environment variables.
- Sensitive configuration must never be committed to GitHub.
- Production communication must use HTTPS.
- Input validation must be implemented on the backend.

### 12.2 Performance

- Notes should load efficiently.
- Search should return results without unnecessary delays.
- Database queries should use appropriate indexes.
- The application should support pagination when the number of notes increases.

### 12.3 Usability

- The interface should be simple and intuitive.
- The application should be responsive.
- Forms should provide meaningful validation messages.
- Users should receive feedback after successful or failed operations.

### 12.4 Maintainability

- Frontend and backend code must be organized separately.
- API responsibilities should be clearly separated.
- Reusable components should be preferred.
- Environment-specific configurations should be maintained separately.
- The application must support Docker-based development and deployment.

---

## 13. Deployment Requirements

The application must support containerized deployment.

The deployment architecture should include:

- A Dockerfile for the React frontend.
- A Dockerfile for the FastAPI backend.
- Docker Compose for managing application containers.
- Supabase PostgreSQL as the external hosted database.
- Environment variables for application configuration.

The Docker images should be pushed to Docker Hub.

The cloud server should be able to pull the images and run the application.

GitHub will be used to maintain the source code and version history.

---

## 14. Acceptance Criteria

RecallBox V1.0 will be considered ready for its initial release when:

1. A user can create a workspace successfully.
2. A user can access an existing workspace using valid credentials.
3. Invalid workspace credentials are rejected.
4. A user can create notes.
5. A user can view all notes in their workspace.
6. A user can edit existing notes.
7. A user can delete notes.
8. A user can create and assign categories.
9. A user can create and assign tags.
10. A user can search notes by title and content.
11. Workspace data remains isolated.
12. The application runs successfully using Docker.
13. The application can be deployed to a cloud server.

---

## 15. Future Enhancements

The following features may be considered for future releases:

- Rich text and Markdown editor.
- File and PDF attachments.
- User registration and authentication.
- Google authentication.
- AI-powered note summarization.
- Semantic search.
- Bookmark management.
- Code snippet management.
- Note sharing.
- Mobile application.

These enhancements are not part of V1.0.

---

## 16. Version History

| Version | Description | Status |
|---|---|---|
| 1.0 | Initial note management application specification | Initial release |

**End of Document**

**Project:** RecallBox  
**Specification:** V1.0  
**Purpose:** Primary requirements reference for development and AI-assisted implementation.