from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.models.project import Project
from app.database.models.task import Task
from app.database.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.dependencies.pagination import pagination


# Create task
def create_task(data: TaskCreate, project_id: UUID, db: Session):
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project doesn't exit for a task")
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
        task = Task(
            task_name=data.task_name,
            task_description=data.task_description,
            task_type=data.task_type,
            project_id=project_id,
            users=users,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except IntegrityError:
        db.rollback()
        raise ValueError("Task with the same name already exists")
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
def read_tasks(project_id: UUID, db: Session,pagination):
    try:
        page=pagination["page"]
        limit=pagination["limit"]
        total = db.query(Task).filter(Task.project_id == project_id).count()
        data=db.query(Task).filter(Task.project_id == project_id).offset((page-1)*limit).limit(limit).all()

        return {
            "meta":{
                "total":total,
                "page":page,
                "limit":limit,
                "pages":(total+limit-1)//limit
            },
            "data":data
        }
    except Exception as e:
        raise RuntimeError(f"Error occured: {e}")


# Update the task
def update_task(db: Session, task_id: UUID, data: TaskUpdate):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError("Task doesn't exist")
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
