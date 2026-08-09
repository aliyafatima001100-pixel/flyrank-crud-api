# FlyRank CRUD API — Task Management System (SQLite Edition)

A RESTful CRUD API built with Python, FastAPI, and SQLite for persistent task management.

## 🗄️ Database Architecture
- **Database Engine:** SQLite3
- **Database File:** `tasks.db` (stored in project root)
- **Why SQLite?** SQLite is lightweight, serverless, zero-configuration, and stores data in a single portable file, making it ideal for local microservices and development.

## 🚀 Tech Stack
- **Language:** Python 3
- **Framework:** FastAPI
- **Database:** SQLite (`sqlite3`)
- **Data Validation:** Pydantic
- **ASGI Server:** Uvicorn

## 🛠️ Setup & Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/aliyafatima001100-pixel/flyrank-crud-api.git
   cd flyrank-crud-api
```

2. **Install dependencies:**
```bash
   pip install fastapi uvicorn pydantic
```

3. **Run the API server:**
```bash
   py -m uvicorn main:app --port 8000 --reload
```
   *(Note: `tasks.db` and the `tasks` table will be automatically created on initial launch, seeded with 3 sample tasks.)*

---

## 📋 API Endpoints

| Method | Endpoint | Description | Status Code |
| --- | --- | --- | --- |
| GET | `/` | Welcome / metadata message | `200 OK` |
| GET | `/health` | Health check endpoint | `200 OK` |
| GET | `/tasks` | Retrieve tasks (supports `search` & `done` filters) | `200 OK` |
| GET | `/tasks/{id}` | Retrieve task by ID from SQLite | `200 OK` / `404 Not Found` |
| POST | `/tasks` | Insert new task into SQLite | `201 Created` / `400 Bad Request` |
| PUT | `/tasks/{id}` | Update existing task in SQLite | `200 OK` / `400 Bad Request` / `404 Not Found` |
| DELETE | `/tasks/{id}` | Remove task from SQLite | `204 No Content` / `404 Not Found` |

---

## 🔍 SQL Exploration Queries

```sql
-- 1. List every task
SELECT * FROM tasks;

-- 2. Show only completed tasks
SELECT * FROM tasks WHERE done = 1;

-- 3. Count all tasks
SELECT COUNT(*) FROM tasks;

-- 4. Mark every task as completed
UPDATE tasks SET done = 1;

-- 5. Delete all completed tasks
DELETE FROM tasks WHERE done = 1;
```

---

## 💻 Example Request (curl)

```bash
curl -i http://localhost:8000/tasks/1
```

**Output:**
```http
HTTP/1.1 200 OK
server: uvicorn
content-type: application/json

{"id":1,"title":"Buy groceries","done":false}
```

---

## 📖 Interactive Documentation (Swagger UI)

FastAPI automatically generates interactive API documentation. Visit:

```
http://localhost:8000/docs
```
## 🐳 Docker & Database Persistence (Assignment 3)

- **Service Layer Unchanged:** I successfully swapped the SQLite database for a PostgreSQL repository. Because of the layered architecture, the API service layer and routes remained completely untouched—only the database connection logic was updated!
- **Proving Persistence:** I verified that the database data survives a restart by following these steps:
  1. Started the application and database using `docker compose up`.
  2. Created a new task via the `POST /tasks` endpoint in the Swagger UI.
  3. Stopped the Docker containers completely using `Ctrl + C`.
  4. Restarted the stack with `docker compose up`.
  5. Used the `GET /tasks` endpoint and confirmed that the test task was still present, proving the Docker volume successfully preserved the data on the hard drive.