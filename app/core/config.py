from pydantic_settings import SettingsConfigDict, BaseSettings
import cloudinary
import redis


class Settings(BaseSettings):
    DATABASE_URL: str
    CLOUD_NAME: str
    CLOUD_KEY: int
    CLOUD_SECRET: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_EXPIRY: int
    REFRESH_EXPIRY: int
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
