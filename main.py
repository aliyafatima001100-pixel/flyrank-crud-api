from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# This is our in-memory "database"
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Finish internship assignment", "done": False}
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Endpoint to get ALL tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# Endpoint to get ONE specific task by its ID number
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    # If the loop finishes and doesn't find it, return a 404 error
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
#stage 2 done