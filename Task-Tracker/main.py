import json
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import os

class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

@dataclass
class Task:
    id: int
    description: str
    status: Status
    created_at: datetime
    updated_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @staticmethod
    def from_dict(data):
        return Task(
            id=data["id"],
            description=data["description"],
            status=Status(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )

class TaskTracker:
    def __init__(self, json_file='tasks.json'):
        self.tasks = []
        self.json_file = json_file
        self.load_tasks()

    def save_tasks(self):
        with open(self.json_file, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def load_tasks(self):
        os.makedirs('Task-Tracker', exist_ok=True)
        self.json_file = os.path.join('Task-Tracker', self.json_file)
        try:
            with open(self.json_file, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task.from_dict(task) for task in tasks_data]
        except FileNotFoundError:
            self.tasks = []

    def add_task(self, description: str):
        task = Task(
            id=len(self.tasks) + 1,
            description=description,
            status=Status.TODO,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.tasks.append(task)
        self.save_tasks()

    def get_tasks(self):
        return self.tasks

    def get_task(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_task_by_status(self, status: Status):
        return [task for task in self.tasks if task.status == status]

    def update_task(self, task_id: int, description: str, status: Status):
        task = self.get_task(task_id)
        if task:
            task.description = description
            task.status = status
            task.updated_at = datetime.now()
            self.save_tasks()
            return task
        return None
    
    def update_task_status(self, task_id: int, status: Status):
        task = self.get_task(task_id)
        if task:
            task.status = status
            task.updated_at = datetime.now()
            self.save_tasks()
            return task
        return None

    def delete_task(self, task_id: int):
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return task
        return None
    

class Main:
    def __init__(self):
        self.task_tracker = TaskTracker()

    def run(self):
        print("Welcome to Task Tracker by Adriel :P")
        print()
        while True:
            
            print("Task Tracker")
            print("1. Add Task")
            print("2. List Tasks")
            print("3. List Tasks by Status")
            print("4. Update Task")
            print("5. Update Task Status")
            print("6. Delete Task")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                description = input("Enter task description: ")
                self.task_tracker.add_task(description)

            elif choice == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                tasks = self.task_tracker.get_tasks()
                for task in tasks:
                    print(task.to_dict())
                print()

            elif choice == '3':
                while True:
                    status_input = input("Enter task status (todo, in-progress, done): ").lower()
                    if status_input in ["todo", "in-progress", "done"]:
                        status = Status(status_input)
                        break
                    else:
                        print("Invalid status. Please enter 'todo', 'in-progress', or 'done'.")
                tasks = self.task_tracker.get_task_by_status(status)
                for task in tasks:
                    print(task.to_dict())
                print()

            elif choice == '4':
                task_id = int(input("Enter task id: "))
                while True:
                    task = self.task_tracker.get_task(task_id)
                    if task:
                        break
                    else:
                        task_id = int(input("Task not found. Please enter a valid task id: "))
                description = input("Enter task description: ")
                status = Status(input("Enter task status (todo, in-progress, done): "))
                task = self.task_tracker.update_task(task_id, description, status)
                if task:
                    print(task.to_dict())
                else:
                    print("Task not found")
                print()

            elif choice == '5':
                task_id = int(input("Enter task id: "))
                while True:
                    task = self.task_tracker.get_task(task_id)
                    if task:
                        break
                    else:
                        task_id = int(input("Task not found. Please enter a valid task id: "))
                while True:
                    status = input("Enter task status (todo, in-progress, done): ")
                    if status in ["todo", "in-progress", "done"]:
                        status = Status(status)
                        break
                    else:
                        print("Invalid status. Please enter 'todo', 'in-progress', or 'done'.")
                task = self.task_tracker.update_task_status(task_id, status)
                print(task.to_dict())
                print()

            elif choice == '6':
                task_id = int(input("Enter task id for delete: "))
                while True:
                    task = self.task_tracker.get_task(task_id)
                    if task:
                        break
                    else:
                        task_id = int(input("Task not found. Please enter a valid task id: "))
                task = self.task_tracker.delete_task(task_id)
                print(task.to_dict())
                print()

            elif choice == '7':
                break
            else:
                print("Invalid choice")
            

if __name__ == "__main__":
    Main().run()