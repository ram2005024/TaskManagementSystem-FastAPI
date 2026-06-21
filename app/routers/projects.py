from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.crud.project import (
    create_project,
    delete_project,
    read_project,
    read_projects,
    update_project,
)
from app.database.db import get_db
from app.schemas.project import (
    ProjectCreate,
    ProjectReadMultiple,
    ProjectReadSingle,
    ProjectUpdate,
)

projectRouter = APIRouter(prefix="/project", tags=["project_endpoints"])


# Create endpoint
@projectRouter.post("/", response_model=ProjectReadMultiple)
def create_project_endpoint(data: ProjectCreate, db: Session = Depends(get_db)):
    try:
        project = create_project(db, data)
        return project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update endpoint
@projectRouter.put("/{project_id}", response_model=ProjectReadSingle)
def update_project_endpoint(
    project_id: UUID, data: ProjectUpdate, db: Session = Depends(get_db)
):
    try:
        project = update_project(db, project_id, data)
        return project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)


# Read endpoint
@projectRouter.get("/{project_id}", response_model=ProjectReadSingle)
def read_project_endpoint(project_id: UUID, db: Session = Depends(get_db)):
    try:
        project = read_project(db, project_id)
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)


# Read multiple projects endpoint
@projectRouter.get("/", response_model=list[ProjectReadMultiple])
def read_projects_endpoint(db: Session = Depends(get_db)):
    projects = read_projects(db)
    return projects


# Delete the project
@projectRouter.delete("/{project_id}")
def delete_project_endpoint(project_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = delete_project(db, project_id)
        if deleted:
            return {"message": "Project deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)
