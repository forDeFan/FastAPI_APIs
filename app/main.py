from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routers.route_login import login_router
from app.api.routers.route_root import root_router
from app.api.routers.route_user import user_router
from app.core.db.db import database, engine, metadata
from app.core.user_repo import UserRepo
from app.core.config import settings


def include_router(app: FastAPI):
    app.include_router(router=user_router)
    app.include_router(router=root_router)
    app.include_router(router=login_router)


def configure_static(app: FastAPI):
    app.mount("/static", StaticFiles(directory="app/web/static"), name="static")


def start_application() -> FastAPI:
    app = FastAPI(title="Fast API training")
    include_router(app)
    configure_static(app)
    metadata.create_all(engine)
    return app


app = start_application()


@app.on_event("startup")
async def startup():
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
async def shutdown():
    if database.is_connected:
        await database.disconnect()
