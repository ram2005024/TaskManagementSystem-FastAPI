from pydantic import BaseModel,field_validator
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.project import ProjectReadSingle
    from app.schemas.user import UserRead
    from app.schemas.join_requests import ReadMultipleJoinRequest

class CompanyBase(BaseModel):
    company_name:str
    company_description:str|None=None
    company_banner:str|None=None
    company_type:str|None=None
    logo:str|None=None

    @field_validator("company_name")
    def check_company_name(cls,v):
        if len(v)<5:
            raise ValueError("Company name should have atleast 5 characters")
        return v
    
# Create Company
class CompanyCreate(CompanyBase):
    pass

# Read  company
class CompanyReadSingle(CompanyBase):
    id:str
    issue_date:datetime
    updated_at:datetime
    is_active:bool
    projects:list["ProjectReadSingle"]=[]
    manager:"UserRead |None"=None
    enrolled_users:list["UserRead"]=[]
    company_requests:list["ReadMultipleJoinRequest"]=[]
    class Config:
        form_attributes=True

# Read multiple company
class CompanyReadMultiple(CompanyBase):
    enrolled_users:list["UserRead"]=[]
    
    class Config:
        form_attributes=True

# Update the company
class CompanyUpdate(BaseModel):
    id:str
    company_name:str|None=None
    company_description:str|None=None
    company_banner:str|None=None
    company_type:str|None=None
    logo:str|None=None

    class Config:
        form_attributes=True
