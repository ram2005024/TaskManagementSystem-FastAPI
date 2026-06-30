import uuid
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.db import Base
from app.database.models.association import task_tasks

from .association import user_tasks


class TaskStatus(str, Enum):
    pending = "Pending"
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
        nullable=False,
    )
    project = relationship("Project", back_populates="tasks")
    status = Column(
        SQLEnum(TaskStatus, name="task_status"), default=TaskStatus.pending, index=True
    )
    users = relationship("User", secondary=user_tasks, back_populates="tasks")
    sub_tasks = relationship("SubTask", back_populates="task")
    progress = Column(Integer, default=0)
    blocked_by = relationship(
        "Task",
        secondary=task_tasks,
        primaryjoin=id == task_tasks.c.task_id,
        secondaryjoin=id == task_tasks.c.blocked_by_id,
        backref="blocks",
    )
    __table_args__ = (
        UniqueConstraint("task_name", "project_id", name="Unique task per project"),
    )

    @property
    def is_blocked(self) -> bool:
        return any(b.status != TaskStatus.completed for b in self.blocked_by)


class SubTask(Base):
    __tablename__ = "subtasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(
        UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    task = relationship("Task", back_populates="sub_tasks")
    status = Column(
        SQLEnum(TaskStatus, name="Sub-Task status"), default=TaskStatus.pending
    )
    sub_task_name = Column(String, nullable=False)
    sub_task_description = Column(String)
    __table_args__ = (
        UniqueConstraint(
            "sub_task_name",
            "task_id",
            name="Unique subtask per task",
        ),
    )
