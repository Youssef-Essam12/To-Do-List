from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine, create_tables
from models import *
import security

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    current_user = security.get_logged_user(request, db)
    if (current_user):
        tasks = db.query(TaskDB).filter(TaskDB.user_id == current_user.id).order_by(TaskDB.id).all()
        msg = request.query_params.get("msg")
        return templates.TemplateResponse("index.html", {"request": request, "tasks_list": tasks, "message": msg})
    else:
        return templates.TemplateResponse("login.html", {"request":request})    

@app.post("/add-task")
async def add_task(
        request: Request,
        title: str = Form(...),
        status: str = Form(...),
        db: Session = Depends(get_db)
):
    current_user = security.get_logged_user(request, db)
    new_task = TaskDB(title=title, status=status, user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return RedirectResponse("/", status_code=303)

@app.post("/delete-task/{task_id}")
async def delete_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = db.get(TaskDB, task_id)
    if task:
        db.delete(task)
        db.commit()
    return RedirectResponse("/", status_code=303)
    

@app.post("/toggle-task/{task_id}")
async def toggle_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.get(TaskDB, task_id)
    if task:
        task.done ^= 1
        db.commit()
    tasks = db.query(TaskDB).all()
    return RedirectResponse("/", status_code=303)

@app.get("/signup/", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup/", response_class=HTMLResponse)
async def signup(request: Request, name = Form(...), email = Form(...), password = Form(...), db = Depends(get_db)):    
    user = db.query(User).filter(User.email == email).first()
    if (not user):
        new_user = User(name=name, email=email, password_hash=security.hash_password(password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return RedirectResponse("/login/?msg=signup_ok", status_code=303)
    else:
        return templates.TemplateResponse(
            "signup.html",
            {
                "request": request,
                "message": "User already exists"
            },
            status_code=409
        )

@app.get("/login/", response_class=HTMLResponse)
async def login_page(request: Request):
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("login.html", {"request": request, "message": msg})

@app.post("/login/", response_class=HTMLResponse)
async def login(request: Request, email = Form(...), password = Form(...), db = Depends(get_db)):
    # check if email exists and verify password
    user = db.query(User).filter(User.email == email).first()
    if (user and security.verify_password(password, user.password_hash)):
        session_id = security.generate_session_id()
        security.redis_client.set(f"session_id:{session_id}", user.id, 3600)
        response = RedirectResponse(f"/?msg=Welcome Back {user.name}!", status_code=303)
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600, samesite="lax")
        return response
    else:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "message": "Login Failed"
            },
            status_code=401      
        )

@app.get("/logout/", response_class=HTMLResponse)
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    security.logout(session_id)
    return templates.TemplateResponse("login.html", {"request": request, "message": "Logged Out Successfully!"})