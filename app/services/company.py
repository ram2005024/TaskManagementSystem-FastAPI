from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.models.company import Company


# Search company by name
def find_company_by_name(query: str, db: Session):
    try:
        companies = (
            db.query(Company).filter(Company.company_name.ilike(f"%{query}")).all()
        )
        return companies
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error occured: {e}")
