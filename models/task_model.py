import enum

from sqlalchemy import Column, Integer, JSON
from sqlmodel import Field, SQLModel


class TaskStatus(str, enum.Enum):
    PENDENTE = "pendente"
    FAZENDO = "fazendo"
    CONCLUIDO = "concluido"


class Task(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True),
    )
    title: str
    description: str
    owner: str = Field(index=True)
    status: str = Field(default=TaskStatus.PENDENTE.value, index=True)
    comments: list[str] = Field(default_factory=list, sa_column=Column(JSON))
