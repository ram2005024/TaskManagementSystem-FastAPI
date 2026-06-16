from sqlalchemy import Column,ForeignKey,Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from enum import Enum
from app.database.db import Base
# Make the join requests table
class StatusEnum(str,Enum):
    approved="APPROVED"
    pending="PENDING"

class JoinRequest(Base):
    __tablename__="joinrequests"
    # Fields
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),unique=True)
    company_id=Column(UUID(as_uuid=True),ForeignKey("companies.id",ondelete="CASCADE"),unique=True)
    user=relationship("User",back_populates="user_requests")
    company=relationship("Company",back_populates="company_requests")
    status=Column(SQLEnum(StatusEnum,name="join_request_enum"),default=StatusEnum.pending)
    