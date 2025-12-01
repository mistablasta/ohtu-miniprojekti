from entities.entry import type_from_str, Fields

# pylint: disable=too-many-return-statements
def validate_entry(form) -> str | None:
    """
    Validate that the form submitted by the user for an entry is correct.
    Returns an error if validation failed.
    """
    entry_type_str = form.get("type")
    entry_type = type_from_str(entry_type_str)

    if entry_type is None:
        return "Unknown entry type!"

    entry_type_data = entry_type.get_metadata()

    # Check if all required fields are present
    for required_field in entry_type_data.required_fields:
        if required_field not in form or not _is_valid_string(form[required_field]):
            return required_field.lower().capitalize() + " is a required field."

    # Special field checks
    if Fields.YEAR in form and not form[Fields.YEAR].isdigit():
        return "Year must be a number."

    return None

def _is_valid_string(value):
    """
    Returns true if the given string is non-empty. Accounts for whitespace strings.
    """
    return value is not None and len(value) > 0 and not str.isspace(value)
