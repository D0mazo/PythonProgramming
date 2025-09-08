import json
from typing import List, Optional
from task import Task, Category, TaskStatus

class TaskManager:
    def __init__(self, filename: str = "tasks.json"):
        self.tasks: List[Task] = []
        self.categories: List[Category] = [
            Category("Work", "#FF6B6B"),
            Category("Personal", "#4ECDC4"),
            Category("Urgent", "#45B7D1")
        ]
        self.filename = filename
        self.load_tasks()

    def add_task(self, title: str, description: str, due_date: str, category: Optional[Category] = None) -> Task:
        task = Task(title, description, due_date, category)
        task.id = len(self.tasks) + 1
        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, **kwargs) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            task.update(**kwargs)
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            # Reassign IDs
            for i, t in enumerate(self.tasks, 1):
                t.id = i
            self.save_tasks()
            return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        return self.update_task(task_id, status=TaskStatus.COMPLETED)

    def set_status(self, task_id: int, status: TaskStatus) -> bool:
        return self.update_task(task_id, status=status)

    def get_all_tasks(self, status_filter: Optional[TaskStatus] = None, category_filter: Optional[Category] = None) -> List[Task]:
        filtered = self.tasks
        if status_filter:
            filtered = [t for t in filtered if t.status == status_filter]
        if category_filter:
            filtered = [t for t in filtered if t.category == category_filter]
        return filtered

    def search_tasks(self, query: str) -> List[Task]:
        return [t for t in self.tasks if query.lower() in t.title.lower() or query.lower() in t.description.lower()]

    def save_tasks(self):
        data = {
            "tasks": [t.to_dict() for t in self.tasks],
            "categories": [c.to_dict() for c in self.categories]
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
                self.categories = [Category.from_dict(c) for c in data.get("categories", [])]
        except FileNotFoundError:
            pass  # File doesn't exist yet