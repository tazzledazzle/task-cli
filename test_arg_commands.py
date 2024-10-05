import unittest
from datetime import datetime

import app
from task import list_tasks


class TestArgCommands(unittest.TestCase):
    def test_something(self):
        timestamp = datetime.now().strftime('%Y-%m-%d')
        app.main("add", f"some new task {timestamp}")
        tasks = list_tasks()
        if tasks:
            timed_tasks = [task for task in tasks if timestamp in task.description]
            self.assertTrue(timed_tasks is not None)


    def test_add_task(self):
        app.main("add", "some new task")


    def test_remove_task(self):
        app.main("delete", "1")

    def test_update_task(self):
        app.main("update", "2", "I've changed the title")

    def test_list_tasks(self):
        app.main("list")

    def test_list_todo_tasks(self):
        app.main("list", "todo")

    def test_list_done(self):
        app.main("list", "complete")

    def test_mark_done(self):
        app.main("complete", "3")

if __name__ == '__main__':
    unittest.main()
