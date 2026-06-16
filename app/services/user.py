from fastapi import UploadFile
from app.database.models.user import User, Profile
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin, UserRegister
import random
from app.utils.upload_image import upload_image
import string
from app.core.security import create_access, create_refresh, hashPwd, verifyPwd

# To upload the image to cloudinary




# Generate the username
def generate_username(fname: str, db: Session):
    while True:
        prefix = "".join(random.choices(string.digits, k=4))
        base = fname.lower() + prefix
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
    username = generate_username(data.first_name, db)
    password = hashPwd(data.password)
    user = User(username=username, email=data.email, hashed_pwd=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    # If the user has uploaded the image then generate the url and save the image url
    user_image = ""
    if file.filename:
        user_image = upload_image(file,"user", user.id)
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
    isMatched = verifyPwd(userdata.password, exist.hashed_pwd)
    if not isMatched:
        return None, "Invalid credentials"

    return exist, None
