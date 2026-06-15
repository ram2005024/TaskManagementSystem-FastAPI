from pydantic import BaseModel, EmailStr, field_validator


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
