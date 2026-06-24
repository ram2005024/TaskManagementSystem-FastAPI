import cloudinary
import redis
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    CLOUD_NAME: str
    CLOUD_KEY: int
    CLOUD_SECRET: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_EXPIRY: int
    REFRESH_EXPIRY: int
    CLIENT_ID_GOOGLE:str
    CLIENT_SECRET_GOOGLE:str
    CLIENT_ID_FACEBOOK:int
    CLIENT_SECRET_FACEBOOK:str
    SERVER_METADATA_URL:str
    AUTHORIZE_URL_FACEBOOK:str
    ACCESS_TOKEN_URL_FACEBOOK:str
    API_BASE_URL_FACEBOOK:str
    REDIRECT_URL_FACEBOOK:str
    REDIRECT_URL_GOOGLE:str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# Cloudinary Setting
cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.CLOUD_KEY,
    api_secret=settings.CLOUD_SECRET,
)

# Redis settings
redis = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
