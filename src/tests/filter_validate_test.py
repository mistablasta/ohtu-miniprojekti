import unittest
from util import validate_year

class TestFilterValidation(unittest.TestCase):
    def test_validate_year(self):
        # Valid years
        self.assertIsNone(validate_year("2020"))
        self.assertIsNone(validate_year("1990"))

        # Invalid years
        self.assertEqual(validate_year("-1"), "Year must be between 0-3000")
        self.assertEqual(validate_year("3001"), "Year must be between 0-3000")

        # Non-numeric input
        self.assertEqual(validate_year("abc"), "Year must be a number.")
