from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from Task import *

app = FastAPI()

templates = Jinja2Templates(directory="templates")
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