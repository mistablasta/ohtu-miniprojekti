from flask import Response, make_response
from repositories import entry_repository
from services import bibtex

def get_error(message, status: int) -> Response:
    return make_response(({"error": message}, status))

def is_valid_selection(selection) -> bool:
    if selection is None or not isinstance(selection, list):
        return False

    if len(selection) == 0:
        return False

    for entry_id in selection:
        try:
            int(entry_id)
        except ValueError:
            return False

    return True

def run_delete_action(selection) -> Response:
    for entry_id in selection:
        entry_repository.delete(entry_id)

    return make_response(({"error": ""}, 200))

def run_bibtex_action(selection) -> Response:
    entries = []

    for entry_id in selection:
        entry = entry_repository.get(int(entry_id))
        if entry is not None:
            entries.append(entry)

    result = bibtex.entries_to_bibtex(entries)

    return make_response(({"bibtex": result}, 200))

def process_request(action, selection) -> Response:
    # Validate action
    if action is None or not action in ["delete", "bibtex"]:
        return get_error("Action missing or invalid", 400)

    # Validate selection
    if not is_valid_selection(selection):
        return get_error("Selection missing or empty", 400)

    # Run actions
    if action == "delete":
        return run_delete_action(selection)
    if action == "bibtex":
        return run_bibtex_action(selection)

    return get_error("Action missing or invalid", 400)
