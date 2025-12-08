import unittest
import textwrap

from services import bibtex
from entities.entry import Entry, Type, Fields

class TestBibtex(unittest.TestCase):

    def setUp(self):
        self.simple_entry = Entry(
            id=0,
            key="mykey",
            type=Type.BOOK,
            fields={
                Fields.TITLE: "My Title"
            }
        )
        self.simple_entry_expectation = textwrap.dedent("""
            @book{mykey,
               title = "My Title",
            }
        """)

    # ---
    # entry_to_bibtex
    # ---

    def test_simple_entry_to_bibtex(self):
        self.assertEqual(
            bibtex.entry_to_bibtex(self.simple_entry),
            self.simple_entry_expectation
        )

    def test_simple_entry_to_bibtex_invalid_field_ignored(self):
        # Attempt to add an invalid field
        self.simple_entry.fields = {
            Fields.TITLE: "My Title",
            "myfield": "test"
        }

        self.assertEqual(
            bibtex.entry_to_bibtex(self.simple_entry),
            self.simple_entry_expectation
        )

    def test_simple_entry_to_bibtex_empty_values_ignored(self):
        # Attempt to add fields with empty values
        self.simple_entry.fields = {
            Fields.TITLE: "My Title",
            Fields.NOTE: "",
            Fields.MONTH: None,
        }

        self.assertEqual(
            bibtex.entry_to_bibtex(self.simple_entry),
            self.simple_entry_expectation
        )

    def test_none_entry_to_bibtex_returns_empty(self):
        expectation = ""

        self.assertEqual(
            bibtex.entry_to_bibtex(None),
            expectation
        )

    def test_simple_entry_to_bibtex_without_fields(self):
        self.simple_entry.fields = {}
        expectation = textwrap.dedent("""
            @book{mykey,
            
            }
        """)

        self.assertEqual(
            bibtex.entry_to_bibtex(self.simple_entry),
            expectation
        )

    # ---
    # entries_to_bibtex
    # ---

    def test_multiple_simple_entries_to_bibtex(self):
        entries = [self.simple_entry, self.simple_entry]
        expectation = f"{self.simple_entry_expectation}{self.simple_entry_expectation}"

        self.assertEqual(
            bibtex.entries_to_bibtex(entries),
            expectation
        )

    def test_empty_entry_list_to_bibtex(self):
        entries = []
        expectation = ""

        self.assertEqual(
            bibtex.entries_to_bibtex(entries),
            expectation
        )

    def test_none_entry_list_to_bibtex(self):
        entries = None
        expectation = ""

        self.assertEqual(
            bibtex.entries_to_bibtex(entries),
            expectation
        )
