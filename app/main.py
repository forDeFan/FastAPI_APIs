from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routers.route_login import login_router
from app.api.routers.route_root import root_router
from app.api.routers.route_user import user_router
from app.core.db.db import database, engine, metadata
from app.core.user_repo import UserRepo
from app.core.config import settings


def include_description():
    """
    Add basic description for docs endpoint.
    """
    description = """
        Training project.

        The API returns Jinja generated templates in response.
        Authentication and authorization layers implemented thru JWT token returned inside cookies.

        At first app run user can log into as admin (see users/get/all endpoint for log in details) to add more users and 
        try out restrictions in user modification in regard to privilege level (admin/ non-admin user).

        Passwords and login data shown intentionally to make log in/ user swap easier.
        """
    return description


def include_router(app: FastAPI) -> None:
    """
    To include specific API routes into FastAPI app.

    Args:
        app (FastAPI): instance where routers will be added.
    """
    app.include_router(router=user_router)
    app.include_router(router=root_router)
    app.include_router(router=login_router)


def configure_static(app: FastAPI) -> None:
    """
    Add static files folder as path to website.

    Args:
        app (FastAPI): instance
    """
    app.mount(
        "/static",
        StaticFiles(directory="app/web/static"),
        name="static",
    )


def start_application() -> FastAPI:
    """
    Start the app and include routers, static folder, created DB and instance of
    FastAPI itself.

    Returns:
        FastAPI: runnable instance
    """
    app = FastAPI(
        title="Fast API training", description=include_description()
    )
    include_router(app)
    configure_static(app)
    metadata.create_all(engine)
    return app


app = start_application()


@app.on_event("startup")
async def startup() -> None:
    """
    Connect to database at app startup and add default admin user to satabse
    if not exist.
    """
    if not database.is_connected:
        await database.connect()
    admin_exist = await UserRepo.get_by_username(username="admin")
    if admin_exist is None:
        await UserRepo.add_user(
            username="admin",
            email="admin@localhost",
            password=settings.ADMIN_PASSWORD,
            is_active=True,
            is_admin=True,
        )


@app.on_event("shutdown")
async def shutdown() -> None:
    """
    Close databse connection at app/ website closing.
    """
    if database.is_connected:
        await database.disconnect()
