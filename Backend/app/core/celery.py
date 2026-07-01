from celery import Celery

from .config import settings

celery_app = Celery(
    name="task-management-system",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BACKEND_URL,
)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
celery_app.conf.beat_schedule = {
    "update_task_status_every_5mins": {
        "task": "app.workers.tasks.task_status.update_task_status",
        "schedule": 300.0,
    }
}
celery_app.autodiscover_tasks(["app.workers.tasks"])
