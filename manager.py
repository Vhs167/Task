import json
import datetime
from typing import List, Optional, Tuple
from models import Task
from structures import TaskQueue, UndoStack, BinarySearchTree

class TaskManager:
    """Главный класс менеджера, который связывает все структуры вместе"""
    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self.queue: TaskQueue = TaskQueue()
        self.undo_stack: UndoStack = UndoStack()

    def rebuild_tree(self) -> BinarySearchTree:
        """Собираем дерево заново из текущего списка всех задач"""
        tree = BinarySearchTree()
        for task in self.tasks:
            tree.insert(task)
        return tree

    def add_task(self, title: str, priority: int, execution_time: int, deadline: str, track_undo: bool = True) -> None:
        try:
            task = Task(title, priority, execution_time, deadline)
            self.tasks.append(task)
            if track_undo:
                self.undo_stack.push_action('add', task)
            print(f"Задача успешно добавлена: {task.title}")
        except ValueError:
            print("Ошибка: Неверный формат даты. Используйте ДД-ММ-ГГГГ.")

    def delete_task(self, title: str) -> None:
        for task in self.tasks:
            if task.title.lower() == title.lower():
                self.tasks.remove(task)
                self.undo_stack.push_action('delete', task)
                print(f"Задача «{task.title}» удалена из системы.")
                return
        print("Задача с таким названием не найдена.")

    def edit_task(self, title: str, new_priority: Optional[int], new_time: Optional[int], new_deadline: Optional[str]) -> None:
        for task in self.tasks:
            if task.title.lower() == title.lower():
                # Создаем копию старого состояния задачи для отмены (Undo)
                old_copy = Task(task.title, task.priority, task.execution_time, task.deadline.strftime("%d-%m-%Y"))
                
                # Проверяем приоритет
                if new_priority is not None:
                    task.priority = new_priority
                else:
                    print(f"Приоритет оставлен прежним: {task.priority}")
                
                # Проверяем время выполнения
                if new_time is not None:
                    task.execution_time = new_time
                else:
                    print(f"Время выполнения оставлено прежним: {task.execution_time}ч")
                
                # Проверяем дедлайн
                if new_deadline is not None:
                    task.deadline = datetime.datetime.strptime(new_deadline, "%d-%m-%Y").date()
                else:
                    print(f"Дедлайн оставлен прежним: {task.deadline.strftime('%d-%m-%Y')}")
                
                # Кладем старую и новую версию в стек для возможного отката
                self.undo_stack.push_action('edit', (old_copy, task))
                print(f"Задача «{task.title}» успешно изменена.")
                return
        print("Задача с таким названием не найдена.")

    def undo(self) -> None:
        """Логика отмены последнего действия через стек"""
        action = self.undo_stack.pop_action()
        if not action:
            print("Нет действий для отмены.")
            return

        action_type, data = action
        if action_type == 'add':
            self.tasks.remove(data)
            print(f"Отменено добавление задачи: {data.title}")
        elif action_type == 'delete':
            self.tasks.append(data)
            print(f"Восстановлена удаленная задача: {data.title}")
        elif action_type == 'edit':
            old_task, current_task = data
            current_task.priority = old_task.priority
            current_task.execution_time = old_task.execution_time
            current_task.deadline = old_task.deadline
            print(f"Изменения задачи «{current_task.title}» отменены.")

    def filter_by_priority(self, priority: int) -> List[Task]:
        """Фильтрация по приоритету"""
        return [t for t in self.tasks if t.priority == priority]

    def save_to_file(self, filename: str = "tasks.json") -> None:
        """Сохранение данных в json"""
        data = {
            "tasks": [t.to_dict() for t in self.tasks],
            "queue": [t.to_dict() for t in self.queue.get_all()]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Данные сохранены в файл tasks.json.")

    def load_from_file(self, filename: str = "tasks.json") -> None:
        """Загрузка данных из json"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
                self.queue = TaskQueue()
                for t in data.get("queue", []):
                    self.queue.enqueue(Task.from_dict(t))
            print("Данные успешно загружены из файла tasks.json.")
        except FileNotFoundError:
            print("Файл сохранения не найден. Начнем с чистого листа.")
