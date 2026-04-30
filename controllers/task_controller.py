import json
from fastapi import HTTPException
from schemas.task_schema import TaskCreate, TaskUpdate


class TaskController:
    @staticmethod
    async def get_tasks(owner: str | None = None,
                        status: str | None = None,
                        skip: int = 0,
                        limit: int | None = None):
        dados = await TaskController.ler_arquivo_json()
        tasks_list = dados["tasks"]

        filtered_tasks = [
            task for task in tasks_list
            if (owner is None or owner.lower() in task["owner"].lower())
            and (status is None or status.lower() in task["status"].lower())
        ]

        if limit is None:
            return filtered_tasks[skip:]
        return filtered_tasks[skip:skip + limit]

    @staticmethod
    async def get_tasks_by_id(id: int):
        responseTasks = await TaskController.ler_arquivo_json()
        tasks_list = responseTasks["tasks"]
        task = next((item for item in tasks_list if item["id"] == id), None)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    @staticmethod
    async def create_task(task: TaskCreate):
        tasks = await TaskController.ler_arquivo_json()
        last_id = tasks["tasks"][-1]["id"] if tasks["tasks"] else 0
        new_task = task.model_dump()
        new_task["id"] = last_id + 1
        tasks["tasks"].append(new_task)
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
        return new_task

    @staticmethod
    async def update_task(id: int, task: TaskUpdate):
        tasks_data = await TaskController.ler_arquivo_json()
        tasks_list = tasks_data["tasks"]
        index = next((i for i, item in enumerate(tasks_list) if item["id"] == id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Task not found")
        updated = tasks_list[index] | task.model_dump(exclude_unset=True)
        updated["id"] = id
        tasks_list[index] = updated
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=4)
        return updated

    @staticmethod
    async def delete_task(id: int):
        tasks_list = await TaskController.ler_arquivo_json()
        task_exists = any(item["id"] == id for item in tasks_list["tasks"])
        if not task_exists:
            raise HTTPException(status_code=404, detail="Task not found")
        tasks_list["tasks"] = [item for item in tasks_list["tasks"] if item["id"] != id]
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks_list, f, ensure_ascii=False, indent=4)
        return {"message": "Task deletada com sucesso"}

    @staticmethod
    async def ler_arquivo_json():
        with open("tasks.json", encoding="utf-8") as f:
            dados = json.load(f)
        return dados
