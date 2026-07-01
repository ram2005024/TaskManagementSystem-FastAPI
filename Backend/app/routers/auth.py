from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.config import redis, settings
from app.core.oauth import oauth
from app.core.security import (
    create_access,
    create_refresh,
)
from app.database.db import get_db
from app.database.models.user import Profile, User
from app.dependencies.auth import get_user
from app.schemas.user import UserLogin, UserRead, UserRegister
from app.services.user import create_user, generate_username, verify_credentials

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
    print("Hello World")
    access_token = create_access(token_data)
    refresh_token = create_refresh(token_data)
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Login successful", "access": access_token},
    )
    # Set the refresh token in redis too
    redis.setex(f"token-{refresh_token}", settings.REFRESH_EXPIRY * 24 * 3600, "true")
    response.set_cookie(
        "refresh", refresh_token, httponly=True, secure=False, samesite="lax"
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
    # Verify the token
    try:
        payload = jwt.decode(
            old_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Create the new access token and refresh token and black list previous refresh token and store new refresh in redis

        data = {
            "id": payload["id"],
            "username": payload["username"],
            "is_authenticated": payload["is_authenticated"],
            "role": payload["role"],
        }
        new_access = create_access(data)

        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"access": new_access}
        )
        return response
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
    refresh = request.cookies.get("refresh")
    if refresh:
        redis.delete(f"token-{refresh}")

    response = JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Logged out"}
    )
    response.delete_cookie("refresh", httponly=True, secure=False, samesite="lax")
    return response


# When user logs in through the google
@authRouter.get("/google/login")
async def login_google(request: Request):
    redirect_url = settings.REDIRECT_URL_GOOGLE
    return await oauth.google.authorize_redirect(request, redirect_url)


@authRouter.get("/facebook/login")
async def facebook_login(request: Request):
    redirect_uri = settings.REDIRECT_URL_FACEBOOK
    return await oauth.facebook.authorize_redirect(request, redirect_uri)


@authRouter.get("/github/login")
async def login_github(request: Request):
    redirect_uri = settings.REDIRECT_URL_GITHUB
    return await oauth.github.authorize_redirect(request, redirect_uri)


@authRouter.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token["userinfo"]
        if user:
            existing_user = (
                db.query(User)
                .filter(User.oauth_id == str(user.get("sub")))
                .one_or_none()
            )
            if existing_user:
                final_user = existing_user
            else:
                if user.get("email"):
                    existing_user = (
                        db.query(User)
                        .filter(User.email == user.get("email"))
                        .one_or_none()
                    )
                    if existing_user:
                        existing_user.oauth_id = user.get("sub")
                        existing_user.oauth_provider = "google"
                        db.commit()
                        final_user = existing_user
                else:
                    user_name = generate_username(user.get("name"), db)
                    new_user = User(
                        email=user.get("email"),
                        is_authenticated=True,
                        oauth_provider="google",
                        username=user_name,
                        oauth_id=user.get("sub"),
                    )
                    db.add(new_user)
                    db.flush()
                    # Create profile
                    profile = Profile(
                        user_id=new_user.id,
                        user_image=user.get("picture"),
                        full_name=user.get("name"),
                    )
                    db.add(profile)
                    db.commit()
                    final_user = new_user
            token_data = {
                "id": str(final_user.id),
                "username": final_user.username,
                "is_authenticated": final_user.is_authenticated,
                "role": final_user.role,
            }
            refresh = create_refresh(token_data)
            access = create_access(token_data)
            response = JSONResponse(
                status_code=201,
                content={"access": access, "message": "Login successful"},
            )
            redis.setex(f"token-{refresh}", settings.REFRESH_EXPIRY * 24 * 3600, "true")
            response.set_cookie(
                "refresh", refresh, httponly=True, secure=False, samesite="none"
            )
            return response

    except Exception as e:
        print(e)
        raise


@authRouter.get("/facebook/callback")
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.facebook.authorize_access_token(request)
        resp = await oauth.facebook.get(
            "me/?fields=name,email,birthday,picture", token=token
        )
        user = resp.json()
        if user:
            existing_user = (
                db.query(User)
                .filter(User.oauth_id == str(user.get("id")))
                .one_or_none()
            )
            if existing_user:
                final_user = existing_user
            else:
                if user.get("email"):
                    existing_user = (
                        db.query(User)
                        .filter(User.email == user.get("email"))
                        .one_or_none()
                    )
                    if existing_user:
                        existing_user.oauth_id = user.get("id")
                        existing_user.oauth_provider = "facebook"
                        db.commit()
                        final_user = existing_user
                else:
                    user_name = generate_username(user.get("name"), db)
                    new_user = User(
                        email=user.get("email"),
                        username=user_name,
                        is_authenticated=True,
                        oauth_id=user.get("id"),
                        oauth_provider="facebook",
                    )
                    db.add(new_user)
                    db.flush()
                    # Create profile
                    profile = Profile(
                        user_id=new_user.id,
                        user_image=user.get("picture").get("data").get("url"),
                        full_name=user.get("name"),
                    )
                    db.add(profile)
                    db.commit()
                    final_user = new_user
            token_data = {
                "id": str(final_user.id),
                "username": final_user.username,
                "is_authenticated": final_user.is_authenticated,
                "role": final_user.role,
            }
            refresh = create_refresh(token_data)
            access = create_access(token_data)
            response = JSONResponse(
                status_code=201,
                content={"access": access, "message": "Login successful"},
            )
            redis.setex(f"token-{refresh}", settings.REFRESH_EXPIRY * 24 * 3600, "true")
            response.set_cookie(
                "refresh", refresh, httponly=True, secure=False, samesite="none"
            )
            return response

    except Exception as e:
        print(e)
        raise


# Github callback
@authRouter.get("/github/callback")
async def github_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.github.authorize_access_token(request)
        resp = await oauth.github.get("user", token=token)
        user = resp.json()
        if user:
            existing_user = (
                db.query(User)
                .filter(User.oauth_id == str(user.get("id")))
                .one_or_none()
            )
            if existing_user:
                final_user = existing_user
            else:
                if user.get("email"):
                    existing_user = (
                        db.query(User)
                        .filter(User.email == user.get("email"))
                        .one_or_none()
                    )
                    if existing_user:
                        existing_user.oauth_id = user.get("id")
                        existing_user.oauth_provider = "github"
                        db.commit()
                        final_user = existing_user
                    else:
                        user_name = generate_username(user.get("name"), db)
                        new_user = User(
                            email=user.get("email"),
                            username=user_name,
                            is_authenticated=True,
                            oauth_id=user.get("id"),
                            oauth_provider="github",
                        )
                        db.add(new_user)
                        db.flush()
                        # Create profile
                        profile = Profile(
                            user_id=new_user.id,
                            user_image=user.get("avatar_url"),
                            full_name=user.get("name"),
                        )
                        db.add(profile)
                        db.commit()
                        final_user = new_user
            token_data = {
                "id": str(final_user.id),
                "username": final_user.username,
                "is_authenticated": final_user.is_authenticated,
                "role": final_user.role,
            }
            refresh = create_refresh(token_data)
            access = create_access(token_data)
            response = JSONResponse(
                status_code=201,
                content={"access": access, "message": "Login successful"},
            )
            redis.setex(f"token-{refresh}", settings.REFRESH_EXPIRY * 24 * 3600, "true")
            response.set_cookie(
                "refresh", refresh, httponly=True, secure=False, samesite="none"
            )
            return response

    except Exception as e:
        print(e)
        raise


@authRouter.get("/me", response_model=UserRead)
def get_me(request: Request, user=Depends(get_user), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user["user_id"]).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
