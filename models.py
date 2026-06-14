import datetime
from typing import Dict, Any

class Task:
    def __init__(self, title: str, priority: int, execution_time: int, deadline: str) -> None:
        self.title: str = title
        self.priority: int = priority
        self.execution_time: int = execution_time
        # Переводим строку в тип даты, чтобы потом было проще сравнивать дедлайны в дереве
        self.deadline: datetime.date = datetime.datetime.strptime(deadline, "%d-%m-%Y").date()

    def to_dict(self) -> Dict[str, Any]:
        """Переводим данные задачи в словарь, чтобы их можно было записать в файл"""
        return {
            "title": self.title,
            "priority": self.priority,
            "execution_time": self.execution_time,
            "deadline": self.deadline.strftime("%d-%m-%Y")
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Восстанавливаем объект задачи из словаря, который прочитали из файла"""
        return cls(data["title"], data["priority"], data["execution_time"], data["deadline"])

    def __str__(self) -> str:
        return f"«{self.title}» | Приоритет: {self.priority} | Время: {self.execution_time}ч | Дедлайн: {self.deadline.strftime('%d-%m-%Y')}"
