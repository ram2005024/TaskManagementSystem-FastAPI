from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.crud.task import create_task, delete_task, read_task, read_tasks, update_task
from app.database.db import get_db
from app.schemas.task import TaskCreate, TaskReadMultiple, TaskReadSingle, TaskUpdate

task_router = APIRouter(prefix="/task", tags=["task_endpoints"])


# Create task
@task_router.post("/", response_model=TaskReadMultiple)
def create_task_endpoint(data: TaskCreate, db: Session = Depends(get_db)):
    try:
        task = create_task(data, db)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Read single task
@task_router.get("/{task_id}", response_model=TaskReadSingle)
def read_task_endpoint(task_id: UUID, db: Session = Depends(get_db)):
    try:
        task = read_task(task_id, db)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Read multiple tasks task
@task_router.get("/tasks/{project_id}", response_model=list[TaskReadMultiple])
def read_tasks_endpoint(project_id: UUID, db: Session = Depends(get_db)):
    try:
        tasks = read_tasks(project_id, db)
        return tasks
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update the basic info of task
@task_router.put("/{task_id}", response_model=TaskReadSingle)
def update_task_endpoint(
    task_id: UUID, data: TaskUpdate, db: Session = Depends(get_db)
):
    try:
        task = update_task(db, task_id, data)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete the task
@task_router.delete("/{task_id}")
def delete_task_endpoint(task_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = delete_task(db, task_id)
        if deleted:
            return {"message": "Task deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)
