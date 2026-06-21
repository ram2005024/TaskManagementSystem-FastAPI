from fastapi import FastAPI

import app.schemas.rebuild
from app.routers.auth import authRouter
from app.routers.company import company_router
from app.routers.projects import projectRouter
from app.routers.task import task_router

from .core.security import blacklist_middleware

app = FastAPI()
app.include_router(authRouter)
app.include_router(company_router)
app.include_router(projectRouter)
app.include_router(task_router)
app.middleware("http")(blacklist_middleware)


@app.get("/")
def default():
    return {"message": "Hello World I am into the world of fastapi"}
