from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from app.schemas.company import CompanyReadSingle
    from app.schemas.task import TaskReadSingle
    from app.schemas.user import UserReadBasic


class ProjectUrgency(str, Enum):
    high = "High"
    low = "Low"
    medium = "Medium"


# Base Project Model
class ProjectBase(BaseModel):
    project_name: str
    project_type: str | None = None
    project_description: str | None = None
    company_id: UUID
    end_on: datetime

    @field_validator("project_name")
    def check_project_name(cls, v):
        if len(v) < 5:
            raise ValueError("Project name should have atleast 5 characters")
        return v


# For Creating the project
class ProjectCreate(ProjectBase):
    user_ids: list[UUID]
    urgency: ProjectUrgency


# For reading the single project
class ProjectReadSingle(ProjectBase):
    tasks: list["TaskReadSingle"] = []
    users: list["UserReadBasic"] = []
    company: "CompanyReadSingle"
    urgency: str
    updated_at: datetime
    created_at: datetime
    end_on: datetime
    status: str
    id: UUID

    class Config:
        from_attributes = True


# For reading the mulitiple projects
class ProjectReadMultiple(ProjectBase):
    id: UUID
    urgency: str
    created_at: datetime
    end_on: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# For updating the project
class ProjectUpdate(BaseModel):
    project_name: str | None = None
    project_type: str | None = None
    project_description: str | None = None
    status: str | None = None
    end_on: datetime | None = None
    urgency: str | None = None

    class Config:
        from_attributes = True


class ProjectDelete(BaseModel):
    id: UUID
