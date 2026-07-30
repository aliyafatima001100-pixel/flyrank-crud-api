from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Finish internship assignment", "done": False}
]

# This defines the "shape" of the data we expect from the user
class Task(BaseModel):
    title: str
    done: bool = False

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

#stage 3 work
@app.post("/tasks")
def create_task(new_task: Task):
    # Calculate the next available ID
    new_id = len(tasks) + 1
    
    # Creating dictionary
    task_dict = {
        "id": new_id,
        "title": new_task.title,
        "done": new_task.done
    }
    
    # Append it to list
    tasks.append(task_dict)
    
    # Send the newly created task back to the client
    return task_dict