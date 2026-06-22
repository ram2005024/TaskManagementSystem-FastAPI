from uuid import UUID

from fastapi import Request, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.models import Company
from app.database.models.user import User
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.utils.upload_image import upload_image


# Create company
def create_company(
    data: CompanyCreate, logo: UploadFile, db: Session, request: Request
):
    # Handle the image upload
    try:
        company = Company(
            company_name=data.company_name,
            company_description=data.company_description,
            company_banner=data.company_banner,
            company_type=data.company_type,
            manager_id=request.state.user["user_id"],
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        # Add manager in enrolled company users
        manager = db.query(User).filter(User.id == company.manager_id).first()
        if manager:
            company.enrolled_users.append(manager)
            db.commit()

        image_url = ""
        if logo and logo.filename:
            image_url: str = upload_image(logo, "company", str(company.id))

        company.logo = image_url  # type: ignore
        db.commit()
        # Change the role of the user as Manager for the company
        user = db.query(User).filter(User.id == request.state.user["user_id"]).first()
        user.role = "Manager"
        db.add(user)
        db.commit()
        return company, None
    except IntegrityError:
        db.rollback()
        return None, "Manager already exists for this company"
    except Exception as e:
        db.rollback()
        return None, f"Error occured  {e}"


# GET LIST
def get_company_list(db: Session, request: Request):
    try:
        user = db.query(User).filter(User.id == request.state.user["user_id"]).first()
        companies = user.companies
        return companies, None

    except Exception as e:
        return None, f"Error occured: {e}"


# GET Single
def get_company_single(db: Session, request: Request, c_id: UUID):
    try:
        company = db.query(Company).filter(Company.id == c_id).first()
        return company, None

    except Exception as e:
        return None, f"Error occured: {e}"


# Update company info
def update_company(c_id: UUID, db: Session, data: CompanyUpdate, file: UploadFile):
    new_url = ""
    try:
        if file and file.filename:
            new_url = upload_image(file, "company", c_id)
        company = db.query(Company).filter(Company.id == c_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(company, key, value)
        if new_url:
            company.logo = new_url
        db.commit()
        db.refresh(company)
        return company, None
    except Exception as e:
        return None, f"Error occured: {e}"


# Delete the company
def delete_company(c_id: UUID, db: Session):
    try:
        company = db.query(Company).filter(Company.id == c_id).first()
        if not company:
            return None, "Company doesn't exist."
        db.delete(company)
        db.commit()
        return True, None
    except Exception as e:
        db.rollback()
        return None, f"Error occured: {e}"
