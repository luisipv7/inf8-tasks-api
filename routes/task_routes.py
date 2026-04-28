from controllers.task_controller import TaskController
from fastapi import APIRouter
from schemas.task_schema import TaskCreate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router.get("/")
async def tasks(owner: str | None = None, 
                status: str | None = None, 
                skip: int = 0, limit: int | None = None):
    return TaskController.get_tasks(owner, status, skip, limit)

@router.get("/tasks/{id}")
async def tasks_id(id: int):
    return TaskController.get_tasks_by_id(id)

@router.post("/tasks")
async def create_task(task: TaskCreate):
    return TaskController.create_task(task)