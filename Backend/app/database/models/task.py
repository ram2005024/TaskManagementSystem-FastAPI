import uuid
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.db import Base

from .association import user_tasks


class TaskStatus(str, Enum):
    pending = ("Pending",)
    completed = "Completed"


class Task(Base):
    __tablename__ = "tasks"

    # Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_type = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    task_name = Column(String, nullable=False)
    task_description = Column(String)
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
    )
    project = relationship("Project", back_populates="tasks")
    status = Column(
        SQLEnum(TaskStatus, name="task_status"), default=TaskStatus.pending, index=True
    )
    users = relationship("User", secondary=user_tasks, back_populates="tasks")
    __table_args__ = (
        UniqueConstraint("task_name", "project_id", name="unique_task_project"),
    )
