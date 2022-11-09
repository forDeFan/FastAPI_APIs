from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.forms.add_user_form import AddUserForm
from app.api.forms.check_user_form import CheckUserForm
from app.api.forms.update_user_pass_form import UpdateUserPassForm
from app.core.config import settings
from app.core.security.auth import OAuth2PasswordBearerWithCookie
from app.core.security.jwt_handler import get_current_user_from_cookie
from app.core.user_repo import UserRepo

templates = Jinja2Templates(directory="app/web/templates/")
user_router = APIRouter()
# API endpoint to get new token from.
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/token")


def is_logged_in(request: Request) -> bool:
    """
    Helper function to check if user is logged in.

    Args:
        request (Request): to be used in templating.

    Returns:
        bool:
            True if logged in
            False if not logged in
    """
    if not settings.COOKIE_NAME in request.cookies:
        return False
    return True


@user_router.get("/user", response_class=HTMLResponse)
async def get_user_operations(request: Request) -> Jinja2Templates:
    """
    \f Endpoint to get user operations page.

    Args:
        request (Request): to be used in templating.

    Returns:
        Jinja2Templates: user operations page.
    """
    return templates.TemplateResponse(
        name="user/user_operations.html", context={"request": request}
    )


@user_router.get("/user/get/all", response_class=HTMLResponse)
async def get_all_users(request: Request) -> Jinja2Templates:
    """
    \f Endpoint to get all users from database page.

    Args:
        request (Request): to be used in templating.

    Returns:
        Jinja2Templates: all users in database page.
    """
    users = await UserRepo.get_all()
    return templates.TemplateResponse(
        name="user/user_all.html",
        context={"request": request, "users": users},
    )


@user_router.post("/user/get", response_class=HTMLResponse)
async def get_user(request: Request) -> Jinja2Templates:
    """
    \f Endpoint to get specific user data.
    Non logged in user can browse other users data.

    If errors - will be returned in the Jinja template to inform user in UI.

    Args:
        request (Request): to be used in templating.

    Returns:
        Jinja2Templates: specific user data page.
    """
    form = CheckUserForm(request=request)
    await form.load_data()
    if await form.is_valid():
        user = await UserRepo.get_by_username(username=form.username)
        if user is not None:
            response = templates.TemplateResponse(
                name="user/user_info.html",
                context={"request": request, "user": user},
            )
            return response
        else:
            form.errors.append("No such user !")
    return templates.TemplateResponse(
        "user/user_operations.html", form.__dict__
    )


@user_router.post("/user/update", response_class=HTMLResponse)
async def update_user_password(request: Request) -> Jinja2Templates:
    """
    \f Endpoint to update secific user password.
    Only looged in user can change his own password.
    Logged in user can't change password of other user (authorization thru cookie JWT).
    Admin can change password for all users.

    If errors - will be returned in the Jinja template to inform user in UI.

    Args:
        request (Request): to be used in templating.

    Returns:
        Jinja2Templates: user opareations page.
    """
    form = UpdateUserPassForm(request=request)
    await form.load_data()
    if await form.is_valid():
        if not is_logged_in(request=request):
            form.errors.append("Update not allowed without log in!")
        else:
            db_user = await UserRepo.get_by_username(
                username=form.username
            )
            cookie_user = await get_current_user_from_cookie(
                request=request
            )
            if db_user is not None:
                if (
                    cookie_user.username == db_user.username
                    or cookie_user.is_admin
                ):
                    if db_user.password == form.old_password:
                        await UserRepo.update_user_password(
                            username=form.username,
                            new_password=form.new_password,
                        )
                        form.__dict__.update(
                            msg=f"Password for user: {form.username}, changed successfully."
                        )
                    else:
                        form.errors.append(
                            "Wrong old password provided!"
                        )
                else:
                    form.errors.append(
                        "Only user himself or Admin can change password!"
                    )
            else:
                form.errors.append("No such user!")
    return templates.TemplateResponse(
        "user/user_operations.html", form.__dict__
    )


@user_router.post(
    "/user/add",
    dependencies=[Depends(oauth2_scheme)],
    response_class=HTMLResponse,
)
async def add_user(request: Request) -> Jinja2Templates:
    """
    \f Endpoint to add new user.
    Only admin can add new users (authorization thru cookie JWT).

    If errors - will be returned in the Jinja template to inform user in UI.

    Args:
        request (Request): to be used in templating.

    Returns:
        Jinja2Templates: user opareations page.
    """
    form = AddUserForm(request=request)
    await form.load_data()
    if await form.is_valid():
        if not is_logged_in(request=request):
            form.errors.append("Adding not allowed without log in!")
        else:
            cookie_user = await get_current_user_from_cookie(
                request=request
            )
            if cookie_user.is_admin:
                new_user = await UserRepo.add_user(
                    username=form.username,
                    email=form.email,
                    password=form.password,
                )
                if new_user is not None:
                    form.__dict__.update(
                        msg=f"User with username: {form.username}, added succesfully."
                    )
                else:
                    form.errors.append(
                        "Not added - such user already exists!"
                    )
            else:
                form.errors.append(
                    "Not added - only admin can add new users."
                )
    return templates.TemplateResponse(
        "user/user_operations.html", form.__dict__
    )


@user_router.post(
    "/user/delete",
    dependencies=[Depends(oauth2_scheme)],
    response_class=HTMLResponse,
)
async def delete_user(request: Request) -> Jinja2Templates:
    """
    \f Endpoint to delete specific user.
    Only admin can delete users (authorization thru cookie JWT).
    Admin can't be removed at all.

    If errors - will be returned in the Jinja template to inform user in UI.

    Args:
        request (Request): to be used in templating.

    Returns:
        Jinja2Templates: user opareations page.
    """
    form = CheckUserForm(request=request)
    await form.load_data()
    if await form.is_valid():
        if not is_logged_in(request=request):
            form.errors.append("Delete not allowed without log in!")
        else:
            cookie_user = await get_current_user_from_cookie(
                request=request
            )
            if cookie_user.is_admin:
                user = await UserRepo.delete_user(
                    username=form.username
                )
                if user is True:
                    form.__dict__.update(
                        msg=f"User with username: {form.username}, deleted succesfully."
                    )
                if user is False:
                    form.errors.append("Admin can not be removed !")
                else:
                    form.errors.append("No such user!")
            else:
                form.errors.append("Only Admin can delete users!")
    return templates.TemplateResponse(
        "user/user_operations.html", form.__dict__
    )
