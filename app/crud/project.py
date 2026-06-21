from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.models.company import Company
from app.database.models.project import Project
from app.database.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


# Create the project for the company
def create_project(db: Session, data: ProjectCreate):
    try:
        project = Project(
            project_name=data.project_name,
            project_type=data.project_type,
            project_description=data.project_description,
            company_id=data.company_id,
            end_on=data.end_on,
            urgency=data.urgency,
        )
        # Find the users from the passed user data and insert into the projects
        users = db.query(User).filter(User.id.in_(data.user_ids)).all()
        if not users:
            raise ValueError("Project must be assigned to at least one user")
        for user in users:
            belongs = (
                db.query(User)
                .filter(
                    User.id == user.id,
                    User.companies.any(Company.id == data.company_id),
                )
                .first()
            )
            if not belongs:
                raise ValueError("User is not assigned to this company")

        project.users = users
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    except IntegrityError:
        db.rollback()
        raise ValueError("Same project already exists for the company")
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error occured: {e}")


# Read the project detail(Single)
def read_project(db: Session, project_id: UUID):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise ValueError("Project doesn't exist")
    return project


# Read the the project detail(Multiple)
def read_projects(db: Session):
    return db.query(Project).all()


# Update the project
def update_project(db: Session, project_id: UUID, data: ProjectUpdate):
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if project is None:
            raise ValueError("Project doesnot exist.")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(project, key, value)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to update the project: {e}")


# Delete the project
def delete_project(db: Session, project_id: UUID):
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if project is None:
            raise ValueError("Project you are trying to delete doesnot exist.")
        db.delete(project)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error occured: {e}")
