from typing import Dict, Optional

from app.core.config import settings
from fastapi.openapi.models import OAuthFlows
from fastapi.requests import Request
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param


class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    Oauth2 implementation with usage of cookie as authorization token transmit layer,
    as HTML in routes is returned - headers will not be included in the response.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ) -> None:
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Implementation to search for authorization cookie in request.

        Args:
            request (Request): to search cookies into.

        Returns:
            Optional[str]:
                return param when authorized - cookie with "Bearer" found in request
                return None if authorization cookie not found in request cookies
        """
        authorization: str = request.cookies.get(settings.COOKIE_NAME)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            return None
        return param
