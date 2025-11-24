import json

from sqlalchemy import text

from config import db
from entities.entry import Entry, Type


def create(key: str, type: Type, fields: dict):
    """
    Create a new entry
    """
    sql = text("""
        INSERT INTO entries (key, type, fields)
        VALUES (:key, :type, :fields)
    """)
    db.session.execute(sql, {
        "key": key,
        "type": type.name.lower(),
        "fields": json.dumps(fields)
    })
    db.session.commit()

def get(id: int) -> Entry:
    """
    Get an entry by its ID
    """
    sql = text("""
        SELECT id, key, type, fields FROM entries
        WHERE id = :id
    """)
    result = db.session.execute(sql, {"id": id})
    return _parse_entry(result.fetchone())

def get_all() -> list[Entry]:
    """
    Get all entries
    """
    sql = text("""SELECT * FROM entries""")
    result = db.session.execute(sql)
    return _parse_entries(result)

def delete(id: int):
    """
    Delete an entry by its ID
    """
    sql = text("""DELETE FROM entries WHERE id = :id""")
    db.session.execute(sql, {"id": id})

def update(entry: Entry):
    """
    Update an entire entry
    """
    sql = text("""
        UPDATE entries
    """)
    db.session.execute(sql, {
        "key": entry.key,
        "type": entry.type,
        "fields": json.dumps(entry.fields)
    })
    db.session.commit()

def search(query: str):
    """
    Search all entries matching the given string query.
    This method will look for values in the fields or the entry key matching the query string.
    """
    sql = text("""
       SELECT id, key, type, fields
       FROM entries
       WHERE EXISTS (
           SELECT 1
           FROM jsonb_each_text(fields) AS t(key, value)
           WHERE value ILIKE :query
       )
       OR key ILIKE :query
   """)

    result = db.session.execute(sql, {"query": f"%{query}%"})
    return _parse_entries(result.fetchall())

def _parse_entries(result) -> list[Entry]:
    """
    Parse multiple entries at once from a result
    """
    return [_parse_entry(row) for row in result]

def _parse_entry(result) -> Entry | None:
    """
    Parse a single entry from a result
    """
    if result is None:
        return None

    id = result[0]
    key = result[1]
    type = result[2]

    if isinstance(type, str):
        type_enum = Type[type.upper()]
    else:
        raise ValueError(f"Unknown entry type: {type}")

    fields_json = result[3]
    fields_dict = json.loads(fields_json) if isinstance(fields_json, str) else fields_json

    return Entry(id=id, key=key, type=type_enum, fields=fields_dict)


#-------------------------------------

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