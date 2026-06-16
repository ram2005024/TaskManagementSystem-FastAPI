from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, DateTime, func,UniqueConstraint
from app.database.db import Base
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

from .association import user_tasks
from enum import Enum


class TaskStatus(str, Enum):
    pending = "Pending",
    completed = "Completed"


class Task(Base):
    __tablename__ = "tasks"

    # Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_type = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    task_name = Column(String, nullable=False)
    task_description = Column(String)
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
    )
    project = relationship("Project", back_populates="tasks")
    status = Column(SQLEnum(TaskStatus, name="task_status"), default=TaskStatus.pending,index=True)
    users = relationship("User", secondary=user_tasks, back_populates="tasks")
    __tableargs__=(
        UniqueConstraint("task_name","project_id",name="unique_task_project")
    )