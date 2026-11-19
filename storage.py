import json
from pathlib import Path

DEFAULT_STORAGE_PATH = Path("tasks.json")


class StorageError(Exception):
    """Ошибка при чтении или записи файла хранилища."""


def load_storage(path: Path = DEFAULT_STORAGE_PATH) -> list[dict]:
    """Загружает список заданий из JSON-файла.

    При первом запуске (если файл отсутствует) возвращает пустой список.
    При повреждении файла или ошибке чтения выбрасывает StorageError.
    """
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        raise StorageError(f"Не удалось прочитать файл хранилища: {error}") from error

    if not isinstance(data, list):
        raise StorageError("Некорректный формат данных в файле хранилища.")
    return data


def save_storage(data: list[dict], path: Path = DEFAULT_STORAGE_PATH) -> None:
    """Сохраняет список заданий в JSON-файл."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise StorageError(f"Не удалось сохранить файл хранилища: {error}") from error
