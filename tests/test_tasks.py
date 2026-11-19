import pytest

from tasks import add_task, complete_task, delete_task, get_tasks


@pytest.fixture
def sample_tasks() -> list[dict]:
    """Возвращает изолированный тестовый список заданий."""
    return [
        {
            "id": 1,
            "subject": "Информационные технологии",
            "title": "ЛР 3",
            "deadline": "20.11",
            "status": "активно",
        },
        {
            "id": 2,
            "subject": "Физика",
            "title": "Типовой расчёт",
            "deadline": "25.11",
            "status": "активно",
        },
    ]


def test_add_task_to_empty_list():
    tasks = []
    created = add_task(tasks, "ОС", "ЛР 4", "28.11")

    assert len(tasks) == 1
    assert created["id"] == 1
    assert created["subject"] == "ОС"
    assert created["status"] == "активно"


def test_add_task_increments_id(sample_tasks):
    created = add_task(sample_tasks, "ОС", "ЛР 4", "28.11")

    assert len(sample_tasks) == 3
    assert created["id"] == 3


def test_get_tasks_all_and_filtered(sample_tasks):
    assert len(get_tasks(sample_tasks)) == 2

    physics_tasks = get_tasks(sample_tasks, "физика")
    assert len(physics_tasks) == 1
    assert physics_tasks[0]["title"] == "Типовой расчёт"

    assert get_tasks(sample_tasks, "История") == []


def test_complete_task_changes_status(sample_tasks):
    result = complete_task(sample_tasks, 1)

    assert result is True
    assert sample_tasks[0]["status"] == "выполнено"
    assert sample_tasks[1]["status"] == "активно"


@pytest.mark.parametrize("invalid_id", [0, -1, 99])
def test_complete_task_invalid_id(sample_tasks, invalid_id):
    assert complete_task(sample_tasks, invalid_id) is False
    assert all(task["status"] == "активно" for task in sample_tasks)


def test_delete_task_removes_item(sample_tasks):
    result = delete_task(sample_tasks, 1)

    assert result is True
    assert len(sample_tasks) == 1
    assert sample_tasks[0]["id"] == 2


@pytest.mark.parametrize("invalid_id", [0, -1, 99])
def test_delete_task_invalid_id(sample_tasks, invalid_id):
    assert delete_task(sample_tasks, invalid_id) is False
    assert len(sample_tasks) == 2
