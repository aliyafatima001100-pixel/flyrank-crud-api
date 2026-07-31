from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Finish internship assignment", "done": False}
]

class Task(BaseModel):
    title: str
    done: bool = False

@app.get("/")
def read_root():
    """Welcome message and API details."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    """Check if the server is running and healthy."""
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    """Get the complete list of tasks."""
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by its ID number."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": "Task not found"})

@app.post("/tasks")
def create_task(new_task: Task):
    """Create a brand new task."""
    new_id = len(tasks) + 1
    task_dict = {"id": new_id, "title": new_task.title, "done": new_task.done}
    tasks.append(task_dict)
    return task_dict

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    """Update an existing task's title or status."""
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks[index]["title"] = updated_task.title
            tasks[index]["done"] = updated_task.done
            return tasks[index]
    return JSONResponse(status_code=404, content={"error": "Task not found"})

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task completely."""
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            return {"message": "Task deleted successfully", "task": deleted_task}
    return JSONResponse(status_code=404, content={"error": "Task not found"})