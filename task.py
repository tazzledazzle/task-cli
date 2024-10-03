import json
import os.path
from datetime import datetime
from enum import Enum

TASKS_FILE = 'tasks.json'

class Status(Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    done = 'done'


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    else:
        return load_json_tasks(TASKS_FILE)


def create_task_list_from_json(data):
    tasks = []
    for task in data:
        tasks.append(Task(task.id, task.description, created_at=task.createdAt, status=task.status, updated_at= task.updatedAt))
    return tasks


def add_task(description):
    tasks = load_tasks()
    tasks.append(
        Task(generate_task_id(tasks), description)
    )
    save_tasks(tasks)



def load_json_tasks(TASKS_FILE):
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return create_task_list_from_json(json.load(f))
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)


def find_task_by_id(id):
    tasks = load_json_tasks(TASKS_FILE)
    for task in tasks:
        if task['id'] == id:
            return task


def generate_task_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1


def update_task(task_id, updated_desc):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = updated_desc
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated.")
            return
    print(f"Task {task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted.")


def update_task_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated with status: {status}.")
            return
    print(f"Task {task_id} not found.")


def mark_task_complete(task_id):
    update_task_status(task_id, Status.done)
    print(f"Task {task_id} marked as complete.")


def mark_task_in_progress(task_id):
    update_task_status(task_id, Status.in_progress)
    print(f"Task {task_id} marked as in_progress.")


class Task:
    def __init__(self, task_id, description, created_at = datetime.now(), status = Status.todo, updated_at = datetime.now()):
        self.id  = task_id # A unique identifier for the task
        self.status = Status.todo
        self.description = description # A short description of the task
        self.createdAt = created_at #  The date and time when the task was created
        self.updatedAt = updated_at # The date and time when the task was last updated
