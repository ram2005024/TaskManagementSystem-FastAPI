import uuid
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base
from app.database.models.association import user_companies, user_projects, user_tasks


# Make a role ENUM
class UserRole(str, Enum):
    member = ("Member",)
    admin = "Admin"
    manager = "Manager"

    # Make a user model


class User(Base):
    __tablename__ = "users"

    # Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_pwd = Column(String)
    is_authenticated = Column(Boolean, default=False)
    role = Column(SQLEnum(UserRole, name="user_roles"), default=UserRole.member)
    isActive = Column(Boolean, default=True)
    projects = relationship("Project", secondary=user_projects, back_populates="users")

    tasks = relationship("Task", secondary=user_tasks, back_populates="users")
    profile = relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    manager_company = relationship("Company", back_populates="manager", uselist=False)
    companies = relationship(
        "Company", secondary=user_companies, back_populates="enrolled_users"
    )
    user_requests = relationship("JoinRequest", back_populates="user")


# Make a profile model for the user
class Profile(Base):
    __tablename__ = "profiles"
    # Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    bio = Column(String, nullable=True)
    user_image = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="profile")
