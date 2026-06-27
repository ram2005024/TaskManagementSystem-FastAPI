# Get the user
from fastapi import Depends, Request
from fastapi.exceptions import HTTPException


def get_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=400, detail="Token could not be verified")
    if user["is_authenticated"] is False:
        raise HTTPException(status_code=401, detail="User is not verified.")
    return user


def role_check(accepted_roles: list[str]):
    def wrapper(user: dict = Depends(get_user)):
        if user["role"] not in accepted_roles:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user

    return wrapper
