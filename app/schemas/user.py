from pydantic import BaseModel, EmailStr, field_validator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.project import ProjectReadSingle
    from app.schemas.task import TaskReadSingle
    from app.schemas.company import CompanyReadSingle
    from app.schemas.profile import ProfileRead
    from app.schemas.join_requests import ReadMultipleJoinRequest




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
    id:str
    username:str
    email:str
    user_requests:list["ReadMultipleJoinRequest"]=[]
    is_authenticated:bool
    role:str
    projects:list["ProjectReadSingle"]=[]
    tasks:list["TaskReadSingle"]=[]
    profile:"ProfileRead"
    manager_company:"CompanyReadSingle |None"=None
    company:"CompanyReadSingle"
    
    class Config:
        form_attributes:True
        
# User update
class UserUpdate(BaseModel):
    id:str
    is_authenticated:bool|None=None
    role:str|None=None
    isActive:bool|None=None
    
    class Config:
        form_attributes=True
