from datetime import datetime, timedelta

from jose import jwt
from pwdlib import PasswordHash

from app.core.config import redis, settings

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
