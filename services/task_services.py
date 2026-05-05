from fastapi import HTTPException
from sqlmodel import Session, select

from models.task_model import Task
from schemas.task_schema import TaskCreate, TaskUpdate


class TaskServices:
    @staticmethod
    async def get_tasks(
        session: Session,
        owner: str | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int | None = None,
    ):
        statement = select(Task)
        if owner is not None:
            statement = statement.where(Task.owner.contains(owner))
        if status is not None:
            statement = statement.where(Task.status == status.lower())

        statement = statement.offset(skip)
        if limit is not None:
            statement = statement.limit(limit)

        return session.exec(statement).all()

    @staticmethod
    async def get_tasks_by_id(session: Session, id: int):
        task = session.get(Task, id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    @staticmethod
    async def create_task(session: Session, task: TaskCreate):
        new_task = Task(**task.model_dump(mode="json"))
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task

    @staticmethod
    async def delete_task(session: Session, id: int):
        task = session.get(Task, id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(task)
        session.commit()
        return {"message": "Task deletada com sucesso"}

    @staticmethod
    async def update_task(session: Session, id: int, task: TaskUpdate):
        db_task = session.get(Task, id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        task_data = task.model_dump(mode="json")
        for field, value in task_data.items():
            setattr(db_task, field, value)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
