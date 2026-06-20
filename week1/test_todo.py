import unittest
import os
import todo

class TestTodoList(unittest.TestCase):
    def setUp(self):
        # Use a temporary test file instead of the production file
        self.original_data_file = todo.DATA_FILE
        todo.DATA_FILE = "test_tasks.json"
        if os.path.exists(todo.DATA_FILE):
            os.remove(todo.DATA_FILE)

    def tearDown(self):
        if os.path.exists(todo.DATA_FILE):
            os.remove(todo.DATA_FILE)
        todo.DATA_FILE = self.original_data_file

    def test_load_tasks_empty(self):
        """Verify that starting without a file yields an empty list."""
        tasks = todo.load_tasks(todo.DATA_FILE)
        self.assertEqual(tasks, [])

    def test_add_task(self):
        """Verify that a task is successfully appended and ID is assigned."""
        tasks = []
        new_task = todo.add_task_to_list(tasks, "Finish Python assignment")
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(new_task["id"], 1)
        self.assertEqual(new_task["task"], "Finish Python assignment")
        self.assertEqual(new_task["completed"], False)

    def test_mark_task_completed(self):
        """Verify that a task can be marked as completed."""
        tasks = [{"id": 1, "task": "Finish Python assignment", "completed": False}]
        todo.mark_task_status(tasks, 1, completed=True)
        self.assertTrue(tasks[0]["completed"])

    def test_delete_task(self):
        """Verify that a task can be deleted from the list."""
        tasks = [
            {"id": 1, "task": "Finish Python assignment", "completed": False},
            {"id": 2, "task": "Submit report", "completed": False}
        ]
        removed = todo.delete_task_from_list(tasks, 1)
        self.assertEqual(removed["task"], "Finish Python assignment")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], 2)  # Remaining task

if __name__ == '__main__':
    unittest.main()
