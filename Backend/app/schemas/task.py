from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from app.schemas.project import ProjectReadMultiple
    from app.schemas.user import UserReadBasic


class TaskStatus(str, Enum):
    pending = "Pending"
    completed = "Completed"


class SubTask(BaseModel):
    sub_task_name: Optional[str]
    sub_task_description: Optional[str]
    status: TaskStatus = TaskStatus.pending
    id: Optional[UUID] = None

    @field_validator("sub_task_name")
    def check_sub_task_name(cls, v):
        if len(v) < 5:
            raise ValueError("Subtask name should be at least 5 characters")
        return v


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
    block_task_ids: Optional[list[UUID]]
    subtasks: list[SubTask]


class TaskBasic(TaskBase):
    id: UUID


# For task read single
class TaskReadSingle(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    project: "ProjectReadMultiple"
    status: str
    blocks: Optional[list[TaskBasic]]
    blocked_by: Optional[list[TaskBasic]]
    sub_tasks: list[SubTask]
    is_blocked: bool
    users: list["UserReadBasic"]

    class Config:
        from_attributes = True


# For task read single
class TaskReadMultiple(TaskBase):
    id: UUID
    created_at: datetime
    status: str
    users: list["UserReadBasic"]
    sub_tasks: list[SubTask]
    is_blocked: bool
    blocks: Optional[list[TaskBasic]]
    blocked_by: Optional[list[TaskBasic]]

    class Config:
        from_attributes = True


# For task update
class TaskUpdate(BaseModel):
    id: UUID
    task_type: str | None = None
    task_name: str | None = None
    task_description: str | None = None
