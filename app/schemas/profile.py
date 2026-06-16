from pydantic import BaseModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.schemas.user import UserRead
# For profile read
class ProfileRead(BaseModel):
    user_id:str
    bio:str|None=None
    user_image:str|None=None
    full_name:str
    user:"UserRead"
    
    class Config:
        form_attributes:True

