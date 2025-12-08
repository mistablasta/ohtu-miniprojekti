import json

from sqlalchemy import text

from config import db
from entities.entry import Entry, Type, Fields


def create(type: Type, fields: dict, tags: list[str] | None = None):
    """
    Create a new entry
    """
    if fields is None:
        fields = {}

    key = _generate_unique_key(fields)
    
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

def _generate_unique_key(fields: dict) -> str:
    """
    Build a key from author, year, and title and ensure uniqueness in the database.
    """
    def _extract_author(author: str) -> str:
        if not author:
            return ""
        first_word = author.strip().split()[0] if author.strip() else ""
        return _clean(first_word)

    def _extract_title(title: str) -> str:
        if not title:
            return ""
        first_word = title.split()[0]
        return _clean(first_word)

    def _clean_year(year) -> str:
        return "".join(ch for ch in str(year) if ch.isdigit())

    def _clean(string: str) -> str:
        string_lower = string.lower()
        return "".join(ch for ch in string_lower if ("a" <= ch <= "z") or ("0" <= ch <= "9"))

    def _generate_base_key(fields: dict) -> str:
        author = fields.get(Fields.AUTHOR, "")
        title = fields.get(Fields.TITLE, "")
        year = fields.get(Fields.YEAR, "")

        author_part = _extract_author(author)
        title_part = _extract_title(title)
        year_part = _clean_year(year)

        key_parts = [part for part in [author_part, year_part, title_part] if part]
        base_key = "".join(key_parts)
        return base_key
    
    def _key_exists(key: str) -> bool:
        sql = text("SELECT 1 FROM entries WHERE key = :key LIMIT 1")
        result = db.session.execute(sql, {"key": key})
        return result.scalar() is not None
    
    def _ensure_unique_key(base_key: str) -> str:
        key = base_key
        counter = 1

        while _key_exists(key):
            key = f"{base_key}{counter}"
            counter += 1

        return key
    base_key = _generate_base_key(fields)
    return _ensure_unique_key(base_key)

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

def search(query: str):
    """
    Search all entries matching the given string query.
    This method will look for values in the fields or the entry key matching the query string.
    """

    sql = text("""
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
    """)

    result = db.session.execute(sql, {"query": f"%{query}%"})
    return _parse_entries(result.fetchall())

def search_filter(query: str = "",
                  sort: str = "",
                  year_min: int | None = None,
                  year_max: int | None = None,
                  entry_type: str = "",
                  tags: list[str] | None = None) -> list:

    if tags is None:
        tags = []

    sql = """
        SELECT e.id, e.key, e.type, e.fields, COALESCE(string_agg(t.name, ', ') , '') AS tags
        FROM entries e
        LEFT JOIN entry_tags et ON e.id = et.entry_id
        LEFT JOIN tags t ON et.tag_id = t.id
        WHERE 1=1
    """

    params = {}

    if query:
        sql += """
            AND (
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
            )
        """

        params["query"] = f"%{query}%"

    # TYPE filter
    if entry_type:
        sql += " AND e.type = :entry_type "
        params["entry_type"] = entry_type.lower()

    # YEAR MIN filter
    if year_min:
        sql += " AND (e.fields->>'year')::int >= :year_min "
        params["year_min"] = year_min

    # YEAR MAX FILTER
    if year_max:
        sql += " AND (e.fields->>'year')::int <= :year_max "
        params["year_max"] = year_max

    # TAGS FILTER
    if tags:
        tags_cleaned = [tag.strip() for tag in tags if tag.strip()]
        if tags_cleaned:
            sql += """
                AND e.id IN (
                    SELECT et.entry_id
                    FROM entry_tags et
                    JOIN tags t ON et.tag_id = t.id
                    WHERE t.name = ANY(:tags_array)
                )
            """
            params["tags_array"] = tags_cleaned

    sql += " GROUP BY e.id "

    if sort:
        if sort == "title_asc":
            order_sql = "fields->>'title' ASC"
        elif sort == "title_desc":
            order_sql = "fields->>'title' DESC"
        elif sort == "year_asc":
            order_sql = "fields->>'year' ASC"
        elif sort == "year_desc":
            order_sql = "fields->>'year' DESC"
        elif sort == "id":
            order_sql = "id DESC"
        else:
            order_sql = "id DESC"

        sql += f" ORDER BY {order_sql}"

    result = db.session.execute(text(sql), params)
    rows = result.fetchall()
    return _parse_entries(rows)

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
