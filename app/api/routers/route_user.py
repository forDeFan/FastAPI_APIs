from typing import Optional, Union

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.forms.add_user_form import AddUserForm
from app.api.forms.check_user_form import CheckUserForm
from app.api.forms.update_user_pass_form import UpdateUserPassForm
from app.core.config import settings
from app.core.db.user_model import User
from app.core.security.auth import OAuth2PasswordBearerWithCookie
from app.core.security.jwt_handler import get_current_user_from_cookie
from app.core.user_repo import UserRepo

templates = Jinja2Templates(directory="app/web/templates/")
user_router = APIRouter()
# API endpoint to get new token from.
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/token")


async def get_cookie_user(request: Request) -> Union[User, None]:
    """
    Helper method to get user from session cookie.
    If no cookie user will be returned as None.

    Args:
        request (Request): to be used in templating.

    Returns:
        Union[User, None]:
            If authorization cookie present in request - return User
            If no authorization cookie present in request - return None
    """
    return await get_current_user_from_cookie(request=request)


@user_router.get(
    "/user",
    tags=["USER"],
    response_class=HTMLResponse,
    description="Get all possible user operations page.",
)
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


@user_router.get(
    "/user/get/all",
    tags=["USER"],
    response_class=HTMLResponse,
    description="List all users from database. No login needed.",
)
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


@user_router.post(
    "/user/get/{username}",
    tags=["USER"],
    response_class=HTMLResponse,
    description="Get specific user info. No login in needed.",
)
async def get_user(
    request: Request,
) -> Jinja2Templates:
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


@user_router.post(
    "/user/update",
    tags=["USER"],
    response_class=HTMLResponse,
    description="Update user password. Only admin or logged in user can change his own password. Login needed.",
)
async def update_user_password(request: Request) -> Jinja2Templates:
    """
    \f Endpoint to update secific user password.
    
    Only logged in user can change his own password.
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
        cookie_user = await get_cookie_user(request=request)
        if cookie_user is None:
            form.errors.append("Update not allowed without log in!")
        else:
            db_user = await UserRepo.get_by_username(
                username=form.username
            )
            # To check if session expired while in opeations.
            if cookie_user is not None:
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
            else:
                form.errors.append(
                    "Your session expired - please log in again."
                )
                response = templates.TemplateResponse(
                    "user/user_operations.html", form.__dict__
                )
                response.delete_cookie(settings.COOKIE_NAME)
                # For cookies to be deleted.
                return response

    return templates.TemplateResponse(
        "user/user_operations.html", form.__dict__
    )


@user_router.post(
    "/user/add",
    dependencies=[Depends(oauth2_scheme)],
    tags=["USER"],
    response_class=HTMLResponse,
    description="Add new user - admin permitted only. Log in needed.",
)
async def add_user(request: Request) -> Jinja2Templates:
    """
    \f Endpoint to add new user.
    Authorization and authentication in use (thru cookie JWT).

    Only admin can add new users.

    If errors - will be returned in the Jinja template to inform user in UI.

    Args:
        request (Request): to be used in templating.

    Returns:
        Jinja2Templates: user opareations page.
    """
    form = AddUserForm(request=request)
    await form.load_data()
    if await form.is_valid():
        cookie_user = await get_cookie_user(request=request)
        if cookie_user is None:
            form.errors.append("Adding not allowed without log in!")
        else:
            # To check if session expired while in opeations.
            if cookie_user is not None:
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
            else:
                form.errors.append(
                    "Your session expired - please log in again."
                )
                response = templates.TemplateResponse(
                    "user/user_operations.html", form.__dict__
                )
                response.delete_cookie(settings.COOKIE_NAME)
                # For cookies to be deleted.
                return response

    return templates.TemplateResponse(
        "user/user_operations.html", form.__dict__
    )


@user_router.post(
    "/user/delete",
    dependencies=[Depends(oauth2_scheme)],
    tags=["USER"],
    response_class=HTMLResponse,
    description="Delete user - admin permitted only. Log in needed.",
)
async def delete_user(request: Request) -> Jinja2Templates:
    """
    \f Endpoint to delete specific user.
    Authorization and authentication in use (thru cookie JWT).

    Only admin can delete users, admin can't be removed at all.

    If errors - will be returned in the Jinja template to inform user in UI.

    Args:
        request (Request): to be used in templating.

    Returns:
        Jinja2Templates: user opareations page.
    """
    form = CheckUserForm(request=request)
    await form.load_data()
    if await form.is_valid():
        cookie_user = await get_cookie_user(request=request)
        if cookie_user is None:
            form.errors.append("Delete not allowed without log in!")
        else:
            # To check if session expired while in opeations.
            if cookie_user is not None:
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
                    if user is None:
                        form.errors.append("No such user!")
                else:
                    form.errors.append("Only Admin can delete users!")
            else:
                form.errors.append(
                    "Your session expired - please log in again."
                )
                response = templates.TemplateResponse(
                    "user/user_operations.html", form.__dict__
                )
                response.delete_cookie(settings.COOKIE_NAME)
                # For cookies to be deleted.
                return response

    return templates.TemplateResponse(
        "user/user_operations.html", form.__dict__
    )
