import json
import os

DATA_FILE = "tasks.json"


def load_tasks() -> list[dict]:
    """Загружает список заданий из JSON-файла."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks: list[dict]) -> None:
    """Сохраняет список заданий в JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


def add_task(tasks: list[dict], subject: str, title: str, deadline: str) -> dict:
    """Добавляет новое учебное задание и сохраняет состояние."""
    new_id = 1 if not tasks else max(task["id"] for task in tasks) + 1
    task = {
        "id": new_id,
        "subject": subject,
        "title": title,
        "deadline": deadline,
        "status": "активно",
    }
    tasks.append(task)
    save_tasks(tasks)
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
            save_tasks(tasks)
            return True
    return False


def delete_task(tasks: list[dict], task_id: int) -> bool:
    """Удаляет задание из списка по его ID."""
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            save_tasks(tasks)
            return True
    return False
