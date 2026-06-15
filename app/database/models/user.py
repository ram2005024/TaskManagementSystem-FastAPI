from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database.db import Base
from sqlalchemy.orm import relationship


# Make a user model
class User(Base):
    __tablename__ = "users"

    # Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_pwd = Column(String)
    is_authenticated = Column(Boolean, default=False)
    profile = relationship("Profile", back_populates="user", uselist=False)


# Make a profile model for the user
class Profile(Base):
    __tablename__ = "profiles"
    # Fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    bio = Column(String, nullable=True)
    user_image = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="profile")
