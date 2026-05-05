from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
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
                skip: int = 0, limit: int | None = None,
                session: Session = Depends(get_session)):
    return await TaskController.get_tasks(session, owner, status, skip, limit)

@router.get("/{id}")
async def tasks_id(id: int, session: Session = Depends(get_session)):
    return await TaskController.get_tasks_by_id(session, id)

@router.post("/")
async def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    return await TaskController.create_task(session, task)

@router.delete("/{id}")
async def delete_task(id: int, session: Session = Depends(get_session)):
    return await TaskController.delete_task(session, id)

@router.put("/{id}")
async def update_task(id: int, task: TaskUpdate, session: Session = Depends(get_session)):
    return await TaskController.update_task(session, id, task)
