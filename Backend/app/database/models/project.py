import uuid
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.db import Base

from .association import user_projects


class ProjectStatus(str, Enum):
    done = ("Done",)
    running = "Running"
    failed = "Failed"


class ProjectUrgency(str, Enum):
    high = ("High",)
    low = ("Low",)
    medium = "Medium"


class Project(Base):
    __tablename__ = "projects"

    # Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_name = Column(String, nullable=False, unique=True)
    project_type = Column(String)
    status = Column(
        SQLEnum(ProjectStatus, name="project_status"),
        default=ProjectStatus.running,
        index=True,
    )
    created_at = Column(DateTime, server_default=func.now())
    end_on = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    project_description = Column(String)
    users = relationship("User", secondary=user_projects, back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    urgency = Column(
        SQLEnum(ProjectUrgency, name="project_urgency"), default=ProjectUrgency.medium
    )
    company_id = Column(
        UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE")
    )
    company = relationship("Company", back_populates="projects")
    __table_args__ = (
        UniqueConstraint("project_name", "company_id", name="unique_company_project"),
    )
