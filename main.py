from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# dummy database for testing
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
    """ root endpoint """
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    """ health check for server """
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks(search: str | None = None, done: bool | None = None):
    """ return all tasks or filter them """
    res = tasks

    if done is not None:
        res = [t for t in res if t["done"] == done]

    if search is not None:
        res = [t for t in res if search.lower() in t["title"].lower()]

    return res

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """ find a task by id """
    for t in tasks:
        if t["id"] == task_id:
            return t
    return JSONResponse(status_code=404, content={"error": "task not found"})

@app.post("/tasks")
def create_task(t: Task):
    """ add a new task """
    # auto-increment id logic
    new_id = len(tasks) + 1
    new_item = {"id": new_id, "title": t.title, "done": t.done}
    tasks.append(new_item)
    
    return new_item

@app.put("/tasks/{task_id}")
def update_task(task_id: int, t: Task):
    """ update title or status """
    for i, item in enumerate(tasks):
        if item["id"] == task_id:
            tasks[i]["title"] = t.title
            tasks[i]["done"] = t.done
            return tasks[i]
            
    return JSONResponse(status_code=404, content={"error": "task not found"})

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """ remove a task """
    for i, item in enumerate(tasks):
        if item["id"] == task_id:
            deleted = tasks.pop(i)
            return {"message": "deleted", "task": deleted}
            
    return JSONResponse(status_code=404, content={"error": "task not found"})