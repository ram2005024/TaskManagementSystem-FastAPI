from authlib.integrations.starlette_client import OAuth
from .config import settings
oauth=OAuth()

# Register google oauth
oauth.register(
    name="google",
    client_id=settings.CLIENT_ID_GOOGLE,
    client_secret=settings.CLIENT_SECRET_GOOGLE,
    server_metadata_url=settings.SERVER_METADATA_URL,
    client_kwargs={"scope":"openid email profile"}
)

# Register Facebook oauth
oauth.register(
    name="facebook",
    client_id=settings.CLIENT_ID_FACEBOOK,
    client_secret=settings.CLIENT_SECRET_FACEBOOK,
    authorize_url=settings.AUTHORIZE_URL_FACEBOOK,
    access_token_url=settings.ACCESS_TOKEN_URL_FACEBOOK,
    api_base_url=settings.API_BASE_URL_FACEBOOK,
    client_kwargs={"scope":"email public_profile"}
)