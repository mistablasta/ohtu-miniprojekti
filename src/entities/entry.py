from enum import Enum

class Type(Enum):
    """Built-in entry types"""
    ARTICLE = 1
    BOOK = 2
    MISC = 3

class Fields:
    """Reference for field types"""
    TITLE = "title"
    YEAR = "year"
    AUTHOR = "author"
    PUBLISHER = "publisher"
    JOURNAL = "journal"

class Entry:
    def __init__(self, id: int, key: str, type: Type, fields: dict):
        self.id = id
        self.key = key
        self.type = type
        self.fields = fields

    def has_field(self, field_key: str):
        return field_key in self.fields

    def get_field(self, field_key: str):
        return self.fields.get(field_key)

    def set_field(self, field_key: str, value):
        self.fields[field_key] = value

    def get_title(self):
        if not self.has_field(Fields.TITLE):
            return None
        return self.get_field(Fields.TITLE)

    def __str__(self):
        return f"id={self.id}, key={self.key}, type={self.type}, fields={self.fields}"
