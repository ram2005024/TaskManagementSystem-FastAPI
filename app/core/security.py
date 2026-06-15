from pwdlib import PasswordHash
from jose import jwt
from jose import JWTError, ExpiredSignatureError
from app.core.config import settings
from datetime import datetime, timedelta
from app.core.config import redis
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi import Request
from app.core.config import settings

hashed_pwd = PasswordHash.recommended()


def hashPwd(pwd: str):
    return hashed_pwd.hash(pwd)


def verifyPwd(plain: str, hashed: str):
    return hashed_pwd.verify(plain, hashed)


# Create access token
def create_access(data: dict):
    copied = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_EXPIRY)
    copied.update({"exp": exp, "type": "access"})
    return jwt.encode(copied, settings.SECRET_KEY, settings.ALGORITHM)


# Create refresh token
def create_refresh(data: dict):
    copied = data.copy()
    exp = datetime.utcnow() + timedelta(days=settings.REFRESH_EXPIRY)
    copied.update({"exp": exp, "type": "refresh"})
    return jwt.encode(copied, settings.SECRET_KEY, settings.ALGORITHM)


# Blacklist the token
def blacklist_token(token: str, exp: int) -> bool:
    return redis.setex(f"blacklist-{token}", exp, "true")


# Check the blacklist token
def isblacklisted(token: str):
    return redis.exists(f"blacklist-{token}")


# Blacklist middleware
async def blacklist_middleware(request: Request, call_next):
    pass_path = ["/auth/login", "/auth/register", "/auth/refresh", "/auth/logout"]
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
    request.state.user_id = payload["id"]
    return await call_next(request)
