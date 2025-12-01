import unittest
from entities.entry import Entry, Type, Fields


class TestEntry(unittest.TestCase):

    def test_fields_operations(self):
        entry = Entry(
            1,
            "key1",
            Type.BOOK,
            {
                Fields.TITLE: "Book",
                Fields.AUTHOR: "Author"
            },
            tags=["tag1", "tag2"]
        )

        # test has_field, get_field, set_field
        self.assertTrue(entry.has_field(Fields.TITLE))
        self.assertEqual(entry.get_field(Fields.TITLE), "Book")
        self.assertIsNone(entry.get_field(Fields.PUBLISHER))

        entry.set_field(Fields.YEAR, 2025)
        self.assertTrue(entry.has_field(Fields.YEAR))
        self.assertEqual(entry.get_field(Fields.YEAR), 2025)

        # test get_title
        self.assertEqual(entry.get_title(), "Book")
        entry_no_title = Entry(2, "key2", Type.ARTICLE, {})
        self.assertIsNone(entry_no_title.get_title())

        # test get_tags
        self.assertEqual(entry.get_tags(), "tag1, tag2")
        entry_no_tags = Entry(3, "key3", Type.ARTICLE, {})
        self.assertEqual(entry_no_tags.get_tags(), "")


    def test_enum_and_str(self):
        entry = Entry(3, "key3", Type.ARTICLE, {Fields.JOURNAL: "Journal"}, tags=["tag1", "tag2"])
        self.assertEqual(entry.type, Type.ARTICLE)

        s = str(entry)
        self.assertIn("id=3", s)
        self.assertIn("key=key3", s)
        self.assertIn("type=Type.ARTICLE", s)
        self.assertIn("fields", s)
        self.assertIn("tags=[\'tag1\', \'tag2\']", s)

    def test_all_types_have_metadata_defined(self):
        for t in Type:
            try:
                self.assertIsNotNone(t.get_metadata())
            except KeyError:
                self.fail(f"Type {t} did not have metadata defined")
