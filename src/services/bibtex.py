from string import Template

import util
from entities.entry import Entry, Fields

# Template for a BibTeX entry
ENTRY_TEMPLATE = Template("""
@$type{$key,
$fields
}
""")

def entries_to_bibtex(entries: list[Entry]) -> str:
    """
    Convert a list of entries to a single BibTeX string
    """
    # Return nothing if no entries are given
    if entries is None:
        return ""

    bibtex_entries = [entry_to_bibtex(entry) for entry in entries]
    return "".join(bibtex_entries)

def entry_to_bibtex(entry: Entry) -> str:
    """
    Convert a single entry to a BibTeX formatted string
    """
    # Return nothing if no entry is given
    if entry is None:
        return ""

    # Get all fields that we're going to export
    valid_fields = [
        (key, value)
        for key, value in entry.fields.items()
        if _is_valid_field(key, value)
    ]

    # Create padded field lines
    max_field_length = max((len(f) for f, _ in valid_fields), default=0)
    field_lines = []
    for key, value in valid_fields:
        padded = key.ljust(max_field_length)
        field_lines.append(f"   {padded} = \"{value}\",")

    # Substitute variables for the BibTeX entry template
    final_type = entry.type.name.lower()
    final_key = entry.key
    final_fields = "\n".join(field_lines)

    return ENTRY_TEMPLATE.safe_substitute(
        type=final_type,
        key=final_key,
        fields=final_fields
    )

def _is_valid_field(key, value) -> bool:
    """
    Check whether a key value combination is valid for a BibTeX entry
    """
    # Not an official field
    if not key in Fields.all():
        return False

    # Fields value is empty
    if not util.is_valid_string(value):
        return False

    return True
