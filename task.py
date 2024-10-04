import json
import os.path
from datetime import datetime
from enum import Enum

TASKS_FILE = 'tasks.json'
time_format = '%Y-%m-%d %H:%M:%S'


class Status(Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    done = 'done'


def list_tasks(status=None):
    if not os.path.exists(TASKS_FILE):
        return []
    tasks = load_json_tasks()
    if status:
        tasks = [task for task in tasks if status == task['status']]
    if tasks:
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Updated At: {task['updated_at']}")
    else:
        print("No tasks found")

def add_task(description, task=None):
    tasks = load_json_tasks()
    if task:
        tasks.append(task)
    else:
        task = {
            'id': generate_task_id(tasks),
            'description': description,
            'status': Status.todo.value,
            'created_at': datetime.now().strftime(time_format),
            'updated_at': datetime.now().strftime(time_format)
        }
        tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {tasks}")
    return task

def load_json_tasks(tasks_file=TASKS_FILE):
    if not os.path.exists(tasks_file):
        return []

    with open(tasks_file, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print(f"The file {tasks_file} contains invalid JSON!")
    return []


def save_tasks(tasks, filepath=TASKS_FILE):
    for task in tasks:
        if hasattr(task, 'createdAt'):
            if isinstance(task['createdAt'], datetime):
                task['createdAt'] = task['createdAt'].strftime(time_format)
            if isinstance(task['updatedAt'], datetime):
                task['updatedAt'] = task['updatedAt'].strftime(time_format)
            if isinstance(task['status'], Status):
                task['status'] = task['status'].value

    with open(filepath, 'w') as file:
        json.dump(tasks, file, indent=4)


def find_task_by_id(id):
    tasks = load_json_tasks(TASKS_FILE)
    for task in tasks:
        if task['id'] == id:
            return task
    return []


def generate_task_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1


def update_task(task_id, updated_desc):
    tasks = list_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = updated_desc
            task['updatedAt'] = datetime.now().strftime(time_format)
            save_tasks(tasks)
            print(f"Task {task_id} updated.")
            return task
    print(f"Task {task_id} not found.")
    return []


def delete_task(task_id):
    tasks = list_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted.")
    return tasks

def update_task_status(task_id, status):
    tasks = list_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().strftime(time_format)
            save_tasks(tasks)
            print(f"Task {task_id} updated with status: {status}.")
            return task
    print(f"Task {task_id} not found.")
    return []


def mark_task_complete(task_id):
    task = update_task_status(task_id, Status.done.value)
    if task:
        print(f"Task {task_id} marked as complete.")
    else:
        print(f"Task {task_id} not found.")


def mark_task_in_progress(task_id):
    task = update_task_status(task_id, Status.in_progress.value)
    if task:
        print(f"Task {task_id} marked as in_progress.")
    else:
        print(f"Task {task_id} not found.")

class Task:
    def __init__(
            self,
            task_id,
            description,
            created_at = datetime.now().strftime(time_format),
            status = Status.todo.value,
            updated_at = datetime.now().strftime(time_format)
            ):

        self.id  = task_id # A unique identifier for the task
        self.status = status
        self.description = description # A short description of the task
        self.createdAt = created_at #  The date and time when the task was created
        self.updatedAt = updated_at # The date and time when the task was last updated
