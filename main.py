import datetime
from typing import Optional
from manager import TaskManager

def get_int_input(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None, allow_empty: bool = False) -> Optional[int]:
    while True:
        val_str = input(prompt).strip()
        if allow_empty and val_str == "":
            return None 
        try:
            val = int(val_str)
            if min_val is not None and val < min_val:
                print(f"Ошибка: значение должно быть не меньше {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Ошибка: значение должно быть не больше {max_val}.")
                continue
            return val
        except ValueError:
            print("Ошибка: пожалуйста, введите корректное целое число.")

def get_date_input(prompt: str, allow_empty: bool = False) -> Optional[str]:
    """Запрашиваем число и проверяем, чтобы пользователь не ввел буквы"""
    while True:
        date_str = input(prompt).strip()
        if allow_empty and date_str == "":
            return None 
        try:
            datetime.datetime.strptime(date_str, "%d-%m-%Y")
            return date_str
        except ValueError:
            print("Ошибка: неверный формат даты. Используйте формат ДД-ММ-ГГГГ.")

def get_non_empty_string(prompt: str) -> str:
    """Запрашиваем текст и проверяем, чтобы строка не была пустой"""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Ошибка: поле не может быть пустым.")

def main_menu() -> None:
    manager = TaskManager()
    manager.load_from_file()

    while True:
        print("\n" + "="*55)
        print("      СИСТЕМА УПРАВЛЕНИЯ ЗАДАЧАМИ С ПРИОРИТЕТАМИ")
        print("="*55)
        print("1. Добавить новую задачу")
        print("2. Удалить задачу по названию")
        print("3. Изменить параметры задачи")
        print("4. Отменить последнее действие")
        print("5. Добавить задачу в Очередь на исполнение")
        print("6. Выполнить следующую задачу из очереди")
        print("7. Показать задачи по возрастанию дедлайна")
        print("8. Быстрый поиск в дереве: Самый ранние и поздние сроки")
        print("9. Фильтрация задач по приоритету")
        print("10. Сохранить все изменения в файл")
        print("0. Выход из программы")
        print("="*55)
        
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            title = get_non_empty_string("Название задачи: ")
            priority = get_int_input("Приоритет (1 - высокий, 2 - средний, 3 - низкий): ", 1, 3)
            time_exec = get_int_input("Время выполнения (в часах): ", 1)
            deadline = get_date_input("Дедлайн (в формате ДД-ММ-ГГГГ): ")
            manager.add_task(title, priority, time_exec, deadline)

        elif choice == "2":
            title = get_non_empty_string("Введите название задачи для удаления: ")
            manager.delete_task(title)

        elif choice == "3":
            title = get_non_empty_string("Введите название задачи для изменения: ")
            # Находим задачу в списке, чтобы показать ее старые параметры при редактировании
            found_task = next((t for t in manager.tasks if t.title.lower() == title.lower()), None)
            
            if found_task:
                priority = get_int_input(f"Новый приоритет (текущий: {found_task.priority}) [Enter для сохранения]: ", 1, 3, allow_empty=True)
                time_exec = get_int_input(f"Новое время выполнения (текущее: {found_task.execution_time}ч) [Enter для сохранения]: ", 1, allow_empty=True)
                deadline = get_date_input(f"Новый дедлайн (текущий: {found_task.deadline.strftime('%d-%m-%Y')}) [Enter для сохранения]: ", allow_empty=True)
                
                manager.edit_task(title, priority, time_exec, deadline)
            else:
                print("Задача с таким названием не найдена.")

        elif choice == "4":
            manager.undo()

        elif choice == "5":
            title = get_non_empty_string("Введите название задачи для постановки в очередь: ")
            found_task = next((t for t in manager.tasks if t.title.lower() == title.lower()), None)
            if found_task:
                manager.queue.enqueue(found_task)
                print(f"Задача «{found_task.title}» встала в очередь на исполнение.")
            else:
                print("Задача с таким названием не найдена в общем списке.")

        elif choice == "6":
            task = manager.queue.dequeue()
            if task:
                print(f"Выполняется задача: {task}")
                if task in manager.tasks:
                    manager.tasks.remove(task)
            else:
                print("Очередь исполнения пуста.")

        elif choice == "7":
            tree = manager.rebuild_tree()
            sorted_tasks = tree.get_sorted_tasks()
            if not sorted_tasks:
                print("Задач в системе пока нет.")
            else:
                print("\nЗадачи по возрастанию дедлайна (In-order обход BST):")
                for task in sorted_tasks:
                    print(task)

        elif choice == "8":
            tree = manager.rebuild_tree()
            earliest = tree.find_earliest(tree.root)
            latest = tree.find_latest(tree.root)
            
            if earliest:
                print(f"\nСамый ранний дедлайн ({earliest.deadline.strftime('%d-%m-%Y')}):")
                for t in earliest.tasks:
                    print(f"  - {t.title}")
            if latest:
                print(f"\nСамый поздний дедлайн ({latest.deadline.strftime('%d-%m-%Y')}):")
                for t in latest.tasks:
                    print(f"  - {t.title}")
            if not earliest:
                print("Дерево поиска пусто.")

        elif choice == "9":
            p = get_int_input("Введите приоритет для фильтрации (1-3): ", 1, 3)
            filtered = manager.filter_by_priority(p)
            if filtered:
                print(f"\nЗадачи с приоритетом {p}:")
                for t in filtered:
                    print(t)
            else:
                print(f"Задачи с приоритетом {p} не найдены.")

        elif choice == "10":
            manager.save_to_file()

        elif choice == "0":
            manager.save_to_file()
            print("Программа завершена. До встречи!")
            break
        else:
            print("Неверный пункт меню. Попробуйте еще раз.")

if __name__ == "__main__":
    main_menu()
