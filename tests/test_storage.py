import pytest

from storage import StorageError, load_storage, save_storage


def test_load_storage_first_run_returns_empty_list(tmp_path):
    """При первом запуске (файла нет) возвращается пустой список."""
    storage_file = tmp_path / "tasks.json"
    assert not storage_file.exists()
    assert load_storage(storage_file) == []


def test_save_and_load_storage(tmp_path):
    """Сохранённые задания корректно восстанавливаются после чтения с диска."""
    storage_file = tmp_path / "data" / "tasks.json"
    sample_data = [
        {
            "id": 1,
            "subject": "Информационные технологии",
            "title": "Лабораторная работа № 3",
            "deadline": "20.11",
            "status": "активно",
        }
    ]

    save_storage(sample_data, storage_file)
    assert storage_file.exists()

    loaded_data = load_storage(storage_file)
    assert loaded_data == sample_data


def test_load_storage_corrupted_json_raises_error(tmp_path):
    """Повреждённый JSON вызывает StorageError."""
    storage_file = tmp_path / "broken.json"
    storage_file.write_text("{некорректный json", encoding="utf-8")

    with pytest.raises(StorageError):
        load_storage(storage_file)


def test_load_storage_wrong_root_type_raises_error(tmp_path):
    """Если в файле не список, а словарь, выбрасывается StorageError."""
    storage_file = tmp_path / "wrong_type.json"
    storage_file.write_text('{"id": 1}', encoding="utf-8")

    with pytest.raises(StorageError):
        load_storage(storage_file)


def test_save_storage_os_error_raises_storage_error(tmp_path):
    """Попытка записать данные в путь-каталог вызывает StorageError."""
    with pytest.raises(StorageError):
        save_storage([], tmp_path)
