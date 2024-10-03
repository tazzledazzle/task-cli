import unittest
import os
from datetime import datetime

from task import Task, Status, TASKS_FILE, load_tasks, load_json_tasks, generate_task_id, save_tasks, add_task

TEST_TASKS_FILE = 'test_tasks.json'
test_task = {
            'id': generate_task_id([]),
            'description': "This is a test task",
            'createdAt': datetime.now().isoformat(),
            'status': Status.todo.value,
            'updatedAt': datetime.now().isoformat(),
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
        try:
            self.assertEqual(load_json_tasks(TEST_TASKS_FILE), [])
        except Exception as e:
            print("this is a bad time")


    def test_save_tasks(self):
        tasks = load_json_tasks(TEST_TASKS_FILE)
        tasks.append(test_task)
        save_tasks(TEST_TASKS_FILE, tasks)
        self.assertEqual(tasks, tasks)

    def test_generate_task_id_simple(self):
        generated_task_id = generate_task_id([])
        self.assertEqual(generated_task_id, test_task['id'])


    def test_add_task(self):
        tasks = []
        test_task = Task(generate_task_id(tasks), "this is a test")
        tasks.append(
            test_task
        )

        self.assertEqual(tasks, [test_task])


    def test_generate_task_id_complex(self):
        tasks = []
        tasks.append(test_task)
        self.assertEqual(test_task['id'], 1)
        self.assertEqual(generate_task_id(tasks), 2)

    def setUp(self):
        # Prepare a clean test environment
        if os.path.exists(TEST_TASKS_FILE):
            os.remove(TEST_TASKS_FILE)

    def test_load_tasks_gpt(self):
        # Start with an empty file
        with open(TEST_TASKS_FILE, 'w') as f:
            f.write('')  # Ensure file is empty

        tasks = load_json_tasks(TEST_TASKS_FILE)
        self.assertEqual(tasks, [], "Should return an empty list if the file is empty")

    def test_save_tasks_gpt(self):
        # Save tasks and then load them to verify
        tasks_to_save = [{"id": 1, "description": "Test Task", "status": "todo"}]
        save_tasks(TEST_TASKS_FILE, tasks_to_save)

        tasks = load_json_tasks(TEST_TASKS_FILE)
        self.assertEqual(tasks[0]['id'], tasks_to_save[0]['id'], "Saved tasks should match the loaded tasks")


if __name__ == '__main__':
    unittest.main()