from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/web/templates/")
root_router = APIRouter()


@root_router.get(
    "/",
    tags=["GENERAL"],
    response_class=HTMLResponse,
    description="Homepage",
)
async def home(request: Request) -> Jinja2Templates:
    """
    \f Homepage endpoint.

    Args:
        request (Request): to be used in templating.

    Returns:
        Jinja2Templates: rendered homepage template.
    """
    return templates.TemplateResponse(
        name="home.html", context={"request": request}
    )
