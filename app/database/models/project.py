from sqlalchemy import Column, String, Enum as SQLEnum, DateTime, func, Date
from app.database.db import Base
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
from .association import user_projects

from enum import Enum


class ProjectStatus(str, Enum):
    done = "Done",
    running = "Running"
    failed = "Failed"


class ProjectUrgency(str, Enum):
    high = "High",
    low = "Low",
    medium = "Medium"


class Project(Base):
    __tablename__ = "projects"

    # Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_name = Column(String, nullable=False)
    project_type = Column(String)
    status = Column(
        SQLEnum(ProjectStatus, name="project_status"), default=ProjectStatus.running
    )
    created_at = Column(DateTime, server_default=func.now())
    end_on = Column(Date, nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())
    project_description = Column(String)
    users = relationship("User", secondary=user_projects, back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    urgency = Column(
        SQLEnum(ProjectUrgency, name="project_urgency"), default=ProjectUrgency.medium
    )
