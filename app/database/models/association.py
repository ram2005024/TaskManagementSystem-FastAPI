from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.dialects.postgresql import UUID
from app.database.db import Base

# For user and tasks
user_tasks = Table(
    "user_tasks",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("task_id", UUID(as_uuid=True), ForeignKey("tasks.id"), primary_key=True),
)
# For user and projects
user_projects = Table(
    "user_projects",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column(
        "project_id", UUID(as_uuid=True), ForeignKey("projects.id"), primary_key=True
    ),
)
# For user and companies Many to many
user_companies=Table(
    "user_companies",
    Base.metadata,
    Column("user_id",UUID(as_uuid=True),ForeignKey("users.id"),primary_key=True),
    Column("company_id",UUID(as_uuid=True),ForeignKey("companies.id"),primary_key=True)
)
