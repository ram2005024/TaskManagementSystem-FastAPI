from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.user import UserRead
    from app.schemas.company import CompanyReadSingle
# Create schema 
class JoinRequestCreate(BaseModel):
    user_id:str
    company_id:str

# Read schema
class ReadSingleJoinRequest(BaseModel):
    id:str
    user:"UserRead|None"=None
    company:"CompanyReadSingle|None"=None
    status:str|None=None
    class Config:
        form_attributes=True
# Read schema
class ReadMultipleJoinRequest(BaseModel):
    requests:list[ReadSingleJoinRequest]=[]
    class Config:
        form_attributes=True
    
# Update schema
class UpdateJoinRequest(BaseModel):
    id:str
    user_id:str
    company_id:str
    status:str
    class Config:
        form_attributes=True
