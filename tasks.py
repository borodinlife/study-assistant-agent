def add_task(tasks: list[dict], subject: str, title: str, deadline: str) -> dict:
    """Добавляет новое учебное задание в список."""
    new_id = 1 if not tasks else max(task["id"] for task in tasks) + 1
    task = {
        "id": new_id,
        "subject": subject,
        "title": title,
        "deadline": deadline,
        "status": "активно",
    }
    tasks.append(task)
    return task


def get_tasks(tasks: list[dict], subject: str | None = None) -> list[dict]:
    """Возвращает все задания или фильтрует их по названию предмета."""
    if subject is None:
        return list(tasks)
    return [task for task in tasks if task["subject"].lower() == subject.lower()]


def complete_task(tasks: list[dict], task_id: int) -> bool:
    """Переводит задание в статус 'выполнено' по его ID."""
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "выполнено"
            return True
    return False


def delete_task(tasks: list[dict], task_id: int) -> bool:
    """Удаляет задание из списка по его ID."""
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return True
    return False
