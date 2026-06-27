import random
import string

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.security import hashPwd, verifyPwd
from app.database.models.user import Profile, User
from app.schemas.user import UserLogin, UserRegister
from app.utils.upload_image import upload_image

# To upload the image to cloudinary


# Generate the username
def generate_username(fullname: str, db: Session):
    while True:
        prefix = "".join(random.choices(string.digits, k=4))
        base = "".join(fullname.split()).lower() + prefix
        user = db.query(User).filter(User.username == base).first()
        if not user:
            return base


# Create the user
def create_user(data: UserRegister, file: UploadFile | None, db: Session):
    # Check the email is not in database or not
    exist = db.query(User).filter(User.email == data.email).first()
    if exist:
        return None, "Email already exists"
    # Generate the username for the new user
    username = generate_username(f"{data.first_name} {data.last_name}", db)
    password = hashPwd(data.password)
    user = User(username=username, email=data.email, hashed_pwd=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    # If the user has uploaded the image then generate the url and save the image url
    user_image = ""
    if file is not None and file.filename:
        user_image = upload_image(file, "user", str(user.id))
    # Make the profile for the user
    profile = Profile(
        user_id=user.id,
        full_name=f"{data.first_name} {data.last_name}",
        user_image=user_image,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return user, None


def verify_credentials(userdata: UserLogin, db: Session):
    exist = db.query(User).filter(User.email == userdata.email).first()
    if not exist:
        return None, "User doesn't exist with this email"
    # Verify the password
    isMatched = verifyPwd(userdata.password, str(exist.hashed_pwd))
    if not isMatched:
        return None, "Invalid credentials"

    return exist, None
