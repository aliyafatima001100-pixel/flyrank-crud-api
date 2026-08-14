from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, HTTPException, Header, Depends
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Server running and connected to Supabase")


app = FastAPI()
security = HTTPBearer()

class Task(BaseModel):
    title: str
    done: bool = False

class UserCredentials(BaseModel):
    email: str
    password: str

def get_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    try:
        user_response = supabase.auth.get_user(token)
        return user_response.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.post("/auth/signup", status_code=201)
def signup(credentials: UserCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    try:
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return {"message": "User created successfully", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", status_code=200)
def login(credentials: UserCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid login credentials")
@app.get("/tasks")
def get_tasks(current_user = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s;", (current_user.id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

@app.post("/tasks", status_code=201)
def create_task(task: Task, current_user = Depends(get_current_user)):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "INSERT INTO tasks (title, done, user_id) VALUES (%s, %s, %s) RETURNING *;",
        (task.title, task.done, current_user.id)
    )
    new_task = cursor.fetchone()
    conn.commit()
    conn.close()
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task, current_user = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s AND user_id = %s RETURNING *;",
        (task.title, task.done, task_id, current_user.id)
    )
    updated_task = cursor.fetchone()
    conn.commit()
    conn.close()
    
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s RETURNING *;", (task_id, current_user.id))
    deleted_task = cursor.fetchone()
    conn.commit()
    conn.close()
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return {"message": "Task deleted successfully"}


@app.get("/public/info", status_code=200)
def get_public_info():
    return {"message": "This info is public."}

@app.get("/protected/profile")
def get_protected_profile(current_user = Depends(get_current_user)):
    return {
        "message": "Token verified successfully using Dependency Injection!",
        "user": current_user
    }