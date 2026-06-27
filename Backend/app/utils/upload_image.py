import cloudinary.uploader
from fastapi import UploadFile


def upload_image(file: UploadFile, type: str, type_id: str):
    upload = cloudinary.uploader.upload(
        file.file, folder=f"{type}/{type_id}", public_id=f"{type}", overwrite=True
    )
    return upload["secure_url"]
