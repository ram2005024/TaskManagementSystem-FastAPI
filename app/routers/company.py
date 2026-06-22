import json
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.crud.company import (
    create_company,
    delete_company,
    get_company_list,
    get_company_single,
    update_company,
)
from app.database.db import get_db
from app.dependencies.auth import get_user
from app.schemas.company import (
    CompanyCreate,
    CompanyReadMultiple,
    CompanyReadSingle,
    CompanyUpdate,
)
from app.services.company import find_company_by_name

company_router = APIRouter(prefix="/company", tags=["company_endpoints"])


# Create the company
@company_router.post("/", response_model=CompanyReadSingle)
def register_company(
    request: Request,
    data: str = Form(...),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user: dict = Depends(get_user),
):
    create_data = CompanyCreate(**json.loads(data))
    company, error = create_company(create_data, file, db, request)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return company


# Get the list of the company
@company_router.get("/", response_model=list[CompanyReadMultiple])
def read_list_company(request: Request, db: Session = Depends(get_db)):
    companies, error = get_company_list(db, request)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return companies


# Get the single  company
@company_router.get("/{company_id}", response_model=CompanyReadSingle)
def read_single_company(
    company_id: UUID, request: Request, db: Session = Depends(get_db)
):
    company, error = get_company_single(db, request, company_id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return company


# Update the   company
@company_router.put("/{company_id}", response_model=CompanyReadSingle)
def UpdateCompany(
    company_id: UUID,
    data: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    company_update = CompanyUpdate(**json.loads(data))
    company, error = update_company(company_id, db, company_update, file)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return company


# Delete the   company
@company_router.delete("/{company_id}")
def DeleteCompany(company_id: UUID, db: Session = Depends(get_db)):
    deleted, error = delete_company(company_id, db)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Company deleted successfully"}


# Search company by name
@company_router.get("/companies/search", response_model=list[CompanyReadMultiple])
def search_company_by_name(query: str, db: Session = Depends(get_db)):
    try:
        return find_company_by_name(query, db)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
