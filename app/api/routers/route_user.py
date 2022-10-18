from app.api.forms.add_user_form import Add_User_Form
from app.api.forms.check_user_form import Check_User_Form
from app.core.user_repo import User_Repo
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/web/templates/")
user_router = APIRouter()


@user_router.get("/user", response_class=HTMLResponse)
async def get_user_operations(request: Request) -> Jinja2Templates:
    return templates.TemplateResponse(name="user/user_operations.html", context={"request": request})


@user_router.get("/user/all", response_class=HTMLResponse)
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


@user_router.patch("/user/", response_class=HTMLResponse)
async def update_user_password(request: Request, username: str, password: str) -> Jinja2Templates:
    user = await User_Repo.update_user_password(username=username, password=password)
    if user is None:
        return templates.TemplateResponse(name="error/error_general.html", context={"request": request})
    else:
        updated_user = await User_Repo.get_by_username(username=username)
        return templates.TemplateResponse(name="user/user_info.html", context={"request": request, "user": updated_user})


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
                "User already exists with this username or email")
    return templates.TemplateResponse("user/user_operations.html", form.__dict__)


@user_router.delete("/user/", response_class=HTMLResponse)
async def delete_user(request: Request, username: str) -> Jinja2Templates:
    user = await User_Repo.delete_user(username=username)
    users = await User_Repo.get_all()
    if user:
        return templates.TemplateResponse(name="user/user_all.html", context={"request": request, "users": users})
    else:
        return templates.TemplateResponse(name="error/error_general.html", context={"request": request})
