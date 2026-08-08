# FlyRank CRUD API — Task Management System (In-Memory Edition)

A RESTful CRUD API built with Python and FastAPI. This is the Week 1 implementation using an in-memory Python list for storage.

## 🗄️ Database Architecture (Assignment 1)
- **Database Engine:** In-Memory Python List
- **Why In-Memory?** Used as an initial proof-of-concept to build out the FastAPI route logic and Pydantic validation before attaching a persistent database.

## 🚀 Tech Stack
- **Language:** Python 3
- **Framework:** FastAPI
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

3. **Run the server:**
```bash
   uvicorn main:app --reload
```

4. **Access the API:**
   Once running, open your browser and go to `http://127.0.0.1:8000/docs` to test all endpoints via the interactive Swagger UI.

---

## 📋 API Endpoints

| Method | Endpoint | Description | Expected Status |
| --- | --- | --- | --- |
| GET | `/tasks` | Retrieve all tasks | `200 OK` |
| GET | `/tasks/{id}` | Retrieve a single task by ID | `200 OK` / `404 Not Found` |
| POST | `/tasks` | Create a new task | `201 Created` / `400 Bad Request` |
| PUT | `/tasks/{id}` | Update an existing task | `200 OK` / `404 Not Found` |
| DELETE | `/tasks/{id}` | Delete a task by ID | `204 No Content` / `404 Not Found` |
