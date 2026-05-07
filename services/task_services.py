import json
from pathlib import Path
from fastapi import HTTPException
from sqlmodel import Session, select

from models.task_model import Task

try:
    from ..schemas.task_schema import TaskCreate, TaskUpdate
except ImportError:
    from schemas.task_schema import TaskCreate, TaskUpdate


TASKS_FILE = Path(__file__).resolve().parents[1] / "tasks.json"

class TaskServices:
    @staticmethod
    async def get_tasks(session: Session,
                        owner: str | None = None,
                        status: str | None = None,
                        skip: int = 0,
                        limit: int | None = None):
        declaracao = select(Task)
        if owner is not None:
            declaracao = declaracao.where(Task.owner.contains(owner))
        if status is not None:
            declaracao = declaracao.where(Task.status == status.lower())

        declaracao = declaracao.offset(skip)
        if limit is not None:
            declaracao = declaracao.limit(limit)

        return session.exec(declaracao).all()

    @staticmethod
    async def get_tasks_by_id(id: int):
        response_tasks = await TaskServices.ler_arquivo_json()
        tasks_list = response_tasks["tasks"]
        task = next((item for item in tasks_list if item["id"] == id), None)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    @staticmethod
    async def create_task(task: TaskCreate):
        tasks = await TaskServices.ler_arquivo_json()
        last_id = tasks["tasks"][-1]["id"] if tasks["tasks"] else 0
        new_task = task.model_dump()
        new_task["id"] = last_id + 1
        tasks["tasks"].append(new_task)
        with TASKS_FILE.open("w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
        return new_task

    @staticmethod
    async def delete_task(id: int):
        tasks_data = await TaskServices.ler_arquivo_json()
        task_exists = any(item["id"] == id for item in tasks_data["tasks"])
        if not task_exists:
            raise HTTPException(status_code=404, detail="Task not found")
        tasks_data["tasks"] = [item for item in tasks_data["tasks"] if item["id"] != id]
        with TASKS_FILE.open("w", encoding="utf-8") as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=4)
        return {"message": "Task deletada com sucesso"}

    @staticmethod
    async def update_task(id: int, task: TaskUpdate):
        tasks_data = await TaskServices.ler_arquivo_json()
        tasks_list = tasks_data["tasks"]
        index = next((i for i, item in enumerate(tasks_list) if item["id"] == id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Task not found")
        updated = task.model_dump()
        updated["id"] = id
        tasks_list[index] = updated
        with TASKS_FILE.open("w", encoding="utf-8") as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=4)
        return updated
    
    @staticmethod
    async def ler_arquivo_json():
        with TASKS_FILE.open(encoding="utf-8") as f:
            dados = json.load(f)
        return dados