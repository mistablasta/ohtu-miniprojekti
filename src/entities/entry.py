from enum import Enum

class TypeData:
    def __init__(self, required_fields: list[str], optional_fields: list[str]):
        self.required_fields = required_fields
        self.optional_fields = optional_fields

    def get_required_fields(self):
        return self.required_fields

    def get_optional_fields(self):
        return self.optional_fields

class Type(Enum):
    """Built-in entry types"""
    ARTICLE = 1
    BOOK = 2
    MISC = 3

    def get_metadata(self):
        return type_map[self]

class Fields:
    """Reference for field types"""
    TITLE = "title"
    YEAR = "year"
    AUTHOR = "author"
    PUBLISHER = "publisher"
    JOURNAL = "journal"
    ADDRESS = "address"
    EDITION = "edition"
    MONTH = "month"
    NOTE = "note"
    NUMBER = "number"
    VOLUME = "volume"
    SERIES = "series"
    HOWPUBLISHED = "howpublished"

# Common fields for a few entry types
common = [Fields.TITLE, Fields.YEAR, Fields.AUTHOR]

class TypeMetadata:
    """
    Defines the metadata for all entry types
    """

    ARTICLE = TypeData(
        required_fields=common + [Fields.JOURNAL],
        optional_fields=[Fields.MONTH, Fields.NOTE, Fields.NUMBER]
    )
    BOOK = TypeData(
        required_fields=common + [Fields.PUBLISHER],
        optional_fields=[Fields.ADDRESS,
                         Fields.EDITION,
                         Fields.MONTH,
                         Fields.NOTE,
                         Fields.NUMBER,
                         Fields.SERIES,
                         Fields.VOLUME]
    )
    MISC = TypeData(
        required_fields=common,
        optional_fields=[Fields.HOWPUBLISHED,
                         Fields.MONTH,
                         Fields.NOTE]
    )

type_map = {
    Type.ARTICLE: TypeMetadata.ARTICLE,
    Type.BOOK: TypeMetadata.BOOK,
    Type.MISC: TypeMetadata.MISC
}

def type_from_str(name: str) -> Type | None:
    try:
        return Type[name.upper()]
    except KeyError:
        return None

class Entry:
    def __init__(self, id: int, key: str, type: Type, fields: dict, tags: list[str] | None=None):
        self.id = id
        self.key = key
        self.type = type
        self.fields = fields
        self.tags = tags if tags is not None else []

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

    def get_tags(self):
        return ", ".join(self.tags)

    def __str__(self):
        return (
            f"Entry(id={self.id}, key={self.key}, type={self.type}, "
            f"fields={self.fields}, tags={self.tags})"
        )
