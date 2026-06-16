from sqlalchemy import Column,String,DateTime,func,Boolean,ForeignKey
from app.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
class Company(Base):
    __tablename__="companies"
    # Fields
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    company_name=Column(String,nullable=False)
    issue_date=Column(DateTime,server_default=func.now())
    projects=relationship("Project",back_populates="company")
    company_description=Column(String)
    company_banner=Column(String)
    company_type=Column(String)
    is_active=Column(Boolean,default=True)
    manager_id=Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="SET NULL"),unique=True,nullable=True)
    manager=relationship("User",back_populates="manager_company")
    enrolled_users=relationship("User",back_populates="company")
    updated_at=Column(DateTime,onupdate=func.now())
    logo=Column(String)