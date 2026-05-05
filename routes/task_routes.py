from fastapi import APIRouter, Depends

from controllers.task_controller import TaskController
from schemas.task_schema import TaskCreate, TaskUpdate
from services.auth_service import get_current_active_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_active_user)],
)

@router.get("/")
async def tasks(owner: str | None = None, 
                status: str | None = None, 
                skip: int = 0, limit: int | None = None):
    return await TaskController.get_tasks(owner, status, skip, limit)

@router.get("/{id}")
async def tasks_id(id: int):
    return await TaskController.get_tasks_by_id(id)

@router.post("/")
async def create_task(task: TaskCreate):
    return await TaskController.create_task(task)

@router.delete("/{id}")
async def delete_task(id: int):
    return await TaskController.delete_task(id)

@router.put("/{id}")
async def update_task(id: int, task: TaskUpdate):
    return await TaskController.update_task(id, task)
