from typing import List, Union

from app.core.db.user_model import User
from asyncpg.exceptions import UniqueViolationError
from ormar.exceptions import NoMatch


class User_Repo:

    @classmethod
    async def get_all(cls) -> List[User]:
        users = await User.objects.all()
        return users

    @classmethod
    async def get_by_username(cls, username: str) -> Union[User, None]:
        try:
            user = await User.objects.filter(username__contains=username).get()
            return user
        except NoMatch:
            return None

    @classmethod
    async def get_by_email(cls, email: str) -> Union[User, None]:
        try:
            user = await User.objects.filter(email__contains=email).get()
            return user
        except NoMatch:
            return None

    @classmethod
    async def update_user_password(cls, username: str, password: str) -> Union[User, None]:
        try:
            await User.objects.filter(username__contains=username).update(password=password)
            updated_user = await User.objects.filter(username__contains=username).get()
            return updated_user
        except:
            return None

    @classmethod
    async def add_user(cls, username: str, email: str, password: str) -> Union[User, None]:
        try:
            user = await User.objects.create(username=username, email=email, password=(password))
            return user
        except UniqueViolationError:
            return None

    @classmethod
    async def delete_user(cls, username: str) -> bool:
        if await User.objects.filter(username__contains=username).delete() != None:
            return True
        else:
            return False

    @classmethod
    async def get_user_password(cls, username: str):
        user = await User.objects.filter(username__contains=username).get()
        return str(user.password)

    @classmethod
    async def get_user_email(cls, username: str):
        user = await User.objects.filter(username__contains=username).get()
        return str(user.email)
