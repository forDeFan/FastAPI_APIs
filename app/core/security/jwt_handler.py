from datetime import datetime, timedelta
from typing import Dict, Union

from app.core.config import settings
from app.core.db.user_model import User
from app.core.user_repo import UserRepo
from fastapi import Request
from jose import JWTError, jwt


def create_access_token(data: Dict) -> str:
    """
    Create JWT token.

    Args:
        data (Dict): {"username": provided username : str}

    Returns:
        str: encoded token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def decode_access_token(token: str) -> Union[User, None]:
    """
    Decode JWT token.

    Args:
        token (str): to be decoded

    Returns:
        Union[User, None]:
            User object if user exsist and decoding process was succesfull
            None if user do not exists or JWT decoding error
    """
    token = token.lstrip("Bearer").strip()
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("username")
    except JWTError:
        return None

    user = await UserRepo.get_by_username(username=username)
    return user


async def get_current_user_from_cookie(request: Request) -> Union[User, None]:
    """
    Extract authorization cookie from request, and decode token
    to get user from database.

    Args:
        request (Request): from which auyhorization cookie will be extracted

    Returns:
        Union[User, None]:
            User object taken from database if user exists
            None if such user do not exists in database or token decoding error
    """
    token = request.cookies.get(settings.COOKIE_NAME)
    user = await decode_access_token(token)
    return user
