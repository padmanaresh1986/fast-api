from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4

app = FastAPI()

# In-memory database
tasks_db = {}

# Pydantic model for task
class Task(BaseModel):
    title: str
    description: str
    status: str

# Create a new task
@app.post("/tasks", response_model=dict)
def create_task(task: Task):
    task_id = str(uuid4())
    new_task = {"id": task_id, **task.dict()}
    tasks_db[task_id] = new_task
    return new_task

# Get all tasks
@app.get("/tasks", response_model=list)
def get_tasks():
    return list(tasks_db.values())

# Get a specific task
@app.get("/tasks/{task_id}", response_model=dict)
def get_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

# Update a task
@app.put("/tasks/{task_id}", response_model=dict)
def update_task(task_id: str, updated_task: Task):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[task_id].update(updated_task.dict())
    return tasks_db[task_id]

# Delete a task
@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]
    return {"message": "Task deleted successfully"}