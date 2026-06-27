from uuid import UUID

from fastapi import Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models.company import Company
from app.dependencies.auth import get_user


def company_user_role_required(user_roles: list[str]):
    def dependency(
        request: Request,
        company_id: UUID,
        user=Depends(get_user),
        db: Session = Depends(get_db),
    ):
        # Check if the company exist or not
        company = db.query(Company).filter(Company.id == company_id).one_or_none()
        if company is None:
            raise HTTPException(status_code=404, detail="Company doesn't exist")
        # Return if it is admin(GLOBAL)
        if user["role"] == "Admin":
            return company, user
        enrolled_ids = [str(u.id) for u in company.enrolled_users]
        if user["user_id"] not in enrolled_ids:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission",
            )

        return company, user

    return dependency
