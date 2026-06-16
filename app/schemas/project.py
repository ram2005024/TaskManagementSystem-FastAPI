from pydantic import BaseModel,field_validator
from datetime import date,datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.company import CompanyReadSingle
    from app.schemas.task import TaskReadSingle
    from app.schemas.user import UserRead
# Base Project Model
class ProjectBase(BaseModel):
    project_name:str
    project_type:str|None=None
    project_description:str|None=None
    company_id:str

    @field_validator("project_name")
    def check_project_name(cls,v):
        if len(v)<5:
            raise ValueError("Project name should have atleast 5 characters")
        return v
    
# For Creating the project
class ProjectCreate(ProjectBase):
    end_on:date

# For reading the single project
class ProjectReadSingle(ProjectCreate):
    tasks:list["TaskReadSingle"]=[]
    users:list["UserRead"]=[]
    company:list["CompanyReadSingle"]=[]
    urgency:str
    updated_at:datetime
    created_at:datetime
    status:str
    id:str
    
    class Config:
        form_attributes=True

# For reading the mulitiple projects
class ProjectReadMultiple(ProjectBase):
    pass
    class Config:
        form_attributes=True

# For updating the project
class ProjectUpdate(ProjectReadSingle):
    project_name:str|None=None
    project_type:str|None=None
    project_description:str|None=None
    status:str|None=None
    end_one:date|None=None
    urgency:str|None=None

    class Config:
        form_attributes=True
    
class ProjectDelete(BaseModel):
    id:str

