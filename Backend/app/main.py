from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import app.schemas.rebuild
from app.core.config import settings
from app.routers.auth import authRouter
from app.routers.company import company_router
from app.routers.projects import projectRouter
from app.routers.task import task_router

from .core.middleware import blacklist_middleware

app = FastAPI()
# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(authRouter)
app.include_router(company_router)
app.include_router(projectRouter)
app.include_router(task_router)
app.middleware("http")(blacklist_middleware)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.get("/")
def default():
    return {"message": "Hello World I am into the world of fastapi"}
