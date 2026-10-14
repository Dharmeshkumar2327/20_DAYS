import unittest
import expense_tracker


class ExpenseTrackerTests(unittest.TestCase):
    def test_csv_fields(self):
        self.assertEqual(expense_tracker.FIELDS, ["date", "category", "description", "amount"])

    def test_data_file_location(self):
        self.assertEqual(expense_tracker.DATA_FILE.parent.name, "data")


if __name__ == "__main__":
    unittest.main()
