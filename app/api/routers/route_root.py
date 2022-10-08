from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/web/templates/")
root_router = APIRouter()


@root_router.get("/")
async def home(request: Request) -> Jinja2Templates:
    return templates.TemplateResponse(name="home.html", context={"request": request})
