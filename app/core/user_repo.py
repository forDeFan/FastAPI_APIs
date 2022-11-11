from typing import List, Union

from app.core.model.user_model import UserModel
from asyncpg import UniqueViolationError
from ormar.exceptions import NoMatch


class UserRepo:
    """
    Main user repository to use ORM in it.
    """

    @classmethod
    async def get_all(cls) -> List[UserModel]:
        """
        Get all users from database.

        Returns:
            List[User]: all users from databse
        """
        users = await UserModel.objects.all()
        return users

    @classmethod
    async def get_by_username(
        cls, username: str
    ) -> Union[UserModel, None]:
        """
        Get user from database by username.

        Args:
            username (str): username to get user by

        Returns:
            Union[User, None]:
                if user exist return User object
                if not return None
        """
        user = await UserModel.objects.filter(
            username=username
        ).get_or_none()
        return user

    @classmethod
    async def update_user_password(
        cls, username: str, new_password: str
    ) -> Union[UserModel, None]:
        """
        Update user password if user exists in database.

        Args:
            username (str): to get user from database
            new_password (str): new pasword to be set

        Returns:
            Union[User, None]:
                if user exists return User object with updated password
                if not exists return None
        """
        try:
            await UserModel.objects.filter(
                username__contains=username
            ).update(password=new_password)
            updated_user = await UserModel.objects.filter(
                username__contains=username
            ).get()
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
    ) -> Union[UserModel, None]:
        """
        Add new user to database.

        Args:
            username (str): unique new user username
            email (str): unique new user email
            password (str): password of min lenght of 5 chars
            is_active (bool, optional): if new user is active (default True)
            is_admin (bool, optional): if new user is admin (default False)

        Returns:
            Union[User, None]:
                new User object if username and password is unique and ok
                None if user with such username or email exist already
        """
        try:
            # Remove single quotes from .env file in admin pass case.
            password = password.replace("'", "")
            user = await UserModel.objects.create(
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
        """
        Delete user from database if user exists.

        Args:
            username (str): to search by in database

        Returns:
            Union[bool, None]:
                return User object if user existed in database and was deleted
                return None if user was not found in database by username and wasn't deleted
        """
        try:
            user = await UserModel.objects.filter(
                username__contains=username
            ).first()
            if not user.is_admin:
                await user.delete()
                return True
            else:
                return False
        except NoMatch:
            return None
