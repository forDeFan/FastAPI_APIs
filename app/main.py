from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.db.db import database, engine, metadata
from app.core.db.user_model import User

app = FastAPI()
app.mount("/static",
          StaticFiles(directory="app/web/static/styles"), name="static")
templates = Jinja2Templates(directory="app/web/templates/")

metadata.create_all(engine)


@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    return templates.TemplateResponse(name="home.html", context={"request": request})


@app.get("/user/all", response_class=HTMLResponse)
async def get_all_users(request: Request):
    users = await User.objects.all()
    return templates.TemplateResponse(name="users.html", context={"request": request, "users": users})


@app.post("/user/", response_class=HTMLResponse)
async def add_user(request: Request, username: str, email: str, password: str):
    await User.objects.create(username=username, email=email, password=password)
    users = await User.objects.all()
    return templates.TemplateResponse(name="users.html", context={"request": request, "users": users})


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
