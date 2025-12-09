import requests
from requests.exceptions import RequestException
import bibtexparser
from entities.entry import type_from_str, Fields, Type
from repositories import entry_repository as repository

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
        if required_field not in form or not is_valid_string(form[required_field]):
            return required_field.lower().capitalize() + " is a required field."

    # Special field checks
    if Fields.YEAR in form and not form[Fields.YEAR].isdigit():
        return "Year must be a number."

    return None

def is_valid_string(value):
    """
    Returns true if the given string is non-empty. Accounts for whitespace strings.
    """
    return value is not None and len(value) > 0 and not str.isspace(value)

def doi_to_dictionary(doi: str):
    try:
        if doi.startswith("http"):
            url = doi
        else:
            url = f"https://doi.org/{doi}"

        headers = {"Accept": "text/bibliography; style=bibtex"}
        r = requests.get(url, headers = headers, timeout=10)
        r.encoding = "utf-8"
        bib = r.text

        parser = bibtexparser.loads(bib)
        bibdict = parser.entries

        if not bibdict:
            return {"error": f"No BibTeX entry found for DOI {doi}"}

        res = {}
        for dic in bibdict:
            res.update(dic)
        return res

    except RequestException as e:
        return {"error": f"Failed to fetch DOI '{doi}': {str(e)}"}
    except (ValueError, TypeError) as e:
        return {"error": f"Failed to parse DOI '{doi}': {str(e)}"}

def dictionary_to_entry(doi: str):
    bib = doi_to_dictionary(doi)

    if "error" in bib:
        raise ValueError(bib["error"])

    bib_type = bib.get("ENTRYTYPE", "").lower()
    if bib_type == "article":
        etype = Type.ARTICLE
    elif bib_type == "book":
        etype = Type.BOOK
    else:
        etype = Type.MISC

    key = bib.get("ID", bib.get("doi", "unknown"))

    bib_to_fields = {
        "title": Fields.TITLE,
        "year": Fields.YEAR,
        "author": Fields.AUTHOR,
        "publisher": Fields.PUBLISHER,
        "journal": Fields.JOURNAL,
        "edition": Fields.EDITION,
        "month": Fields.MONTH,
        "note": Fields.NOTE,
        "number": Fields.NUMBER,
        "volume": Fields.VOLUME,
        "series": Fields.SERIES,
        "howpublished": Fields.HOWPUBLISHED,
    }

    metadata = etype.get_metadata()
    allowed_fields = metadata.get_required_fields() + metadata.get_optional_fields()

    fields = {
        field_enum: bib[bib_key]
        for bib_key, field_enum in bib_to_fields.items()
        if bib_key in bib and field_enum in allowed_fields
    }

    entryid = repository.create(key, etype, fields)
    return entryid

def validate_year(value_str):
    if value_str:
        try:
            year = int(value_str)
        except ValueError:
            return "Year must be a number."

        if year < 0 or year > 3000:
            return "Year must be between 0-3000"
    return None
