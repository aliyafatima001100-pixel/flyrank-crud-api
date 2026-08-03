import sqlite3
from fastapi import FastAPI, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()
DB_NAME = "tasks.db"

def get_db_connection():
    # Open a connection to the SQLite database
    conn = sqlite3.connect(DB_NAME)
    # lets us access columns using names like row["title"]
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    # Create the tasks table and add sample data the first time the app runs
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Creating the table if it hasn't been created already
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()

    # Add sample tasks if no data in table
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.executemany("""
            INSERT INTO tasks (title, done) VALUES (?, ?)
        """, [
            ("Buy groceries", 0),
            ("Learn FastAPI", 1),
            ("Finish internship assignment", 0)
        ])
        conn.commit()
    
    conn.close()

# Set up  database 
@app.on_event("startup")
def startup_event():
    init_db()

class Task(BaseModel):
    title: str
    done: bool = False

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "2.0 (SQLite)", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks(search: str | None = None, done: bool | None = None):
    # Return all tasks, or filter them if search or done is provided
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT id, title, done FROM tasks WHERE 1=1"
    params = []

    if done is not None:
        query += " AND done = ?"
        params.append(1 if done else 0)

    if search is not None:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [{"id": r["id"], "title": r["title"], "done": bool(r["done"])} for r in rows]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    # Look up a task by ID
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={"error": "task not found"}
        )
    
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(t: Task):
    # Add task
    if not t.title or t.title.strip() == "":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"error": "Title cannot be empty"}
        )

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (t.title.strip(), 1 if t.done else 0)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"id": new_id, "title": t.title.strip(), "done": t.done}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, t: Task):
    # Update task
    if not t.title or t.title.strip() == "":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"error": "Title cannot be empty"}
        )

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # the task exists before updating it
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if cursor.fetchone() is None:
        conn.close()
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={"error": "task not found"}
        )

    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (t.title.strip(), 1 if t.done else 0, task_id)
    )
    conn.commit()
    conn.close()

    return {"id": task_id, "title": t.title.strip(), "done": t.done}

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    # Delete a task from the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # to ensure that the task exists before updating it
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if cursor.fetchone() is None:
        conn.close()
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={"error": "task not found"}
        )

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return Response(status_code=status.HTTP_204_NO_CONTENT)