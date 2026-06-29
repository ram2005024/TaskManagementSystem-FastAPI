from datetime import date
from enum import Enum
from typing import List, Optional
from uuid import UUID

from fastapi import Query

from app.database.models.project import ProjectStatus, ProjectUrgency
from app.database.models.task import TaskStatus


class SubTaskRange(str, Enum):
    high = "High"
    low = "Low"
    medium = "Medium"


class ProjectFilter:
    def __init__(
        self,
        project_type: Optional[str] = Query(None),
        urgency: Optional[ProjectUrgency] = Query(None),
        status: Optional[ProjectStatus] = Query(None),
        min_users: Optional[int] = Query(None, ge=0),
        min_tasks: Optional[int] = Query(None, ge=0),
        start_date: Optional[date] = Query(None),
        end_date: Optional[date] = Query(None),
    ):
        self.status = status
        self.urgency = urgency
        self.project_type = project_type
        self.min_tasks = min_tasks
        self.min_users = min_users
        self.start_date = start_date
        self.end_date = end_date


class TaskFilter:
    def __init__(
        self,
        # BASIC FILTERING QUERIES
        task_name: Optional[str] = Query(None),
        task_type: Optional[str] = Query(None),
        start_date: Optional[date] = Query(None),
        end_date: Optional[date] = Query(None),
        status: Optional[TaskStatus] = Query(None),
        user_id: Optional[UUID] = Query(None),
        # ADVANCED FILTERING QUERIES
        user_ids: Optional[List[UUID]] = Query(None),
        min_users: Optional[int] = Query(None, ge=0),
        is_blocked: Optional[bool] = Query(None),
        is_blocker: Optional[bool] = Query(None),
        progress: Optional[int] = Query(None),
        sub_task: Optional[SubTaskRange] = Query(None),
        due_date: Optional[date] = Query(None),
    ):
        # BASIC
        self.task_name = task_name
        self.task_type = task_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.user_id = user_id

        # ADVANCED
        self.user_ids = user_ids
        self.min_users = min_users
        self.is_blocked = is_blocked
        self.is_blocker = is_blocker
        self.progress = progress
        self.sub_task = sub_task
        self.due_date = due_date
