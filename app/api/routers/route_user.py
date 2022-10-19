from app.api.forms.add_user_form import Add_User_Form
from app.api.forms.check_user_form import Check_User_Form
from app.api.forms.update_user_pass_form import Update_User_Pass_Form
from app.core.user_repo import User_Repo
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/web/templates/")
user_router = APIRouter()


@user_router.get("/user", response_class=HTMLResponse)
async def get_user_operations(request: Request) -> Jinja2Templates:
    return templates.TemplateResponse(name="user/user_operations.html", context={"request": request})


@user_router.get("/user/get/all", response_class=HTMLResponse)
async def get_all_users(request: Request) -> Jinja2Templates:
    users = await User_Repo.get_all()
    return templates.TemplateResponse(name="user/user_all.html", context={"request": request, "users": users})


@user_router.post("/user/get", response_class=HTMLResponse)
async def get_user(request: Request) -> Jinja2Templates:
    form = Check_User_Form(request=request)
    await form.load_data()
    if await form.is_valid():
        user = await User_Repo.get_by_username(username=form.username)
        if user is not None:
            response = templates.TemplateResponse(
                name="user/user_info.html", context={"request": request, "user": user})
            return response
        else:
            form.errors.append("No such user !")
    return templates.TemplateResponse("user/user_operations.html", form.__dict__)


@user_router.post("/user/update", response_class=HTMLResponse)
async def update_user_password(request: Request) -> Jinja2Templates:
    form = Update_User_Pass_Form(request=request)
    await form.load_data()
    if await form.is_valid():
        user = await User_Repo.get_by_username(username=form.username)
        if user is not None:
            if user.password == form.old_password:
                await User_Repo.update_user_password(username=form.username, password=form.new_password)
                form.__dict__.update(
                    msg=f"Password for user: {form.username}, changed successfully.")
            else:
                form.errors.append("Wrong old password provided!")
        else:
            form.errors.append("No such user!")
    return templates.TemplateResponse("user/user_operations.html", form.__dict__)


@user_router.post("/user/add", response_class=HTMLResponse)
async def add_user(request: Request) -> Jinja2Templates:
    form = Add_User_Form(request=request)
    await form.load_data()
    if await form.is_valid():
        user = await User_Repo.add_user(username=form.username, email=form.email, password=form.password)
        if user is not None:
            form.__dict__.update(
                msg=f"User with username: {form.username}, added succesfully.")
        else:
            form.errors.append(
                "User already exists with this username or email.")
    return templates.TemplateResponse("user/user_operations.html", form.__dict__)


@user_router.post("/user/delete", response_class=HTMLResponse)
async def delete_user(request: Request) -> Jinja2Templates:
    form = Check_User_Form(request=request)
    await form.load_data()
    if await form.is_valid():
        user = await User_Repo.delete_user(username=form.username)
        if user == True:
            form.__dict__.update(
                msg=f"User with username: {form.username}, deleted succesfully.")
        else:
            form.errors.append(
                "No such user!")
    return templates.TemplateResponse("user/user_operations.html", form.__dict__)
