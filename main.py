from fastapi import FastAPI

from routes.auth_routes import router as auth_router
from routes.task_routes import router as task_router

app = FastAPI(
    title="Todo API",
    description="API para gerenciamento de tarefas com arquitetura em camadas.",
    version="1.0.0",
    contact={
        "name": "Equipe da disciplina INF8B",
    },
)

app.include_router(auth_router)
app.include_router(task_router)
