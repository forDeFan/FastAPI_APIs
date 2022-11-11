from datetime import datetime, timedelta
from typing import Dict, Union

from app.core.config import settings
from app.core.db.user_model import User
from app.core.user_repo import UserRepo
from fastapi import Request
from jose import jwt, JWTError


def create_access_token(data: Dict) -> str:
    """
    Create JWT token.

    Args:
        data (Dict): {"username": provided username : str}

    Returns:
        str: encoded token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


async def decode_access_token(token: str):
    token = token.lstrip("Bearer").strip()
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError:
        payload = None

    return payload


async def get_current_user_from_cookie(
    request: Request,
) -> Union[User, None]:
    token = request.cookies.get(settings.COOKIE_NAME)
    try:
        payload = await decode_access_token(token=token)
        username = payload.get("username")
        user = await UserRepo.get_by_username(username=username)
    except:
        user = None

    return user
