from datetime import datetime, timedelta
from typing import Dict, Union

from fastapi import Request
from jose import JWTError, jwt

from app.core.config import settings
from app.core.model.user_model import UserModel
from app.core.user_repo import UserRepo
from app.core.jwt_repo import JwtRepo


def create_access_token(data: Dict) -> str:
    """
    Create JWT token.
    Expiration time returned in token as timestamp.

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


async def decode_access_token(token: str) -> Union[Dict, None]:
    """
    Decode JWT extracted from authorization cookie.
    Validate JWT expiry time.

    Args:
        token (str): to be decoded.

    Returns:
        Union[Dict, None]:
            return Dict of username and validation timestamp
            return None if JWT decoding error or JWT expired
    """
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
) -> Union[UserModel, None]:
    """
    Get user from authorization cookie.

    Args:
        request (Request): to be used in templating.

    Returns:
        Union[User, None]:
            return User if authorization cookie present
            return None if authorization cookie not present
                        or no such user in databes
    """
    token = request.cookies.get(settings.COOKIE_NAME)
    try:
        payload = await decode_access_token(token=token)
        username = payload.get("username")
        user = await UserRepo.get_by_username(username=username)
    except:
        user = None

    return user


async def check_if_token_blacklisted(request: Request) -> bool:
    """
    Check against database if token wasn't used before.

    Args:
        request (Request): used in templating.

    Returns:
        bool:
            True - if token was used before and is blacklisted
            False - if token is not blacklisted
    """
    try:
        cookie = request.cookies.get(settings.COOKIE_NAME)
        token = cookie.lstrip("Bearer").strip()
        blacklisted_token = await JwtRepo.get_from_database(token=token)
    except AttributeError:
        blacklisted_token = None

    if blacklisted_token is not None:
        return True
    return False


async def blacklist_token(request: Request) -> None:
    """
    Add token to blacklist in database to not be used again.

    Args:
        request (Request): used in templating.
    """
    cookie = request.cookies.get(settings.COOKIE_NAME)
    token = cookie.lstrip("Bearer").strip()
    await JwtRepo.add_to_database(token=token)
