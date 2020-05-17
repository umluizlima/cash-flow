from fastapi import FastAPI

from .routers import records_router

api = FastAPI()
api.include_router(records_router, tags=["records"])
