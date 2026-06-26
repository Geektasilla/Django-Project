from datetime import datetime, timezone
from typing import Any
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def get_token_expiry_datetime(token: AccessToken | RefreshToken) -> datetime:
    return datetime.fromtimestamp(int(token['exp']), tz=timezone.utc)


def build_cookie_kwargs(expires: datetime) -> dict[str, Any]:
    return {
        "httponly": True,
        "secure": False,
        "samesite": "Lax",
        "path": "/",
        "expires": expires
    }


def set_access_token(response: HttpResponse, access_token: str) -> None:
    token = AccessToken(access_token)
    token_exp = get_token_expiry_datetime(token)
    response.set_cookie(
        key="access_token",
        value=access_token,
        **build_cookie_kwargs(token_exp)
    )


def set_refresh_token(response: HttpResponse, refresh_token: str):
    token = RefreshToken(refresh_token)
    token_exp = get_token_expiry_datetime(token)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        **build_cookie_kwargs(token_exp)
    )


def set_jwt_cookies(response: HttpResponse, user) -> None:
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    set_access_token(response, str(access_token))
    set_refresh_token(response, str(refresh_token))


def clear_cookies(response: HttpResponse) -> None:
    response.delete_cookie(key="refresh_token", path="/")
    response.delete_cookie(key="access_token", path="/")
