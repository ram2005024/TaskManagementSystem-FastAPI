from pydantic import BaseModel
from typing import TYPE_CHECKING
from uuid import  UUID

if TYPE_CHECKING:
    from app.schemas.user import UserRead
    from app.schemas.company import CompanyBasic
# Create schema 
class JoinRequestCreate(BaseModel):
    user_id:UUID
    company_id:UUID

# Read schema
class ReadSingleJoinRequest(BaseModel):
    id:UUID
    user:"UserRead|None"=None
    company:"CompanyBasic|None"=None
    status:str|None=None
    class Config:
        from_attributes=True
# Read schema
class ReadMultipleJoinRequest(BaseModel):
    requests:list[ReadSingleJoinRequest]=[]
    class Config:
        from_attributes=True
    
# Update schema
class UpdateJoinRequest(BaseModel):
    id:UUID
    user_id:UUID
    company_id:UUID
    status:str
    class Config:
        from_attributes=True
