from fastapi import FastAPI
from app.core.db import User, database

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/user/all")
async def get_all_things():
    return await User.objects.all()


@app.post("/user/{username}&{email}&{password}")
async def add_thing(username: str, email: str, password: str):
    await User.objects.create(username=username, email=email, password=password)
    return {
        "status": f"Success. User with username: {username} and email: {email} created!"
    }


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
