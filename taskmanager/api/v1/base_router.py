from fastapi import APIRouter

# Local router imports
from taskmanager.api.v1.tasks.task_router import task_manager_router

api_router = APIRouter()

# Import v1 routers here
api_router.include_router(task_manager_router, prefix="/tasks", tags=["tasks"])
