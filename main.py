from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine, create_tables
from models import TaskDB
from Task import Task

create_tables()
app = FastAPI()

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


tasks = []

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks_list": tasks})

@app.post("/add-task")
async def add_task(
        request: Request,
        title: str = Form(...),
        state: str = Form(...)    
):
    new_task = Task(title=title, id=len(tasks)+1, state=state, done=False)
    tasks.append(new_task)
    return templates.TemplateResponse("index.html", {"request": request, "tasks_list": tasks})

@app.post("/delete-task/{task_id}")
async def delete_task(
        request: Request,
        task_id: int
):
    tasks.pop(task_id-1)
    cnt = 1
    for task in tasks:
        task.id = cnt
        cnt += 1
    return templates.TemplateResponse("index.html", {"request": request, "tasks_list": tasks})

@app.post("/toggle-task/{task_id}")
async def toggle_task(
    request: Request,
    task_id: int
):
    tasks[task_id-1].done ^= 1
    return templates.TemplateResponse("index.html", {"request": request, "tasks_list": tasks})