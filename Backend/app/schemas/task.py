from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from app.schemas.project import ProjectReadMultiple
    from app.schemas.user import UserReadBasic


class TaskStatus(str, Enum):
    pending = ("Pending",)
    completed = "Completed"


# Base Task MODEL
class TaskBase(BaseModel):
    task_name: str
    task_type: str | None = None
    task_description: str | None = None

    @field_validator("task_name")
    def check_task_name(cls, v):
        if len(v) < 5:
            raise ValueError("Task name should have atleast 5 characters")
        return v


# For task create
class TaskCreate(TaskBase):
    user_ids: list[UUID]


# For task read single
class TaskReadSingle(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    project: "ProjectReadMultiple"
    status: str
    users: list["UserReadBasic"]

    class Config:
        from_attributes = True


# For task read single
class TaskReadMultiple(TaskBase):
    id: UUID
    created_at: datetime
    status: str
    users: list["UserReadBasic"]

    class Config:
        from_attributes = True


# For task update
class TaskUpdate(BaseModel):
    id: UUID
    task_type: str | None = None
    task_name: str | None = None
    task_description: str | None = None
    status: TaskStatus | None = None
