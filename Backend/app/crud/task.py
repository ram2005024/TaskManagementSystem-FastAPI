from datetime import datetime
from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.models.association import task_tasks, user_tasks
from app.database.models.project import Project
from app.database.models.task import SubTask, Task
from app.database.models.user import User
from app.schemas.task import SubTaskSchema, TaskCreate, TaskUpdate
from app.services.task import due_date_check


# Create task
def create_task(data: TaskCreate, project_id: UUID, db: Session, project: Project):
    try:
        insert_data = data.model_dump(exclude_unset=True).copy()
        due_date = project.end_on
        if data.due_date:
            due_date = due_date_check(project_id, db, data.due_date)
        for key in ["user_ids", "block_task_ids", "subtasks", "due_date"]:
            insert_data.pop(key, None)
        new_task = Task(project_id=project_id, due_date=due_date, **insert_data)
        db.add(new_task)
        db.flush()
        # 1. Handle user ids
        if data.user_ids:
            users = db.query(User).filter(User.id.in_(data.user_ids)).all()
            if not users:
                raise ValueError("Task must be assigned to atleast one memeber")
            invalid_users = [
                str(user.username) for user in users if user not in project.users
            ]
            if invalid_users:
                raise ValueError(
                    f"{'User' if len(invalid_users) == 1 else 'Users'} {', '.join(invalid_users)} {'is' if len(invalid_users) == 1 else 'are'} not included in the project."
                )
            # Put the user
            db.execute(
                user_tasks.insert(),
                [{"user_id": u, "task_id": new_task.id} for u in data.user_ids],
            )
        # 2.When the blocktask ids are given
        if data.block_task_ids:
            try:
                all_valid = db.query(Task).filter(
                    Task.id.in_(data.block_task_ids)
                ).count() == len(data.block_task_ids)
                if not all_valid:
                    raise ValueError("Task doesn't exist")

                db.execute(
                    task_tasks.insert(),
                    [
                        {"task_id": bid, "blocked_by_id": new_task.id}
                        for bid in data.block_task_ids
                    ],
                )
            except Exception as e:
                db.rollback()
                raise e
        # 3. For the sub task
        if data.subtasks:
            try:
                for stask in data.subtasks:
                    sub_task_data = stask.model_dump(exclude_unset=True)
                    sub_task_data["task_id"] = new_task.id
                    sub_task = SubTask(**sub_task_data)
                    db.add(sub_task)
            except IntegrityError:
                db.rollback()
                raise ValueError("Sub task with the same name already exists.")
        db.commit()
        return new_task
    except IntegrityError as e:
        db.rollback()
        orig = getattr(e, "orig", None)
        code = getattr(orig, "pgcode", None)
        diag = getattr(orig, "diag", None)
        unique_contraint = getattr(diag, "constraint_name", None)
        column = getattr(diag, "column_name", None)
        if code == "23502":
            if column == "project_id":
                raise ValueError("Project ID required to create a task")
        elif code == "23505":
            if unique_contraint == "Unique subtask per task":
                raise ValueError("Same subtask already exist for the given task")
            elif unique_contraint == "Unique task per project":
                raise ValueError("Same task exists for the given project")
            else:
                raise ValueError(f"Unqiue contraint violation:{unique_contraint}")
        else:
            raise RuntimeError(f"Database integrity error: {e.orig}")
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error occured: {e}")


# Read single task
def read_task(task_id: UUID, db: Session):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError("Task doesn't exist")
        return task
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error occured {e}")


# Read multiple task
def read_tasks(project_id: UUID, db: Session, pagination):
    try:
        page = pagination["page"]
        limit = pagination["limit"]
        total = db.query(Task).filter(Task.project_id == project_id).count()
        data = (
            db.query(Task)
            .filter(Task.project_id == project_id)
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return {
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
                "pages": (total + limit - 1) // limit,
            },
            "data": data,
        }
    except Exception as e:
        raise RuntimeError(f"Error occured: {e}")


# Update the task
def update_task(db: Session, task_id: UUID, data: TaskUpdate):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError("Task doesn't exist")
        is_valid_due_date = due_date_check(task.project_id, db, datetime.utcnow())
        if is_valid_due_date:
            to_update_data = data.model_dump(exclude_unset=True)
            for key, value in to_update_data.items():
                setattr(task, key, value)
            db.add(task)
            db.commit()
            db.refresh(task)
            return task
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error occured: {e}")


# Delete the task


def delete_task(db: Session, task_id: UUID):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError("Task doesn't exist")
        db.delete(task)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error occured :{e}")


# Change the user list
def change_user_list(
    user_ids: list[UUID], project_id: UUID, db: Session, task_id: UUID
):
    try:
        task = (
            db.query(Task)
            .filter(Task.project_id == project_id, Task.id == task_id)
            .one_or_none()
        )
        if task is None:
            raise ValueError("Task doesn't exist.")
        # Check if all the users belongs to task
        users = db.query(User).filter(User.id.in_(user_ids)).all()
        if not users:
            raise ValueError("Invalid users")
        unauthorized_users = [u.username for u in users if u not in task.users]
        if unauthorized_users:
            raise ValueError(
                f"{'User' if len(unauthorized_users) == 1 else 'Users'} {', '.join(unauthorized_users)} {'is' if len(unauthorized_users) == 1 else 'are'} not included in the project."
            )
        new_ids = set(user_ids)
        current_ids = {u.id for u in task.users}
        to_add_ids = new_ids - current_ids
        to_remove_ids = current_ids - new_ids
        if to_add_ids:
            to_add_users = db.query(User).filter(User.id.in_(to_add_ids)).all()
            task.users.extend(to_add_users)
        if to_remove_ids:
            task.users = [u for u in task.users if u.id not in to_remove_ids]
        db.commit()
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Update the block list of task
def blocklist_update(
    project_id: UUID, task_id: UUID, db: Session, block_ids: list[UUID]
):
    try:
        task = (
            db.query(Task)
            .filter(Task.id == task_id, Task.project_id == project_id)
            .one_or_none()
        )
        if task is None:
            raise ValueError("Task doesn't exist")
        if task.is_blocked:
            raise ValueError("This task is blocked.Please try again")
        blocking_tasks = db.query(Task).filter(Task.id.in_(block_ids)).all()
        if len(blocking_tasks) != len(block_ids):
            raise ValueError("Some task doesn't exist")
        if task.id in block_ids:
            raise ValueError("Same task can't be blocked by itself")
        if any(t.project_id != project_id for t in blocking_tasks):
            raise ValueError("Task doesn't belong to the same project")
        previous_block_ids = {t.id for t in task.blocks}
        new_block_ids = set(block_ids)
        to_add_ids = new_block_ids - previous_block_ids
        if to_add_ids:
            to_add_tasks = db.query(Task).filter(Task.id.in_(to_add_ids)).all()
            task.blocks.extend(to_add_tasks)
        to_remove_ids = previous_block_ids - new_block_ids
        if to_remove_ids:
            task.blocks = [t for t in task.blocks if t.id not in to_remove_ids]
        db.commit()
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Create subtask
def create_subtask(task_id: UUID, data: SubTaskSchema, db: Session):
    try:
        sub_task = SubTask(task_id=task_id, **data.model_dump(exclude_unset=True))
        db.add(sub_task)
        db.commit()
        return sub_task
    except IntegrityError as e:
        db.rollback()
        orig = getattr(e, "orig", None)
        diag = getattr(orig, "diag", None)
        constraint = getattr(diag, "constraint_name", None)
        column = getattr(diag, "column_name", None)
        code = getattr(orig, "pgcode", None)
        if code == "23505":  # Contraint error
            if constraint == "Unique subtask per task":
                raise HTTPException(
                    status_code=400, detail="SubTask already exists for the task"
                )
            else:
                raise HTTPException(
                    status_code=400, detail=f"Constraint error:{constraint}"
                )
        if code == "23502":
            if column == "task_id":
                raise HTTPException(status_code=400, detail="Task id is not provided")
            else:
                raise HTTPException(
                    status_code=400, detail=f"Nullable error for column: {column}"
                )
        raise HTTPException(status_code=400, detail=f"Integrity error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Update subtask
def update_subtask(task_id: UUID, sub_task_id, update_data: SubTaskSchema, db: Session):
    try:
        sub_task = (
            db.query(SubTask)
            .filter(SubTask.task_id == task_id, SubTask.id == sub_task_id)
            .one_or_none()
        )
        if not sub_task:
            raise HTTPException(status_code=404, detail="Subtask not found")
        if update_data.status and sub_task.task.is_blocked:
            raise HTTPException(
                status_code=400, detail="Can't change the status for the blocked task"
            )
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(sub_task, key, value)
        db.commit()
        return sub_task
    except Exception as e:
        db.rollback()
        raise e

    # Delete the subtask


def delete_subtask(task_id: UUID, subtask_id: UUID, db: Session):
    try:
        sub_task = (
            db.query(SubTask)
            .filter(SubTask.task_id == task_id, SubTask.id == subtask_id)
            .one_or_none()
        )
        if sub_task is None:
            raise HTTPException(status_code=404, detail="SubTask doesn't exist")
        db.delete(sub_task)
        db.commit()
        return True
    except Exception as e:
        raise e
