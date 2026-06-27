# Blacklist middleware
from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from app.core.config import settings
from app.core.security import isblacklisted


async def blacklist_middleware(request: Request, call_next):
    pass_path = [
        "/auth/login",
        "/auth/register",
        "/auth/refresh",
        "/auth/logout",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/auth/login/google",
        "auth/google/callback",
    ]
    if request.method == "OPTIONS":
        return await call_next(request)
    if request.url.path in pass_path:
        return await call_next(request)
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Header is missing"},
        )
    token = auth_header.split(" ")[1]
    # Verify if the token is blacklisted or not
    if isblacklisted(token):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token revoked"},
        )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except ExpiredSignatureError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Expired token"},
        )
    except JWTError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid token"},
        )

    request.state.user = {
        "user_id": payload["id"],
        "username": payload["username"],
        "is_authenticated": payload["is_authenticated"],
        "role": payload["role"],
    }
    return await call_next(request)
