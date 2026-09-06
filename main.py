from fastapi import FastAPI, status, Response
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
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": "task not found"})

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(t: Task):
    """ add a new task """
    # manual validation to force a 400 Bad Request instead of Pydantic's 422
    if not t.title or t.title.strip() == "":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"error": "Title cannot be empty"}
        )

    # auto-increment id logic safely
    if tasks:
        new_id = max(task["id"] for task in tasks) + 1
    else:
        new_id = 1
        
    new_item = {"id": new_id, "title": t.title, "done": t.done}
    tasks.append(new_item)
    
    return new_item

@app.put("/tasks/{task_id}")
def update_task(task_id: int, t: Task):
    """ update title or status """
    if not t.title or t.title.strip() == "":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"error": "Title cannot be empty"}
        )

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks[index]["title"] = t.title
            tasks[index]["done"] = t.done
            return tasks[index]
            
    return JSONResponse(status_code=404, content={"error": "task not found"})

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """ remove a task """
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            # return a true 204 no content response
            return Response(status_code=status.HTTP_204_NO_CONTENT)
            
    return JSONResponse(status_code=404, content={"error": "task not found"})