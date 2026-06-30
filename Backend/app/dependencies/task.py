from uuid import UUID

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models.project import Project
from app.database.models.task import Task
from app.dependencies.auth import role_check


def project_user_required(user_role: list[str]):
    def wrapper(
        project_id: UUID,
        user=Depends(role_check(user_role)),
        db: Session = Depends(get_db),
    ):
        project = db.query(Project).filter(Project.id == project_id).one_or_none()
        if project is None:
            raise HTTPException(status_code=404, detail="Project doesn't exist.")
        project_user_ids = [str(u.id) for u in project.users]
        if user["user_id"] not in project_user_ids:
            raise HTTPException(status_code=403, detail="You don't have permission")
        return (user, project)

    return wrapper


# Task user required
def task_user_required(role: list[str]):
    def wrapper(
        task_id: UUID, user=Depends(role_check(role)), db: Session = Depends(get_db)
    ):
        task = db.query(Task).filter(Task.id == task_id).one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail="Task doesn't exist")
        task_user_ids = [u.id for u in task.users]
        if user["role"] in ["Admin", "Manager"]:
            return (user, task)
        if user["user_id"] not in task_user_ids:
            raise HTTPException(status_code=403, detail="User does not belong to task")
        return (user, task)

    return wrapper
