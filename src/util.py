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
    title = form["title"]
    year = form["year"]
    #author = form["author"]
    #publisher = form["publisher"]
    #field = form["field"]

    if not _is_valid_string(title):
        return "Please input a valid title"

    if not year.isdigit():
        return "Year must be a number"

    return None

def _is_valid_string(value):
    """
    Returns true if the given string is non-empty. Accounts for whitespace strings.
    """
    return value is not None and len(value) > 0 and not str.isspace(value)