from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from app.schemas.join_requests import ReadMultipleJoinRequest
    from app.schemas.project import ProjectReadMultiple
    from app.schemas.user import UserReadBasic


class CompanyBase(BaseModel):
    company_name: str
    company_description: str | None = None
    company_banner: str | None = None
    company_type: str | None = None

    @field_validator("company_name")
    def check_company_name(cls, v):
        if len(v) < 5:
            raise ValueError("Company name should have atleast 5 characters")
        return v


class CompanyBasic(CompanyBase):
    logo: str | None = None


# Create Company
class CompanyCreate(CompanyBase):
    pass


# Read  company
class CompanyReadSingle(CompanyBase):
    id: UUID
    logo: str | None = None
    issue_date: datetime
    updated_at: datetime
    is_active: bool
    projects: list["ProjectReadMultiple"] = []
    manager: "UserReadBasic |None" = None
    enrolled_users: list["UserReadBasic"] = []
    company_requests: list["ReadMultipleJoinRequest"] = []

    class Config:
        from_attributes = True


# Read multiple company
class CompanyReadMultiple(CompanyBase):
    id: UUID
    enrolled_users: list["UserReadBasic"] = []
    logo: str | None = None

    class Config:
        from_attributes = True


# Update the company
class CompanyUpdate(BaseModel):
    company_name: str | None = None
    company_description: str | None = None
    company_banner: str | None = None
    company_type: str | None = None

    class Config:
        from_attributes = True
