class Entry:
    def __init__(self, entry_id, title, year, author, publisher, field):    # pylint: disable=too-many-positional-arguments
        self.id = entry_id
        self.title = title
        self.year = year
        self.author = author
        self.publisher = publisher
        self.field = field

    def __str__(self):
        return f"{self.author}, {self.year}"
