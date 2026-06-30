from fastapi.exceptions import HTTPException
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.database.models.task import SubTask, Task


@event.listens_for(SubTask, "after_insert")
@event.listens_for(SubTask, "after_update")
@event.listens_for(SubTask, "after_delete")
def update_task_status_progress(mapper, connection, target):
    try:
        session = Session(bind=connection)
        task = session.query(Task).filter(Task.id == target.task_id).one_or_none()
        if not task:
            raise ValueError("Task doesn't exist")
        sub_tasks = session.query(SubTask).filter(SubTask.task_id == task.id).all()
        total = len(sub_tasks)
        completed = sum(1 for s in sub_tasks if getattr(s, "status") == "Completed")
        progress = int((completed / total) * 100) if total > 0 else 0
        status = "Completed" if total > 0 and completed == total else "Pending"
        setattr(task, "status", status)
        setattr(task, "progress", progress)
        session.flush()
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error updating to the task table")
