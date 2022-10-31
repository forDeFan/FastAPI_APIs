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


@login_router.get("/login")
def get_login(request: Request) -> Jinja2Templates:
    return templates.TemplateResponse("login.html", {"request": request})


@login_router.post("/login")
async def login(request: Request) -> Union[RedirectResponse, Jinja2Templates]:
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        db_user = await UserRepo.get_by_username(username=form.username)
        if db_user is not None:
            if db_user.password == form.password:
                form.__dict__.update(
                    msg=f"{db_user.username.capitalize()}"
                )
                response = templates.TemplateResponse("login.html", form.__dict__)
                # Produce cookie with JWT calling token endpoint.
                await get_access_token(response=response, form_data=form)
                return response
            else:
                form.errors.append("You provided wrong data.")
        else:
            form.errors.append("Incorrect email or password :(")
    return templates.TemplateResponse("login.html", form.__dict__)


@login_router.post("/token")
async def get_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, str]:
    user = await UserRepo.get_by_username(username=form_data.username)
    access_token = create_access_token(data={"username": user.username})
    # HttpOnly - prevent JS from reading the cookie.
    response.set_cookie(
        key=settings.COOKIE_NAME, value=f"Bearer {access_token}", httponly=True
    )
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}


@login_router.get("/logout", response_class=HTMLResponse)
def delete_cookie(response: Response) -> RedirectResponse:
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(settings.COOKIE_NAME)
    return response
