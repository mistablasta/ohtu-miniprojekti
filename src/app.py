from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from entities.entry import (
    Type, type_from_str
)
from repositories import entry_repository as repository
from config import app, test_env
from util import validate_entry, dictionary_to_entry, validate_year
from services import batching

@app.route("/")
def index():
    entries = repository.get_all()
    return render_template("index.html", entries=entries)

#GET endpoint
@app.route("/all_entries", methods=["GET"])
def get_all_entries():
    entries = repository.get_all()
    entries_json = [entry.__dict__ for entry in entries]
    return jsonify(entries_json)

#Entry functions
@app.route("/new_entry")
def new_entry():
    return render_template("select_entry_type.html", types=Type)

@app.route("/add_entry_form", methods=["GET"])
def add_entry_form():
    doi = request.args.get("doi")
    entry_type_str = request.args.get("type")
    entry_type = type_from_str(entry_type_str)
    all_tags = repository.get_all_tags()

    # Invalid entry type
    if entry_type is None:
        return render_template("select_entry_type.html", types=Type)

    error = None

    if doi:
        try:
            entryid = dictionary_to_entry(doi)
            return redirect(f"/edit_entry/{entryid}")
        except ValueError as e:
            error = str(e)
            return render_template("select_entry_type.html", types=Type, error=error)

    return render_template("add_entry.html", entry_type=entry_type, all_tags=all_tags)

@app.route("/create_entry", methods=["POST"])
def create_entry():
    entry_type_str = request.form.get("type")
    entry_type = type_from_str(entry_type_str)

    all_tags = repository.get_all_tags()

    # Invalid entry type
    if entry_type is None:
        return render_template("select_entry_type.html", types=Type)

    fields = {}
    for key, value in request.form.items():
        if key not in ["type", "tags"]:
            fields[key] = value

    existing_tags = request.form.getlist("existing_tags")
    tags_str = request.form.get("tags", "")
    new_tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
    tags = list(set(existing_tags + new_tags))

    # Validate user input
    error = validate_entry(request.form)

    # Return the same page with an error message if validation failed
    if error:
        return render_template(
            "add_entry.html",
            error=error,
            form=request.form,
            entry_type=entry_type,
            all_tags=all_tags
        )

    # Create the entry
    repository.create("test", entry_type, fields, tags)

    flash("Entry added")
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })

# delete nappi entrylle
@app.route("/delete_entry/<entry_id>", methods=["POST"])
def delete_entrys(entry_id):
    try:
        repository.delete(int(entry_id))
        return redirect("/")
    except ValueError:
        return redirect("/")

# edit nappi entrylle
@app.route("/edit_entry/<entry_id>")
def edit_entry_form(entry_id):
    try:
        entry = repository.get(int(entry_id))
        all_tags = repository.get_all_tags()
        return render_template("edit_entry.html", entry=entry, all_tags=all_tags)
    except ValueError:
        return redirect("/")

@app.route("/update_entry/<entry_id>", methods=["POST"])
def update_entry(entry_id):
    entry = repository.get(int(entry_id))

    fields = {}
    for key, value in request.form.items():
        if key not in ["type", "tags"]:
            fields[key] = value

    existing_tags = request.form.getlist("existing_tags")
    tags_str = request.form.get("tags", "")
    new_tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
    tags = list(set(existing_tags + new_tags))
    entry.fields = fields
    entry.tags = tags

    repository.update(entry)
    flash("Entry updated")
    return redirect("/")

# search and filter function
@app.route("/search")
def search():
    query = request.args.get("query", "")
    filter = request.args.get("filter", default = 0, type = int)

    if filter != 1:
        entries = repository.search(query)
        return render_template(
            "index.html",
            entries=entries,
            query=query,
            filter=0,
            all_tags=repository.get_all_tags(),
            types=Type)

    sort = request.args.get("sort", "").strip()
    year_min = request.args.get("year_min", "").strip()
    year_max = request.args.get("year_max", "").strip()
    entry_type = request.args.get("entry_type", "").strip()
    selected_tags = request.args.getlist("tags")

    error_min = validate_year(year_min)
    error_max = validate_year(year_max)

    error = None
    if error_min and error_max:
        error = error_min
    elif error_min:
        error = error_min
    elif error_max:
        error = error_max

    # Only use year filters if they are valid
    search_year_min = int(year_min) if year_min and not error_min else None
    search_year_max = int(year_max) if year_max and not error_max else None

    if search_year_min is not None and search_year_max is not None:
        if search_year_min > search_year_max:
            search_year_min, search_year_max = search_year_max, search_year_min

    entries = repository.search_filter(query,
                                        sort,
                                        search_year_min,
                                        search_year_max,
                                        entry_type,
                                        selected_tags)
    return render_template(
        "index.html",
        entries=entries,
        query=query,
        filter=1,
        sort=sort,
        year_min=search_year_min,
        year_max=search_year_max,
        error=error,
        type=entry_type,
        all_tags=repository.get_all_tags(),
        selected_tags=selected_tags,
        types=Type)

@app.route("/batch", methods=["POST"])
def batch_action():
    body = request.get_json()
    action = body["action"]
    selection = body["selection"]
    return batching.process_request(action, selection)
