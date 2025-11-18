class Entry:
    def __init__(self, id, title, year, author, publisher, field):
        self.id = id
        self.title = title
        self.year = year
        self.author = author
        self.publisher = publisher
        self.field = field

    def __str__(self):
        return f"{self.author}, {self.year}"
