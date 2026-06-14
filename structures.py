import datetime
from typing import List, Optional, Tuple, Any
from models import Task

class TaskQueue:
    """Очередь для задач. Работает по принципу FIFO: первым пришел - первым ушел"""
    def __init__(self) -> None:
        self.queue: List[Task] = []

    def enqueue(self, task: Task) -> None:
        """Добавляем задачу в самый конец списка (очереди)"""
        self.queue.append(task)

    def dequeue(self) -> Optional[Task]:
        """Берем первую задачу из очереди и удаляем ее"""
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def get_all(self) -> List[Task]:
        return self.queue


class UndoStack:
    """Стек для функции отмены. Принцип LIFO: последнее действие отменяется первым"""
    def __init__(self) -> None:
        self.stack: List[Tuple[str, Any]] = []

    def push_action(self, action_type: str, task_data: Any) -> None:
        """Записываем, какую именно операцию мы реализовали"""
        self.stack.append((action_type, task_data))

    def pop_action(self) -> Optional[Tuple[str, Any]]:
        """Извлекаем последнее действие для отмены"""
        if not self.is_empty():
            return self.stack.pop()
        return None

    def is_empty(self) -> bool:
        return len(self.stack) == 0


class BSTNode:
    """Класс узла для бинарного дерева"""
    def __init__(self, deadline: datetime.date) -> None:
        self.deadline: datetime.date = deadline
        self.tasks: List[Task] = []  # Список задач с одинаковым дедлайном
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None


class BinarySearchTree:
    """Бинарное дерево которое сортирует задачи по дедлайнам"""
    def __init__(self) -> None:
        self.root: Optional[BSTNode] = None

    def insert(self, task: Task) -> None:
        """Публичный метод для вставки задачи"""
        self.root = self._insert_recursive(self.root, task)

    def _insert_recursive(self, node: Optional[BSTNode], task: Task) -> BSTNode:
        """Внутренний рекурсивный метод вставки"""
        if node is None:
            new_node = BSTNode(task.deadline)
            new_node.tasks.append(task)
            return new_node

        if task.deadline == node.deadline:
            node.tasks.append(task)
        elif task.deadline < node.deadline:
            node.left = self._insert_recursive(node.left, task)
        else:
            node.right = self._insert_recursive(node.right, task)
        return node

    def get_sorted_tasks(self) -> List[Task]:
        """Собираем все задачи в один список, отсортированный по датам"""
        sorted_list: List[Task] = []
        self._inorder_recursive(self.root, sorted_list)
        return sorted_list

    def _inorder_recursive(self, node: Optional[BSTNode], sorted_list: List[Task]) -> None:
        """Симметричный обход дерева"""
        if node is not None:
            self._inorder_recursive(node.left, sorted_list)
            sorted_list.extend(node.tasks)
            self._inorder_recursive(node.right, sorted_list)

    def find_earliest(self, node: Optional[BSTNode]) -> Optional[BSTNode]:
        """Поиск самого раннего срока (крайний левый узел)"""
        current = node
        if current is None:
            return None
        while current.left is not None:
            current = current.left
        return current

    def find_latest(self, node: Optional[BSTNode]) -> Optional[BSTNode]:
        """Поиск самого позднего срока (крайний правый узел)"""
        current = node
        if current is None:
            return None
        while current.right is not None:
            current = current.right
        return current
