from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.crud.task import (
    blocklist_update,
    change_user_list,
    create_subtask,
    create_task,
    delete_subtask,
    delete_task,
    read_task,
    read_tasks,
    update_subtask,
    update_task,
)
from app.database.db import get_db
from app.dependencies.pagination import pagination
from app.dependencies.task import project_user_required, task_user_required
from app.schemas.pagination import PaginatedResponse
from app.schemas.task import (
    SubTaskSchema,
    TaskCreate,
    TaskReadMultiple,
    TaskReadSingle,
    TaskUpdate,
)

task_router = APIRouter(prefix="/task", tags=["task_endpoints"])


# Create task
@task_router.post("/project/{project_id}", response_model=TaskReadMultiple)
def create_task_endpoint(
    data: TaskCreate,
    project_id: UUID,
    db: Session = Depends(get_db),
    project_details: tuple = Depends(project_user_required(["Admin", "Manager"])),
):
    try:
        user, project = project_details
        task = create_task(data, project_id, db, project)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Read single task
@task_router.get("/project/{project_id}/task/{task_id}", response_model=TaskReadSingle)
def read_task_endpoint(
    task_id: UUID,
    project_id: UUID,
    db: Session = Depends(get_db),
    project_details: tuple = Depends(
        project_user_required(["Admin", "Manager", "Member"])
    ),
):
    try:
        task = read_task(task_id, db)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Read multiple tasks task
@task_router.get(
    "/project/{project_id}/tasks", response_model=PaginatedResponse[TaskReadMultiple]
)
def read_tasks_endpoint(
    project_id: UUID,
    pagination: dict = Depends(pagination),
    db: Session = Depends(get_db),
    project_details: tuple = Depends(
        project_user_required(["Admin", "Manager", "Member"])
    ),
):
    try:
        tasks = read_tasks(project_id, db, pagination)
        return tasks
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update the basic info of task
@task_router.patch(
    "/project/{project_id}/task/{task_id}", response_model=TaskReadSingle
)
def update_task_endpoint(
    task_id: UUID,
    project_id: UUID,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    project_details: tuple = Depends(project_user_required(["Admin", "Manager"])),
):
    try:
        task = update_task(db, task_id, data)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete the task
@task_router.delete("project/{project_id}/task/{task_id}")
def delete_task_endpoint(
    task_id: UUID,
    project_id: UUID,
    db: Session = Depends(get_db),
    project_details: tuple = Depends(project_user_required(["Admin", "Manager"])),
):
    try:
        deleted = delete_task(db, task_id)
        if deleted:
            return {"message": "Task deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)


# Update the user list for the task
@task_router.patch(
    "/project/{project_id}/task/{task_id}/users", response_model=TaskReadSingle
)
def change_user_list_of_task(
    user_ids: list[UUID],
    project_id: UUID,
    task_id: UUID,
    db: Session = Depends(get_db),
    project_details: tuple = Depends(project_user_required(["Admin", "Manager"])),
):
    updated_task = change_user_list(user_ids, project_id, db, task_id)
    return updated_task


# Update the block list task
@task_router.patch(
    "/project/{project_id}/task/{task_id}/blocklist", response_model=TaskReadSingle
)
def update_blocklist_task(
    project_id: UUID,
    task_id: UUID,
    block_task_ids: list[UUID],
    db: Session = Depends(get_db),
    project_details: tuple = Depends(project_user_required(["Admin", "Manager"])),
):
    task = blocklist_update(project_id, task_id, db, block_task_ids)
    return task


@task_router.post("/{task_id}/subtask", response_model=SubTaskSchema)
def create_new_subtask(
    task_id: UUID,
    data: SubTaskSchema,
    db: Session = Depends(get_db),
    task_user: tuple = Depends(task_user_required(["Admin", "Manager"])),
):
    subtask = create_subtask(task_id, data, db)
    return subtask


@task_router.patch("/{task_id}/subtask/{subtask_id}", response_model=SubTaskSchema)
def update_subtask_endpoint(
    data: SubTaskSchema,
    task_id: UUID,
    subtask_id: UUID,
    db: Session = Depends(get_db),
    task_user: tuple = Depends(task_user_required(["Admin", "Manager"])),
):
    data = update_subtask(task_id, subtask_id, data, db)
    return data


@task_router.delete("/{task_id}/subtask/{subtask_id}")
def delete_subtask_endpoint(
    task_id: UUID,
    subtask_id: UUID,
    task_user: tuple = Depends(task_user_required(["Admin", "Manager"])),
    db: Session = Depends(get_db),
):
    data = delete_subtask(task_id, subtask_id, db)
    if data:
        return {"message": "Deleted subtask "}
