import json

from sqlalchemy import text

from config import db
from entities.entry import Entry, Type


def create(key: str, type: Type, fields: dict, tags: list[str] | None = None):
    """
    Create a new entry
    """
    if fields is None:
        fields = {}

    sql = text("""
        INSERT INTO entries (key, type, fields)
        VALUES (:key, :type, :fields)
        Returning id
    """)
    result =db.session.execute(sql, {
        "key": key,
        "type": type.name.lower(),
        "fields": json.dumps(fields)
    })
    entry_id = result.scalar()

    if tags:
        _link_tags_to_entry(entry_id, tags)

    db.session.commit()
    return entry_id # for DOI autofill edit page fetching

def _link_tags_to_entry(entry_id: int, tags: list[str]):

    # Clear tags for the entry
    sql = text("DELETE FROM entry_tags WHERE entry_id = :entry_id")
    db.session.execute(sql, {"entry_id": entry_id})

    # Add new tags
    for tag_name in tags:
        tag_name = tag_name.strip()
        if not tag_name:
            continue

        # Find or create tag
        sql = text("SELECT id FROM tags WHERE name = :name")
        result = db.session.execute(sql, {"name": tag_name})
        tag_id = result.scalar()

        if not tag_id:
            sql = text("INSERT INTO tags (name) VALUES (:name) RETURNING id")
            result = db.session.execute(sql, {"name": tag_name})
            tag_id = result.scalar()

        # Link tag to entry
        sql = text("""
            INSERT INTO entry_tags (entry_id, tag_id)
            values (:entry_id, :tag_id)
            ON CONFLICT (entry_id, tag_id) DO NOTHING
        """)
        db.session.execute(sql, {"entry_id": entry_id, "tag_id": tag_id})

def get(id: int) -> Entry:
    """
    Get an entry by its ID
    """
    sql = text("""
        SELECT e.id, e.key, e.type, e.fields, COALESCE(string_agg(t.name, ', '), '') AS tags
        FROM entries e
        LEFT JOIN entry_tags et ON e.id = et.entry_id
        LEFT JOIN tags t ON et.tag_id = t.id
        WHERE e.id = :id
        GROUP BY e.id
    """)
    result = db.session.execute(sql, {"id": id})
    return _parse_entry(result.fetchone())

def get_all() -> list[Entry]:
    """
    Get all entries
    """
    sql = text("""
        SELECT e.id, e.key, e.type, e.fields, COALESCE(string_agg(t.name, ', '), '') AS tags
        FROM entries e
        LEFT JOIN entry_tags et ON e.id = et.entry_id
        LEFT JOIN tags t ON et.tag_id = t.id
        GROUP BY e.id
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

    _link_tags_to_entry(entry.id, entry.tags)

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
    else:
        order_sql = "id DESC"

    sql = text(f"""
        SELECT e.id, e.key, e.type, e.fields, COALESCE(string_agg(t.name, ', '), '') as tags
        FROM entries e
        LEFT JOIN entry_tags et ON e.id = et.entry_id
        LEFT JOIN tags t ON et.tag_id = t.id
        WHERE
            EXISTS (
                SELECT 1
                FROM jsonb_each_text(e.fields) AS f(key, value)
                WHERE value ILIKE :query
            )
            OR e.key ILIKE :query
            OR e.id IN (
                SELECT et.entry_id
                FROM entry_tags et
                JOIN tags t ON et.tag_id = t.id
                WHERE t.name ILIKE :query
            )
        GROUP BY e.id
        ORDER BY {order_sql}
    """)

    result = db.session.execute(sql, {"query": f"%{query}%"})
    return _parse_entries(result.fetchall())

def get_all_tags() -> list[str]:
    """
    Return all tag names sorted alphabetically.
    """
    sql = text("SELECT name FROM tags ORDER BY name")
    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]

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

    id, key, type, fields_json, tags_str = result

    if isinstance(type, str):
        type_enum = Type[type.upper()]
    else:
        raise ValueError(f"Unknown entry type: {type}")

    fields_dict = json.loads(fields_json) if isinstance(fields_json, str) else fields_json
    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()] if tags_str else []

    return Entry(id=id, key=key, type=type_enum, fields=fields_dict, tags=tags)
