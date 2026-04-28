import json
class TaskController:
    def __init__(self, task_id,):
        self.id = task_id

    async def get_tasks(self, owner: str | None = None, 
                        status: str | None = None, 
                        skip: int = 0, 
                        limit: int | None = None):
        dados = await self.ler_arquivo_json()
        tasks_list = dados["tasks"]

        filtered_tasks = [
            task for task in tasks_list
            if (owner is None or owner.lower() in task["owner"].lower())
            and (status is None or status.lower() in task["status"].lower())
        ]

        if limit is None:
            return filtered_tasks[skip:]
        return filtered_tasks[skip:skip + limit]
    



    async def ler_arquivo_json():
        with open("tasks.json", encoding="utf-8") as f:
            dados = json.load(f)
        return dados