from fastapi import FastAPI

from routes.auth_routes import router as auth_router
from routes.task_routes import router as task_router

app = FastAPI(title="INFO8 API")

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
async def root():
    return {"message": "INFO8 API"}
