from datetime import datetime, timedelta
from typing import Dict, Union

from app.core.config import settings
from app.core.db.user_model import User
from app.core.user_repo import UserRepo
from fastapi import Request
from jose import JWTError, jwt


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def decode_access_token(token: str) -> Union[User, None]:
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
    token = request.cookies.get(settings.COOKIE_NAME)
    user = await decode_access_token(token)
    return user
