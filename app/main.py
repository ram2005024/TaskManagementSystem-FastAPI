from fastapi import FastAPI
import app.schemas.rebuild
from app.routers.company import company_router
from app.routers.auth import authRouter
from .core.security import blacklist_middleware
app = FastAPI()
app.include_router(authRouter)
app.include_router(company_router)
app.middleware("http")(blacklist_middleware)


@app.get("/")
def default():
    return {"message": "Hello World I am into the world of fastapi"}
