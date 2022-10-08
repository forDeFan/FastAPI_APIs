from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routers.route_user import user_router
from app.api.routers.route_root import root_router
from app.core.db.db import database, engine, metadata


def include_router(app: FastAPI):
    app.include_router(router=user_router)
    app.include_router(router=root_router)


def configure_static(app: FastAPI):
    app.mount("/static",
              StaticFiles(directory="app/web/static"), name="static")


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


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
