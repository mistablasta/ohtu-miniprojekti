import unittest
from src.entities.entry import Entry

class TestEntry(unittest.TestCase):

    def test_entry_initialization(self):
        """
        Test that all attributes are set correctly
        """
        entry = Entry(id=1,
                      title="Basic Title", 
                      year=2025, 
                      author="Jane Smith", 
                      publisher="Basic Publisher", 
                      field="Basic Field")

        self.assertEqual(entry.id, 1)
        self.assertEqual(entry.title, "Basic Title")
        self.assertEqual(entry.year, 2025)
        self.assertEqual(entry.author, "Jane Smith")
        self.assertEqual(entry.publisher, "Basic Publisher")
        self.assertEqual(entry.field, "Basic Field")

    def test_entry_str(self):
        """
        Test that the string representation of the Entry object
        returns the correct format: "author, year"
        """
        entry = Entry(id=1,
                      title="Title", 
                      year=2025, 
                      author="John Doe", 
                      publisher="Publisher", 
                      field="Field")
        expected_str = "John Doe, 2025"
        self.assertEqual(str(entry), expected_str)
