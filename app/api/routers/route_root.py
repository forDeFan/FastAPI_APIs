from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/web/templates/")
root_router = APIRouter()


@root_router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> Jinja2Templates:
    return templates.TemplateResponse(name="home.html", context={"request": request})
