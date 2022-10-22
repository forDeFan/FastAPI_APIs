from app.api.forms.login_form import Login_Form
from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from app.core.user_repo import User_Repo

templates = Jinja2Templates(directory="app/web/templates/")
login_router = APIRouter()


@login_router.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@login_router.post("/login")
async def login(request: Request):
    form = Login_Form(request)
    await form.load_data()
    if await form.is_valid():
        user = await User_Repo.get_by_username(username=form.username)
        if user is not None:
            if user.password == form.password:
                form.__dict__.update(msg="Login Successful :)")
            else:
                form.errors.append("You provided wrong data.")
        else:
            form.errors.append("Incorrect email or password :(")
    return templates.TemplateResponse("login.html", form.__dict__)
