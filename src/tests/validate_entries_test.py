import unittest
from util import validate_entry

class TestEntryValidation(unittest.TestCase):
    def setUp(self):
        self.valid_form = {"title": "Valid Title", "year": "2025"}
        self.invalid_title_form = {"title": "", "year": "2025"}
        self.invalid_year_form = {"title": "Valid Title", "year": "abcd"}

    def test_valid_entry_returns_none(self):
        """
        A valid entry should return None (no error)
        """
        error = validate_entry(self.valid_form)
        self.assertIsNone(error)

    def test_empty_title_returns_error(self):
        """
        An empty title should return an error message
        """
        error = validate_entry(self.invalid_title_form)
        self.assertEqual(error, "Please input a valid title")

    def test_whitespace_title_returns_error(self):
        """
        A title with only whitespace should return an error message
        """
        form = {"title": "   ", "year": "2025"}
        error = validate_entry(form)
        self.assertEqual(error, "Please input a valid title")

    def test_invalid_year_returns_error(self):
        """
        A non-numeric year should return an error message
        """
        error = validate_entry(self.invalid_year_form)
        self.assertEqual(error, "Year must be a number")
