from pydantic import BaseModel,field_validator
from uuid import UUID
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.project import ProjectReadSingle
    from app.schemas.user import UserRead
# Base Task MODEL
class TaskBase(BaseModel):
    task_name:str
    task_type:str|None=None
    task_description:str|None=None
    @field_validator("task_name")
    def check_task_name(cls,v):
        if len(v)<5:
            raise ValueError("Task name should have atleast 5 characters")
        return v
# For task create
class TaskCreate(TaskBase):
    project_id:str
    status:str
    user_ids:list[UUID]

# For task read single
class TaskReadSingle(TaskBase):
    id:str
    created_at:datetime
    updated_at:datetime
    project:"ProjectReadSingle"
    status:str
    users:list["UserRead"]
    
    class Config:
        form_attributes:True

# For task read single
class TaskReadMultiple(TaskBase):
    id:str
    created_at:datetime
    status:str
    users:list["UserRead"]
    
    class Config:
        form_attributes:True

# For task update
class TaskUpdate(BaseModel):
    id:str
    task_type:str|None=None
    task_name:str|None=None
    task_description:str|None=None
    status:str|None=None
    user_ids:list[UUID]
    
    