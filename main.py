from tasks import add_task, complete_task, delete_task, get_tasks, load_tasks


def print_help() -> None:
    """Выводит справку по доступным командам приложения."""
    print("\nДоступные команды:")
    print("  add <предмет>; <название>; <срок> — добавить новое задание")
    print(
        "  list [предмет]                    — показать все задания (или по предмету)"
    )
    print("  done <id>                         — отметить задание выполненным")
    print("  delete <id>                       — удалить задание по его номеру")
    print("  help                              — показать список команд")
    print("  exit                              — завершить работу программы\n")


def print_tasks(tasks: list[dict]) -> None:
    """Выводит отформатированный список заданий в консоль."""
    if not tasks:
        print("Список заданий пуст.")
        return
    print("\nСписок заданий:")
    for task in tasks:
        print(
            f"  [{task['id']}] {task['subject']} | {task['title']} "
            f"(срок: {task['deadline']}) — статус: {task['status']}"
        )
    print()


def handle_add(tasks: list[dict], args_text: str) -> None:
    """Обрабатывает команду добавления задания."""
    parts = [part.strip() for part in args_text.split(";")]
    if len(parts) != 3 or not all(parts):
        print(
            "Ошибка: укажите предмет, название и срок через точку с запятой.\n"
            "Пример: add Информационные технологии; Лабораторная работа № 2; 10.11"
        )
        return
    subject, title, deadline = parts
    task = add_task(tasks, subject, title, deadline)
    print(f"Задание добавлено с ID {task['id']}.")


def handle_done(tasks: list[dict], args_text: str) -> None:
    """Обрабатывает команду отметки задания как выполненного."""
    if not args_text:
        print("Ошибка: укажите числовой ID задания. Пример: done 1")
        return
    try:
        task_id = int(args_text)
    except ValueError:
        print("Ошибка: ID задания должен быть целым числом.")
        return

    if complete_task(tasks, task_id):
        print(f"Задание с ID {task_id} отмечено как выполненное.")
    else:
        print(f"Ошибка: задание с ID {task_id} не найдено.")


def handle_delete(tasks: list[dict], args_text: str) -> None:
    """Обрабатывает команду удаления задания."""
    if not args_text:
        print("Ошибка: укажите числовой ID задания. Пример: delete 1")
        return
    try:
        task_id = int(args_text)
    except ValueError:
        print("Ошибка: ID задания должен быть целым числом.")
        return

    if delete_task(tasks, task_id):
        print(f"Задание с ID {task_id} удалено.")
    else:
        print(f"Ошибка: задание с ID {task_id} не найдено.")


def main() -> None:
    """Точка входа: загружает состояние и запускает цикл обработки команд."""
    tasks = load_tasks()
    print("Помощник по учёбе запущен. Введите 'help' для просмотра команд.")

    while True:
        try:
            user_input = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nРабота программы завершена.")
            break

        if not user_input:
            continue

        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        args_text = parts[1].strip() if len(parts) > 1 else ""

        if command == "exit":
            print("Работа программы завершена.")
            break
        elif command == "help":
            print_help()
        elif command == "add":
            handle_add(tasks, args_text)
        elif command == "list":
            subject_filter = args_text if args_text else None
            filtered_tasks = get_tasks(tasks, subject_filter)
            print_tasks(filtered_tasks)
        elif command == "done":
            handle_done(tasks, args_text)
        elif command == "delete":
            handle_delete(tasks, args_text)
        else:
            print(
                f"Неизвестная команда: '{command}'. "
                "Введите 'help' для списка доступных команд."
            )


if __name__ == "__main__":
    main()
