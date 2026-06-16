from fastapi import APIRouter,Depends,Request,Form,File,UploadFile,status
from fastapi.exceptions import HTTPException

from app.schemas.company import CompanyCreate, CompanyReadSingle
from sqlalchemy.orm import Session
from app.crud.company import create_company
from app.database.db import get_db
company_router=APIRouter(prefix="/company",tags=["company_endpoint"])

# Create the company
@company_router.post("/",response_model=CompanyReadSingle)
def register_company(request:Request,company_name:str=Form(...),company_description:str|None=Form(None),company_banner:str|None=Form(None),company_type:str|None=Form(None),logo:UploadFile|None=File(None),db:Session=Depends(get_db)):
    data=CompanyCreate(
        company_name=company_name,
        company_description=company_description,
        company_banner=company_banner,
        company_type=company_type,
        manager_id=request.state.user_id
    )
    company,error=create_company(data,logo,db)
    if error:
        raise HTTPException(status_code=400,detail=error)
    return company