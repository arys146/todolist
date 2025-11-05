from fastapi import FastAPI, APIRouter
from .users import user_routes
from .tasks import task_routes
from .tags import tag_routes
from .habbit import habbit_routes
from .list import list_routes

def setup_routes(api : FastAPI):
    api.include_router(user_routes())
    api.include_router(task_routes())
    api.include_router(tag_routes())
    api.include_router(habbit_routes())
    api.include_router(list_routes())
    