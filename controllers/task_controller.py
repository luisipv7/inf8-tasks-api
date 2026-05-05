import os
from dotenv import load_dotenv
from sqlmodel import Session

from schemas.task_schema import TaskCreate, TaskUpdate
from services.task_services import TaskServices

load_dotenv()


def _validate_positive_int(name: str, value: int):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} deve ser um inteiro positivo")


def _validate_non_negative_int(name: str, value: int):
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} deve ser um inteiro não negativo")


def _validate_optional_str(name: str, value: str | None, max_len: int = 255):
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} deve ser uma string não vazia")
    if len(value) > max_len:
        raise ValueError(f"{name} é muito longa (máx. {max_len} caracteres)")


def _validate_status(name: str, value: str | None):
    """Valida status opcional entre os permitidos em TASK_ALLOWED_STATUSES."""
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} deve ser uma string não vazia")
    raw = os.getenv('TASK_ALLOWED_STATUSES')
    allowed = {s.strip().lower() for s in raw.split(',') if s.strip()} if raw else set()
    if not allowed:
        raise ValueError("TASK_ALLOWED_STATUSES deve ser configurada no arquivo .env")
    val = value.strip().lower()
    if val not in allowed:
        allowed_list = ", ".join(sorted(allowed))
        raise ValueError(f"{name} inválido. Valores permitidos: {allowed_list}")


def _validate_task_model(name: str, value, expected_cls):
    # Expecting a Pydantic model instance (TaskCreate/TaskUpdate)
    if not isinstance(value, expected_cls):
        raise TypeError(f"{name} deve ser do tipo {expected_cls.__name__}")
    
class TaskController:
    @staticmethod
    async def get_tasks(
        session: Session,
        owner: str | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int | None = None,
    ):
        _validate_optional_str('owner', owner)
        _validate_status('status', status)
        _validate_non_negative_int('skip', skip)
        if limit is not None:
            _validate_positive_int('limit', limit)
        return await TaskServices.get_tasks(session, owner, status, skip, limit)

    @staticmethod
    async def get_tasks_by_id(session: Session, id: int):
        _validate_positive_int('id', id)
        return await TaskServices.get_tasks_by_id(session, id)

    @staticmethod
    async def create_task(session: Session, task: TaskCreate):
        _validate_task_model('task', task, TaskCreate)
        return await TaskServices.create_task(session, task)

    @staticmethod
    async def delete_task(session: Session, id: int):
        _validate_positive_int('id', id)
        return await TaskServices.delete_task(session, id)

    @staticmethod
    async def update_task(session: Session, id: int, task: TaskUpdate):
        _validate_positive_int('id', id)
        _validate_task_model('task', task, TaskUpdate)
        return await TaskServices.update_task(session, id, task)
