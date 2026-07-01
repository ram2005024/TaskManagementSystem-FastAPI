from app.core.celery import celery_app


@celery_app.task(name="app.workers.tasks.task_status.update_task_status")
def update_task_status(name):
    print("helloooooooooooooooooooooooooooooo")
    return {"message": f"Hello {name} welcome bro0000"}
