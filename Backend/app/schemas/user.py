from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator

if TYPE_CHECKING:
    from app.schemas.company import CompanyReadSingle
    from app.schemas.join_requests import ReadMultipleJoinRequest
    from app.schemas.profile import ProfileBasic
    from app.schemas.project import ProjectReadSingle
    from app.schemas.task import TaskReadSingle


# User login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# User register Schema
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    @field_validator("password")
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password length must be at least 8 character")
        return v


# Class user read single----
class UserRead(BaseModel):
    id: UUID
    username: str
    email: str
    user_requests: list["ReadMultipleJoinRequest"] = []
    is_authenticated: bool
    role: str
    projects: list["ProjectReadSingle"] = []
    tasks: list["TaskReadSingle"] = []
    profile: "ProfileBasic"
    manager_company: "CompanyReadSingle |None" = None
    company: "CompanyReadSingle|None" = None

    class Config:
        from_attributes: True


# User update
class UserUpdate(BaseModel):
    id: UUID
    is_authenticated: bool | None = None
    role: str | None = None
    isActive: bool | None = None

    class Config:
        from_attributes = True


# Class User read basic
# Class user read single----
class UserReadBasic(BaseModel):
    id: UUID
    username: str
    email: str
    is_authenticated: bool
    role: str
    profile: "ProfileBasic"

    class Config:
        from_attributes: True
