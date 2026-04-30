from controllers.task_controller import TaskController
from fastapi import APIRouter, Depends, status
from schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
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

@router.get("/{id}", response_model=TaskResponse)
async def tasks_id(id: int):
    return await TaskController.get_tasks_by_id(id)

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    return await TaskController.create_task(task)

@router.put("/{id}", response_model=TaskResponse)
async def update_task(id: int, task: TaskUpdate):
    return await TaskController.update_task(id, task)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    await TaskController.delete_task(id)
