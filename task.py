"""
    functionality of data class task
"""
import json
import os.path
from datetime import datetime
from enum import Enum

TASKS_FILE = 'tasks.json'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class Status(Enum):
    """
        Enum representing the possible statuses for tasks.

        Attributes:
            TODO (str): Represents a task that is yet to be started ('todo').
            IN_PROGRESS (str): Represents a task that is currently in progress ('in_progress').
            DONE (str): Represents a task that has been completed ('done').
    """
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


def list_tasks(status=None):
    """
       List all tasks, or tasks filtered by status.

       Parameters:
           status (str, optional): The status to filter tasks by.
                                    Should be one of 'todo', 'in_progress', or 'done'.
                                   If None, all tasks are listed.

       Returns:
           list: A list of tasks that match the given status, or all tasks if no status is provided.
                 If no tasks are found, an empty list is returned.
   """
    if not os.path.exists(TASKS_FILE):
        return []
    tasks = load_json_tasks()
    if status:
        tasks = [task for task in tasks if status == task['status']]
    if tasks:
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']},"
                  f" Updated At: {task['updated_at']}")
        return tasks

    print("No tasks found")
    return []

def add_task(description, task=None):
    """
    Add a new task to the task list
        Parameters:
            description (str): The description of the task.
            task (dict, optional): A predefined task object to add. If not provided, a new
                                    task will be created.

        Returns:
            dict: The newly added task object.
    """
    tasks = load_json_tasks()
    if task:
        tasks.append(task)
    else:
        task = {
            'id': generate_task_id(tasks),
            'description': description,
            'status': Status.TODO.value,
            'created_at': datetime.now().strftime(TIME_FORMAT),
            'updated_at': datetime.now().strftime(TIME_FORMAT)
        }
        tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {tasks}")
    return task

def load_json_tasks(tasks_file=TASKS_FILE):
    """
        Load tasks from the specified JSON file.

        Parameters:
            tasks_file (str, optional): The path to the JSON file
                                        where tasks are stored. Defaults to TASKS_FILE.

        Returns:
            list: A list of tasks loaded from the file. If the file does
            not exist or contains invalid JSON, an empty list is returned.
     """
    if not os.path.exists(tasks_file):
        return []

    with open(tasks_file, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print(f"The file {tasks_file} contains invalid JSON!")
    return []


def save_tasks(tasks, filepath=TASKS_FILE):
    """
        Save the list of tasks to the specified JSON file.

        Parameters:
            tasks (list): The list of tasks to be saved.
            filepath (str, optional): The path to the JSON file where tasks will be saved.
             Defaults to TASKS_FILE.

        Returns:
            None
    """
    for task in tasks:
        if hasattr(task, 'createdAt'):
            if isinstance(task['createdAt'], datetime):
                task['createdAt'] = task['createdAt'].strftime(TIME_FORMAT)
            if isinstance(task['updatedAt'], datetime):
                task['updatedAt'] = task['updatedAt'].strftime(TIME_FORMAT)
            if isinstance(task['status'], Status):
                task['status'] = task['status'].value

    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, indent=4)


def find_task_by_id(task_id):
    """
        Find a task by its ID.

        Parameters:
            task_id (int): The unique identifier of the task.

        Returns:
            dict: The task object if found, otherwise an empty list.
    """
    tasks = load_json_tasks(TASKS_FILE)
    for task in tasks:
        if task['id'] == task_id:
            return task
    return []


def generate_task_id(tasks):
    """
        Generate a new unique task ID based on the existing tasks.

        Parameters:
            tasks (list): The list of current tasks.

        Returns:
            int: The next available task ID.
    """
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1


def update_task(task_id, updated_desc):
    """
        Update the description of a task.

        Parameters:
            task_id (int): The unique identifier of the task to be updated.
            updated_desc (str): The new description for the task.

        Returns:
            dict: The updated task object if found, otherwise an empty list.
    """
    tasks = list_tasks()
    if tasks:
        for task in tasks:
            if task['id'] == task_id:
                task['description'] = updated_desc
                task['updatedAt'] = datetime.now().strftime(TIME_FORMAT)
                save_tasks(tasks)
                print(f"Task {task_id} updated.")
                return task
    print(f"Task {task_id} not found.")
    return []


def delete_task(task_id):
    """
        Delete a task by its ID.

        Parameters:
            task_id (int): The unique identifier of the task to be deleted.

        Returns:
            list: The updated list of tasks with the task removed.
                    If the task is not found, an empty list is returned.
    """
    tasks = list_tasks()
    if tasks:
        tasks = [task for task in tasks if task['id'] != task_id]
        save_tasks(tasks)
        print(f"Task {task_id} deleted.")
        return tasks
    print(f"Task {task_id} not found.")
    return []

def update_task_status(task_id, status):
    """
        Update the status of a task.

        Parameters:
            task_id (int): The unique identifier of the task to update.
            status (str): The new status for the task (e.g., 'todo', 'in_progress', 'done').

        Returns:
            dict: The updated task object if found, otherwise an empty list.
    """
    tasks = list_tasks()
    if tasks:
        for task in tasks:
            if task['id'] == task_id:
                task['status'] = status
                task['updatedAt'] = datetime.now().strftime(TIME_FORMAT)
                save_tasks(tasks)
                print(f"Task {task_id} updated with status: {status}.")
                return task
    print(f"Task {task_id} not found.")
    return []


def mark_task_complete(task_id):
    """
        Marks a task as complete.

        Args:
            task_id (int): The unique identifier of the task.

        Returns:
            None
    """
    task = update_task_status(task_id, Status.DONE.value)
    if task:
        print(f"Task {task_id} marked as complete.")
    else:
        print(f"Task {task_id} not found.")

def mark_task_in_progress(task_id):
    """
    Marks a task as in progress.

    Args:
        task_id (int): The unique identifier of the task.

    Returns:
        None
    """
    task = update_task_status(task_id, Status.IN_PROGRESS.value)
    if task:
        print(f"Task {task_id} marked as in_progress.")
    else:
        print(f"Task {task_id} not found.")
