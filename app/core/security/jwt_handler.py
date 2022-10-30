from datetime import datetime, timedelta
from typing import Dict, Union

from app.core.config import settings
from app.core.db.user_model import User
from app.core.security.auth import OAuth2PasswordBearerWithCookie
from app.core.user_repo import UserRepo
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/token")


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def decode_access_token(token: str) -> Union[User, None]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await UserRepo.get_by_username(username=username)
    return user


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
) -> Union[User, None]:
    user = decode_access_token(token)
    return user


def get_current_user_from_cookie(request: Request) -> Union[User, None]:
    token = request.cookies.get(settings.COOKIE_NAME)
    user = decode_access_token(token)
    return user
