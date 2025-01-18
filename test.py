import unittest
import json
from .task_cli import add_task, update_task, delete_task, mark_task, list_tasks, TASK_FILE

class TestTaskCLI(unittest.TestCase):
    def setUp(self):
        """Set up a temporary tasks.json file for testing."""
        self.test_file = TASK_FILE
        if self.test_file.exists():
            self.test_file.unlink()  # Delete existing file
        # Initialize with empty JSON array instead of just touching
        with self.test_file.open('w') as f:
            json.dump([], f)

    def tearDown(self):
        """Clean up the tasks.json file after tests."""
        if self.test_file.exists():
            self.test_file.unlink()

    def load_tasks(self):
        """Helper function to load tasks from the JSON file."""
        with self.test_file.open("r") as file:
            return json.load(file)

    def test_add_task(self):
        """Test adding a new task."""
        add_task("Test task 1")
        tasks = self.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Test task 1")
        self.assertEqual(tasks[0]["status"], "todo")

    def test_update_task(self):
        """Test updating a task."""
        add_task("Test task 1")
        update_task(1, "Updated task description")
        tasks = self.load_tasks()
        self.assertEqual(tasks[0]["description"], "Updated task description")
        self.assertNotEqual(tasks[0]["updatedAt"], tasks[0]["createdAt"])

    def test_delete_task(self):
        """Test deleting a task."""
        add_task("Test task 1")
        delete_task(1)
        tasks = self.load_tasks()
        self.assertEqual(len(tasks), 0)

    def test_mark_task(self):
        """Test marking a task as done or in-progress."""
        add_task("Test task 1")
        mark_task(1, "done")
        tasks = self.load_tasks()
        self.assertEqual(tasks[0]["status"], "done")
        mark_task(1, "in-progress")
        tasks = self.load_tasks()
        self.assertEqual(tasks[0]["status"], "in-progress")

    def test_list_tasks(self):
        """Test listing tasks by status."""
        add_task("Task 1")
        add_task("Task 2")
        mark_task(1, "done")
        output = []
        list_tasks("done")
        list_tasks("todo")
        tasks = self.load_tasks()
        done_tasks = [task for task in tasks if task["status"] == "done"]
        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(done_tasks[0]["description"], "Task 1")
        todo_tasks = [task for task in tasks if task["status"] == "todo"]
        self.assertEqual(len(todo_tasks), 1)
