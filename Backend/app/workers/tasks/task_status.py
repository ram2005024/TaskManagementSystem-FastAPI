from sqlalchemy import func

from app.core.celery import celery_app
from app.database.db import SessionHandler
from app.database.models.task import Task, TaskStatus


@celery_app.task(name="app.workers.tasks.task_status.update_task_status")
def update_task_status():
    db = SessionHandler()
    try:
        tasks = (
            db.query(Task)
            .filter(Task.due_date < func.now(), Task.status != TaskStatus.failed)
            .all()
        )
        for task in tasks:
            task.status = TaskStatus.failed
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
