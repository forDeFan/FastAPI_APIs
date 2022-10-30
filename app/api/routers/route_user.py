from app.api.forms.add_user_form import AddUserForm
from app.api.forms.check_user_form import CheckUserForm
from app.api.forms.update_user_pass_form import UpdateUserPassForm
from app.core.config import settings
from app.core.security.jwt_handler import oauth2_scheme
from app.core.user_repo import UserRepo
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/web/templates/")
user_router = APIRouter()


def is_logged_in(request: Request) -> bool:
    if not settings.COOKIE_NAME in request.cookies:
        return False
    return True


@user_router.get("/user", response_class=HTMLResponse)
async def get_user_operations(request: Request) -> Jinja2Templates:
    return templates.TemplateResponse(
        name="user/user_operations.html", context={"request": request}
    )


@user_router.get("/user/get/all", response_class=HTMLResponse)
async def get_all_users(request: Request) -> Jinja2Templates:
    users = await UserRepo.get_all()
    return templates.TemplateResponse(
        name="user/user_all.html", context={"request": request, "users": users}
    )


@user_router.post("/user/get", response_class=HTMLResponse)
async def get_user(request: Request) -> Jinja2Templates:
    form = CheckUserForm(request=request)
    await form.load_data()
    if await form.is_valid():
        user = await UserRepo.get_by_username(username=form.username)
        if user is not None:
            response = templates.TemplateResponse(
                name="user/user_info.html", context={"request": request, "user": user}
            )
            return response
        else:
            form.errors.append("No such user !")
    return templates.TemplateResponse("user/user_operations.html", form.__dict__)


@user_router.post("/user/update", response_class=HTMLResponse)
async def update_user_password(request: Request) -> Jinja2Templates:
    form = UpdateUserPassForm(request=request)
    await form.load_data()
    if await form.is_valid():
        if not is_logged_in(request=request):
            form.errors.append("Update not allowed without log in!")
        else:
            user = await UserRepo.get_by_username(username=form.username)
            if user is not None:
                if user.password == form.old_password:
                    await UserRepo.update_user_password(
                        username=form.username, password=form.new_password
                    )
                    form.__dict__.update(
                        msg=f"Password for user: {form.username}, changed successfully."
                    )
                else:
                    form.errors.append("Wrong old password provided!")
            else:
                form.errors.append("No such user!")
    return templates.TemplateResponse("user/user_operations.html", form.__dict__)


@user_router.post(
    "/user/add", dependencies=[Depends(oauth2_scheme)], response_class=HTMLResponse
)
async def add_user(request: Request) -> Jinja2Templates:
    form = AddUserForm(request=request)
    await form.load_data()
    if await form.is_valid():
        if not is_logged_in(request=request):
            form.errors.append("Adding not allowed without log in!")
        else:
            user = await UserRepo.add_user(
                username=form.username, email=form.email, password=form.password
            )
            if user is not None:
                form.__dict__.update(
                    msg=f"User with username: {form.username}, added succesfully."
                )
    return templates.TemplateResponse("user/user_operations.html", form.__dict__)


@user_router.post(
    "/user/delete", dependencies=[Depends(oauth2_scheme)], response_class=HTMLResponse
)
async def delete_user(request: Request) -> Jinja2Templates:
    form = CheckUserForm(request=request)
    await form.load_data()
    if await form.is_valid():
        if not is_logged_in(request=request):
            form.errors.append("Delete not allowed without log in!")
        else:
            user = await UserRepo.delete_user(username=form.username)
            if user is True:
                form.__dict__.update(
                    msg=f"User with username: {form.username}, deleted succesfully."
                )
            if user is False:
                form.errors.append("Admin can not be removed !")
            else:
                form.errors.append("No such user!")
    return templates.TemplateResponse("user/user_operations.html", form.__dict__)
