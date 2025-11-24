from sqlalchemy import text
from config import db

from entities.entry import Entry

def get_entries():
    """Get entries from database"""
    result = db.session.execute(text("SELECT id, title, year, author, publisher, field FROM entry"))
    entries = result.fetchall()
    return [Entry(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]) for entry in entries]

def search_entries(search):
    """Search entries from database"""
    sql = text("""SELECT id, title, year, author, publisher, field FROM entry
                                        WHERE title ILIKE :search
                                        OR author ILIKE :search
                                        OR publisher ILIKE :search
                                        OR year = :year""")

    try:
        year_search = int(search)
    except ValueError:
        year_search = None

    result = db.session.execute(sql, {"search": f"%{search}%", "year": year_search})
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

def delete_entry(entry_id):
    """Add delete button for entrys"""
    sql = text("DELETE FROM entry WHERE id = :id")
    db.session.execute(sql, {"id": entry_id})
    db.session.commit()

def get_entry_by_id(entry_id):
    """Get single entry by ID"""
    sql = text("SELECT id, title, year, author, publisher, field FROM entry WHERE id = :id")
    result = db.session.execute(sql, {"id": entry_id})
    entry = result.fetchone()
    return Entry(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5])

def update_entry_in_db(entry_id, title, year, author, publisher, field):
    """Update entry in database"""
    sql = text("""UPDATE entry
                  SET title = :title, year = :year, author = :author,
                      publisher = :publisher, field = :field
                  WHERE id = :id""")
    db.session.execute(sql, {"id": entry_id, "title": title, "year": year,
                            "author": author, "publisher": publisher, "field": field})
    db.session.commit()