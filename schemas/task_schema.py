from pydantic import BaseModel, ConfigDict, Field

from models.task_model import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., example="Fazer compras")
    description: str = Field(..., example="Comprar leite, pao e ovos")
    owner: str = Field(..., example="Joao")
    status: TaskStatus = Field(default=TaskStatus.PENDENTE, example="pendente")
    comments: list[str] = Field(default_factory=list, example=["Comentario 1", "Comentario 2"])


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


Task = TaskRead
