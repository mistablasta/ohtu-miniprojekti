import unittest
from util import validate_entry

class TestEntryValidation(unittest.TestCase):
    def setUp(self):
        self.base_misc = {
            "type": "misc",
            "title": "A Valid Title",
            "year": "2025",
        }

    def test_valid_misc_entry_returns_none(self):
        error = validate_entry(self.base_misc)
        self.assertIsNone(error)

    def test_missing_title_returns_title_required_error(self):
        form = {**self.base_misc, "title": ""}
        error = validate_entry(form)
        self.assertEqual(error, "Title is a required field.")

    def test_whitespace_title_returns_title_required_error(self):
        form = {**self.base_misc, "title": "   "}
        error = validate_entry(form)
        self.assertEqual(error, "Title is a required field.")

    def test_non_numeric_year_returns_year_number_error(self):
        form = {**self.base_misc, "year": "abc"}
        error = validate_entry(form)
        self.assertEqual(error, "Year must be a number.")

    def _valid_book(self):
        return {
            "type": "book",
            "title": "A Valid Book",
            "year": "2025",
            "author": "Author Name",
            "publisher": "Publisher Name",
        }

    def test_valid_book_returns_none(self):
        error = validate_entry(self._valid_book())
        self.assertIsNone(error)

    def test_book_missing_author_returns_author_required_error(self):
        form = self._valid_book()
        form["author"] = ""
        error = validate_entry(form)
        self.assertEqual(error, "Author is a required field for books.")

    def test_book_missing_publisher_returns_publisher_required_error(self):
        form = self._valid_book()
        form["publisher"] = ""
        error = validate_entry(form)
        self.assertEqual(error, "Publisher is a required field for books.")

    def _valid_article(self):
        return {
            "type": "article",
            "title": "A Valid Article",
            "year": "2025",
            "author": "Author Name",
            "journal": "Journal Name",
        }

    def test_valid_article_returns_none(self):
        error = validate_entry(self._valid_article())
        self.assertIsNone(error)

    def test_article_missing_author_returns_author_required_error(self):
        form = self._valid_article()
        form["author"] = ""
        error = validate_entry(form)
        self.assertEqual(error, "Author is a required field for articles.")

    def test_article_missing_journal_returns_journal_required_error(self):
        form = self._valid_article()
        form["journal"] = ""
        error = validate_entry(form)
        self.assertEqual(error, "Journal is a required field for articles.")
