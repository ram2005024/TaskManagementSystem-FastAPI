from datetime import datetime
from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database.models.project import Project


# Due date verifier for task
def due_date_check(project_id: UUID, db: Session, due_date: datetime):
    try:
        project = db.query(Project).filter(Project.id == project_id).one_or_none()
        if project is not None:
            end_on = project.end_on
            created_at = project.created_at
            if due_date > end_on or due_date < created_at:
                raise HTTPException(
                    status_code=400, detail="Due date has been exceeded"
                )
        return due_date

    except Exception as e:
        raise e
