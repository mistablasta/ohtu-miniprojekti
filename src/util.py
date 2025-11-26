class UserInputError(Exception):
    pass

def validate_todo(content):
    if len(content) < 5:
        raise UserInputError("Todo content length must be greater than 4")

    if len(content) > 100:
          raise UserInputError("Todo content length must be smaller than 100")

def validate_entry(form) -> str | None:
    """
    Validate that the form submitted by the user for an entry is correct.
    Returns an error if validation failed.
    """
    entry_type = form.get("type")

    # Common fields required for all types
    title = form.get("title")
    year = form.get("year")

    if not _is_valid_string(title):
        return "Title is a required field."

    if not year.isdigit():
        return "Year must be a number."

    # Type specific fields that are required
    if entry_type == 'book':
        author = form.get("author")
        publisher = form.get("publisher")
        if not _is_valid_string(author):
            return "Author is a required field for books."
        if not _is_valid_string(publisher):
            return "Publisher is a required field for books."
            
    elif entry_type == 'article':
        author = form.get("author")
        journal = form.get("journal")
        if not _is_valid_string(author):
            return "Author is a required field for articles."
        if not _is_valid_string(journal):
            return "Journal is a required field for articles."

    # misc has no required fields

    return None

def _is_valid_string(value):
    """
    Returns true if the given string is non-empty. Accounts for whitespace strings.
    """
    return value is not None and len(value) > 0 and not str.isspace(value)