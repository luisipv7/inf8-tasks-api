from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routes.auth_routes import router as auth_router
from routes.task_routes import router as task_router
from database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # inicializar recursos na inicialização da aplicação
    create_db_and_tables()
    yield


app = FastAPI(
    title="Todo API",
    description="API para gerenciamento de tarefas com arquitetura em camadas.",
    version="1.0.0",
    contact={
        "name": "Equipe da disciplina INF8B",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(task_router)
