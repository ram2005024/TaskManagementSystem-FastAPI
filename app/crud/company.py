from sqlalchemy.orm import Session
from fastapi import UploadFile,Request
from app.schemas.company import CompanyCreate
from app.database.models import Company
from app.utils.upload_image import upload_image
from app.database.models.user import User

# Create company
def create_company(data:CompanyCreate,logo:UploadFile,db:Session):
    # Handle the image upload
    try:
        company=Company(company_name=data.company_name,
                        company_description=data.company_description,
                        company_banner=data.company_banner,
                        company_type=data.company_type,
                        manager_id=data.manager_id,
                        )
        db.add(company)
        db.commit()
        db.refresh(company)
        
        image_url=""
        if logo.filename:
            image_url=upload_image(logo,"company",company.id)
        
        company.logo=image_url
        db.commit()
        # Change the role of the user as Manager for the company
        user=db.query(User).filter(User.id==data.manager_id).first()
        user.role="Manager"
        db.add(user)
        db.commit()
        return company,None
    except Exception as e:
        db.rollback()
        return None,f"Error occured {e}"