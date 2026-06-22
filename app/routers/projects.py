from uuid import UUID

from fastapi import APIRouter, Depends, Request
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
from app.dependencies.company import company_user_role_required
from app.schemas.project import (
    ProjectCreate,
    ProjectReadMultiple,
    ProjectReadSingle,
    ProjectUpdate,
)

projectRouter = APIRouter(prefix="/project", tags=["project_endpoints"])


# Create endpoint
@projectRouter.post("/company/{company_id}", response_model=ProjectReadMultiple)
def create_project_endpoint(
    data: ProjectCreate,
    company_id: UUID,
    db: Session = Depends(get_db),
    company_detail: tuple = Depends(company_user_role_required(["Admin", "Manager"])),
):
    try:
        project = create_project(db, data)
        return project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update endpoint
@projectRouter.put(
    "/company/{company_id}/project/{project_id}", response_model=ProjectReadSingle
)
def update_project_endpoint(
    company_id: UUID,
    project_id: UUID,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    company_detail: tuple = Depends(company_user_role_required(["Admin", "Manager"])),
):
    try:
        project = update_project(db, project_id, data)
        return project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)


# Read endpoint
@projectRouter.get(
    "/company/{company_id}/project/{project_id}", response_model=ProjectReadSingle
)
def read_project_endpoint(
    company_id: UUID,
    project_id: UUID,
    db: Session = Depends(get_db),
    company_details: tuple = Depends(
        company_user_role_required(["Admin", "Member", "Manager"])
    ),
):
    project = read_project(db, company_id, project_id)
    return project


# Read multiple projects endpoint
@projectRouter.get(
    "/company/{company_id}/projects", response_model=list[ProjectReadMultiple]
)
def read_projects_endpoint(
    company_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    company_details: tuple = Depends(
        company_user_role_required(["Admin", "Member", "Manager"])
    ),
):

    projects = read_projects(company_id, request, db)
    return projects


# Delete the project
@projectRouter.delete("/company/{company_id}/project/{project_id}")
def delete_project_endpoint(
    company_id: UUID,
    project_id: UUID,
    db: Session = Depends(get_db),
    company_detail: tuple = Depends(company_user_role_required(["Admin", "Manager"])),
):
    try:
        deleted = delete_project(db, project_id)
        if deleted:
            return {"message": "Project deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)
