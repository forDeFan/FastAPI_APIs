from typing import List, Union

from app.core.db.user_model import User
from asyncpg import UniqueViolationError
from ormar.exceptions import NoMatch


class UserRepo:
    @classmethod
    async def get_all(cls) -> List[User]:
        users = await User.objects.all()
        return users

    @classmethod
    async def get_by_username(cls, username: str) -> Union[User, None]:
        user = await User.objects.filter(username=username).get_or_none()
        return user

    @classmethod
    async def get_by_email(cls, email: str) -> Union[User, None]:
        user = await User.objects.get_or_none(email=email)
        return user

    @classmethod
    async def update_user_password(
        cls, username: str, password: str
    ) -> Union[User, None]:
        try:
            await User.objects.filter(username__contains=username).update(
                password=password
            )
            updated_user = await User.objects.filter(username__contains=username).get()
            return updated_user
        except:
            return None

    @classmethod
    async def add_user(
        cls,
        username: str,
        email: str,
        password: str,
        is_active: bool = True,
        is_admin: bool = False,
    ) -> Union[User, None]:
        try:
            user = await User.objects.create(
                username=username,
                email=email,
                password=password,
                is_active=is_active,
                is_admin=is_admin,
            )
            return user
        except UniqueViolationError:
            return None

    @classmethod
    async def delete_user(cls, username: str) -> Union[bool, None]:
        try:
            user = await User.objects.filter(username__contains=username).first()
            if not user.is_admin:
                await user.delete()
                return True
            else:
                return False
        except NoMatch:
            return None

    @classmethod
    async def get_user_password(cls, username: str) -> str:
        user = await User.objects.filter(username__contains=username).first()
        return str(user.password)

    @classmethod
    async def get_user_email(cls, username: str) -> str:
        user = await User.objects.filter(username__contains=username).first()
        return str(user.email)
