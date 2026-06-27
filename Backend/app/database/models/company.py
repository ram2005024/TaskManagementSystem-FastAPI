import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.db import Base
from app.database.models.association import user_companies


class Company(Base):
    __tablename__ = "companies"
    # Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String, nullable=False, unique=True, index=True)
    issue_date = Column(DateTime, server_default=func.now())
    projects = relationship("Project", back_populates="company")
    company_description = Column(String)
    company_banner = Column(String)
    company_type = Column(String)
    is_active = Column(Boolean, default=True)
    manager_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )
    manager = relationship("User", back_populates="manager_company")
    enrolled_users = relationship(
        "User", secondary=user_companies, back_populates="companies"
    )
    updated_at = Column(DateTime, onupdate=func.now())
    logo = Column(String)
    company_requests = relationship("JoinRequest", back_populates="company")
    __table_args__ = (
        UniqueConstraint("company_name", "manager_id", name="unique_company_manager"),
    )
