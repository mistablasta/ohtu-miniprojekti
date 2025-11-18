from config import db
from sqlalchemy import text

from entities.entry import Entry

def get_entries():
    """Get entries from database"""
    result = db.session.execute(text("SELECT id, title, year, author, publisher, field FROM entry"))
    entries = result.fetchall()
    return [Entry(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]) for entry in entries]

def add_entry(title, year, author, publisher, field):
    """Add entry to database"""
    sql = text("""INSERT INTO entry (title, year, author, publisher, field)
                  VALUES (:title, :year, :author, :publisher, :field)""")
    db.session.execute(sql, {"title": title,
                             "year": year, 
                             "author": author , 
                             "publisher": publisher, 
                             "field": field})
    db.session.commit()
