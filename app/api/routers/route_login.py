from typing import Dict, Union

from app.api.forms.login_form import LoginForm
from app.core.config import settings
from app.core.security.jwt_handler import create_access_token
from app.core.user_repo import UserRepo
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/web/templates/")
login_router = APIRouter()


@login_router.get(
    "/login",
    tags=["LOGIN"],
    response_class=HTMLResponse,
    description="Login page",
)
def get_login(request: Request) -> Jinja2Templates:
    """
    \f Endpoint to for login page.

    Args:
        request (Request): to be used in templating.

    Returns:
        Jinja2Templates: rendered login page template
    """
    return templates.TemplateResponse(
        "login.html", {"request": request}
    )


@login_router.post(
    "/login",
    tags=["LOGIN"],
    response_class=HTMLResponse,
    description="Login process goes thru form.",
)
async def login(
    request: Request,
) -> Union[RedirectResponse, Jinja2Templates]:
    """
    \f Login functionality with usage of cookie placed access token.
    Only existing user can log in to the service.

    If errors - will be returned in the Jinja template to inform user in UI.

    Args:
        request (Request): to be used in templating.

    Returns:
        Union[RedirectResponse, Jinja2Templates]:
            If succesfull log in - redirect to /user endpoint
            If not succesfull reload login page.
    """
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        db_user = await UserRepo.get_by_username(username=form.username)
        if db_user is not None:
            if db_user.password == form.password:
                response = RedirectResponse(
                    url="/user", status_code=status.HTTP_302_FOUND
                )
                # Produce cookie with JWT calling token endpoint.
                await get_access_token(
                    response=response, form_data=form
                )
                return response
            else:
                form.errors.append("You provided wrong data.")
        else:
            form.errors.append("Incorrect email or password :(")
    return templates.TemplateResponse("login.html", form.__dict__)


@login_router.post(
    "/token",
    tags=["LOGIN"],
    description="Cookie with token generation.",
)
async def get_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, str]:
    """
    \f Endpoint for token to be issued at login in.
    Token placed in cookie with "Bearer" prefix.

    Args:
        response (Response): to be used in templating.
        form_data (OAuth2PasswordRequestForm, optional):
            username and password will be taken from login form.

    Returns:
        Dict[str, str]: cookie with token.
    """
    user = await UserRepo.get_by_username(username=form_data.username)
    access_token = create_access_token(data={"username": user.username})
    # HttpOnly - prevent JS from reading the cookie.
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=f"Bearer {access_token}",
        httponly=True,
    )
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}


@login_router.get(
    "/logout",
    tags=["LOGIN"],
    response_class=HTMLResponse,
    description="Destroy cookies after log out.",
)
def delete_cookie(response: Response) -> RedirectResponse:
    """
    \f Log out endpoint.
    Authorization cookie destroyed here.

    Args:
        response (Response): to be used in templating.

    Returns:
        RedirectResponse: redirection to login page.
    """
    response = RedirectResponse(
        url="/login", status_code=status.HTTP_302_FOUND
    )
    response.delete_cookie(settings.COOKIE_NAME)
    return response
