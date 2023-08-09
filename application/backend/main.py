from fastapi import FastAPI

from database.base import Base
from database.db import engine
from router.router import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
