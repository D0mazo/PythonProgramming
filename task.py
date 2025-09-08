from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class Category:
    def __init__(self, name: str, color: str = "#FFFFFF"):
        self.name = name
        self.color = color  # Hex color for GUI

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"name": self.name, "color": self.color}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["name"], data["color"])

class Task:
    def __init__(self, title: str, description: str, due_date: str, category: Optional[Category] = None):
        self.id = None  # Will be set by manager
        self.title = title
        self.description = description
        self.due_date = due_date
        self.category = category
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at

    def __str__(self):
        status = self.status.value
        cat = f" | Category: {self.category}" if self.category else ""
        return f"[{status}] {self.title} | Due: {self.due_date}{cat} | Created: {self.created_at}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "category": self.category.to_dict() if self.category else None,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        task = cls(data["title"], data["description"], data["due_date"])
        task.id = data["id"]
        task.status = TaskStatus(data["status"])
        task.created_at = data["created_at"]
        task.updated_at = data["updated_at"]
        if data["category"]:
            task.category = Category.from_dict(data["category"])
        return task

    def update(self, title: Optional[str] = None, description: Optional[str] = None,
               due_date: Optional[str] = None, category: Optional[Category] = None):
        if title:
            self.title = title
        if description:
            self.description = description
        if due_date:
            self.due_date = due_date
        if category:
            self.category = category
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")