import time

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import redis, settings
from app.core.security import (
    blacklist_token,
    create_access,
    create_refresh,
    isblacklisted,
)
from app.database.db import get_db
from app.schemas.user import UserLogin, UserRegister
from app.services.user import create_user, verify_credentials

authRouter = APIRouter(prefix="/auth", tags=["auth_endpoints"])


@authRouter.post("/register")
def register(
    email: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    password: str = Form(...),
    user_image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    userdata = UserRegister(
        email=email, password=password, first_name=first_name, last_name=last_name
    )
    user, error = create_user(userdata, user_image, db)
    if error or not user:
        raise HTTPException(status_code=400, detail=error or "Failed to create user")

    return {"message": "User created successfully", "username": user.username}


@authRouter.post("/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db),
):
    user, error = verify_credentials(data, db)
    if error or not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": error}
        )
    # Generate the access and refresh token
    token_data = {
        "id": str(user.id),
        "username": user.username,
        "is_authenticated": user.is_authenticated,
        "role": user.role,
    }
    access_token = create_access(token_data)
    refresh_token = create_refresh(token_data)
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Login successful", "access": access_token},
    )
    # Set the refresh token in redis too
    redis.setex(f"token-{refresh_token}", settings.REFRESH_EXPIRY * 24 * 3600, "true")
    response.set_cookie(
        "refresh", refresh_token, httponly=True, secure=False, samesite="none"
    )

    return response


@authRouter.post("/refresh")
def refresh(request: Request):
    old_token = request.cookies.get("refresh")
    if not old_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token doesn't exist"},
        )
    # Check if refresh token exist in redis or not
    if not redis.exists(f"token-{old_token}"):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token revoked"},
        )
    # Check if token is blacklisted or not
    if isblacklisted(old_token):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token revoked"},
        )
    # Verify the token
    try:
        payload = jwt.decode(
            old_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Create the new access token and refresh token and black list previous refresh token and store new refresh in redis

        data = {"id": payload["id"], "username": payload["username"]}
        current = int(time.time())
        ttl = payload["exp"] - current
        if ttl > 0:
            blacklist_token(old_token, ttl)
        new_access = create_access(data)
        new_refresh = create_refresh(data)
        redis.delete(f"token-{old_token}")
        redis.setex(f"token-{new_refresh}", settings.REFRESH_EXPIRY * 24 * 3600, "true")
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"access": new_access}
        )
        response.set_cookie(
            "refresh", new_refresh, httponly=True, secure=False, samesite="none"
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


# Logout endpoint
@authRouter.post("/logout")
def logout(request: Request):
    header = request.headers.get("Authorization")
    if header:
        access = header.split(" ")[1]
        refresh = request.cookies.get("refresh")
        try:
            payload = jwt.decode(
                access, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            ttl = payload["exp"] - int(time.time())
            if ttl > 0:
                blacklist_token(access, ttl)
        except ExpiredSignatureError:
            pass
        except JWTError:
            pass
    if refresh:
        try:
            payload = jwt.decode(
                refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            ttl = int(time.time()) - payload["exp"]
            if ttl > 0:
                blacklist_token(refresh, ttl)
            redis.delete(f"token-{refresh}")
        except ExpiredSignatureError:
            pass
        except JWTError:
            pass
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Logged out"}
    )
    response.delete_cookie("refresh")
    return response
