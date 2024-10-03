import unittest
import json
from datetime import datetime
from venv import create

from task import Task, Status, TASKS_FILE, load_tasks, load_json_tasks, generate_task_id, save_tasks, add_task

TEST_TASKS_FILE = 'test_tasks.json'
test_task = {
            'id': generate_task_id([]),
            'description': "This is a test task",
            'createdAt': datetime.now(),
            'status': Status.todo,
            'updatedAt': datetime.now(),
        }

class TestAppCli(unittest.TestCase):
    def test_app_cli(self):
        self.assertTrue(True)

    def test_task_creation(self):
        timestamp = datetime.now()
        task = Task(1, "a test task, close it", created_at=timestamp, status=Status.todo, updated_at=timestamp)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.createdAt, timestamp)
        self.assertEqual(task.updatedAt, timestamp)
        self.assertEqual(task.status, Status.todo)

    def test_load_tasks(self):
        tasks = load_json_tasks(TEST_TASKS_FILE)
        self.assertEqual(tasks, [])

    def test_save_tasks(self):
        tasks = load_json_tasks(TEST_TASKS_FILE)
        tasks.append(test_task)
        save_tasks(tasks)
        self.assertEqual(tasks, tasks)

    def test_generate_task_id_simple(self):
        generated_task_id = generate_task_id([])
        self.assertEqual(generated_task_id, test_task['id'])


    def test_add_task(self):
        tasks = []
        add_task("This is a test task!")
        load_json_tasks(TEST_TASKS_FILE)
        self.assertEqual(tasks, load_json_tasks(TEST_TASKS_FILE))


    def test_generate_task_id_complex(self):
        tasks = []
        tasks.append(test_task)
        self.assertEqual(test_task['id'], 1)
        self.assertEqual(generate_task_id(tasks), 2)