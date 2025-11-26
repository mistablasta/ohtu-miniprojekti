import json

from sqlalchemy import text

from config import db
from entities.entry import Entry, Type


def create(key: str, type: Type, fields: dict):
    """
    Create a new entry
    """
    if fields is None:
        fields = dict()

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
    sql = text("""
        SELECT id, key, type, fields FROM entries
    """)
    result = db.session.execute(sql)
    return _parse_entries(result.fetchall())

def delete(id: int):
    """
    Delete an entry by its ID
    """
    sql = text("""DELETE FROM entries WHERE id = :id""")
    db.session.execute(sql, {"id": id})
    db.session.commit()

def update(entry: Entry):
    """
    Update an entire entry
    """
    sql = text("""
        UPDATE entries
        SET key = :key, type = :type, fields = :fields
        WHERE id = :id
    """)
    db.session.execute(sql, {
        "id": entry.id,
        "key": entry.key,
        "type": entry.type.name.lower(),
        "fields": json.dumps(entry.fields)
    })
    db.session.commit()

def search(query: str, filter):
    """
    Search all entries matching the given string query.
    This method will look for values in the fields or the entry key matching the query string.
    """
    if filter == "title_asc":
        order_sql = "fields->>'title' ASC"
    elif filter == "title_desc":
        order_sql = "fields->>'title' DESC"
    elif filter == "year_asc":
        order_sql = "fields->>'year' ASC"
    elif filter == "year_desc":
        order_sql = "fields->>'year' DESC"
    elif filter == "id":
        order_sql = "id DESC"

    sql = text(f"""
       SELECT id, key, type, fields
       FROM entries
       WHERE EXISTS (
           SELECT 1
           FROM jsonb_each_text(fields) AS t(key, value)
           WHERE value ILIKE :query
       )
       OR key ILIKE :query
       ORDER BY {order_sql}
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
