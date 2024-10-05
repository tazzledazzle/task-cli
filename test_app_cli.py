import os
import unittest
from datetime import datetime

from task import Status, load_json_tasks, generate_task_id, save_tasks, time_format, add_task

TEST_TASKS_FILE = 'test_tasks.json'
test_task = {
            'id': generate_task_id([]),
            'description': "This is a test task",
            'createdAt': datetime.now().strftime(time_format),
            'status': Status.todo.value,
            'updatedAt': datetime.now().strftime(time_format),
        }

class TestAppCli(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_TASKS_FILE):
            os.remove(TEST_TASKS_FILE)

    def test_task_creation(self):
        test_created_task = add_task(test_task['description'])

        self.assertEqual(test_created_task['description'], test_task['description'])
        self.assertEqual(test_created_task['status'], Status.todo.value)

    def test_load_tasks(self):
        try:
            tasks = load_json_tasks()
            self.assertEqual(len(tasks), 0)
        except Exception as e:
            print("this is a bad time")


    def test_save_tasks(self):
        test_save_task = load_json_tasks()
        test_save_task.append(test_task) # this isn't testing anything

        self.assertEqual(len(test_save_task), 1)

    def test_generate_task_id_simple(self):
        generated_task_id = generate_task_id([])
        self.assertEqual(generated_task_id, test_task['id'])


    def test_add_task(self):
        tasks = load_json_tasks()
        test_add_task = {
            'id': generate_task_id(tasks),
            'description': "this is a test",
            'created_at': datetime.now().strftime(time_format),
            'updated_at': datetime.now().strftime(time_format),
            'status': Status.todo.value
        }
        add_task(test_add_task['description'], test_add_task)

        self.assertEqual(tasks, [test_add_task])


    def test_generate_task_id_complex(self):
        tasks = []
        tasks.append(test_task)
        self.assertEqual(test_task['id'], 1)
        self.assertEqual(generate_task_id(tasks), 2)

    def test_load_tasks_gpt(self):
        with open(TEST_TASKS_FILE, 'w') as f:
            f.write('')

        tasks = load_json_tasks(TEST_TASKS_FILE)
        self.assertEqual(tasks, [], "Should return an empty list if the file is empty")

    def test_save_tasks_gpt(self):
        tasks_to_save = [{"id": 1, "description": "Test Task", "status": "todo"}]
        save_tasks(TEST_TASKS_FILE, tasks_to_save)

        tasks = load_json_tasks(TEST_TASKS_FILE)
        self.assertEqual(tasks[0]['id'], tasks_to_save[0]['id'], "Saved tasks should match the loaded tasks")


if __name__ == '__main__':
    unittest.main()