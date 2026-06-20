import unittest
import os
import tracker

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        # Use a temporary test file instead of production database
        self.original_data_file = tracker.DATA_FILE
        tracker.DATA_FILE = "test_expenses.json"
        if os.path.exists(tracker.DATA_FILE):
            os.remove(tracker.DATA_FILE)

    def tearDown(self):
        if os.path.exists(tracker.DATA_FILE):
            os.remove(tracker.DATA_FILE)
        tracker.DATA_FILE = self.original_data_file

    def test_load_expenses_default(self):
        """Verify that starting without a file initializes total to 0.0."""
        data = tracker.load_expenses(tracker.DATA_FILE)
        self.assertEqual(data["total"], 0.0)
        self.assertEqual(data["history"], [])

    def test_process_valid_expenses(self):
        """Verify that multiple numeric entries accumulate properly."""
        total = 0.0
        history = []

        # Add first expense
        total, should_exit = tracker.process_expense(total, "10.50", history)
        self.assertEqual(total, 10.50)
        self.assertFalse(should_exit)
        self.assertEqual(history, [10.50])

        # Add second expense
        total, should_exit = tracker.process_expense(total, "25", history)
        self.assertEqual(total, 35.50)
        self.assertFalse(should_exit)
        self.assertEqual(history, [10.50, 25.0])

    def test_process_invalid_input(self):
        """Verify that text inputs raise a ValueError (Defensive Poka-Yoke)."""
        total = 0.0
        history = []
        with self.assertRaises(ValueError):
            tracker.process_expense(total, "twenty", history)

    def test_process_negative_input(self):
        """Verify that negative numbers are rejected."""
        total = 0.0
        history = []
        with self.assertRaises(ValueError):
            tracker.process_expense(total, "-5.00", history)

    def test_process_quit_sentinel(self):
        """Verify that the sentinel value 'quit' triggers the shutdown signal."""
        total = 100.0
        history = [100.0]
        new_total, should_exit = tracker.process_expense(total, "quit", history)
        self.assertEqual(new_total, 100.0)
        self.assertTrue(should_exit)

if __name__ == '__main__':
    unittest.main()
