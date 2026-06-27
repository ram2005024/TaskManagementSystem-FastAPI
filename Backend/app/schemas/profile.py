from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemas.user import UserRead


# For profile read
class ProfileRead(BaseModel):
    user_id: UUID
    bio: str | None = None
    user_image: str | None = None
    full_name: str
    user: "UserRead"

    class Config:
        from_attributes: True


class ProfileBasic(BaseModel):
    user_id: UUID
    bio: str | None = None
    user_image: str | None = None
    full_name: str

    class Config:
        from_attributes: True
