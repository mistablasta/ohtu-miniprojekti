from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from entities.entry import type_from_str, Type, Fields
from repositories import entry_repository as repository
from config import app, test_env
from util import validate_entry
import requests
from requests.exceptions import RequestException
import bibtexparser


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
    entry_type_str = request.args.get("type")
    entry_type = type_from_str(entry_type_str)
    all_tags = repository.get_all_tags()

    # Invalid entry type
    if entry_type is None:
        return render_template("select_entry_type.html", types=Type)

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
    filter = request.args.get("filter", "id")
    entries = repository.search(query, filter)
    return render_template("index.html", entries=entries, query=query, filter=filter)

@app.route("/doi2bib")
def test_doi():
    return dictionary_to_entry("https://doi.org/10.1126/science.aar3646")

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

        res = {} 
        for dic in bibdict: 
            res.update(dic) 
        return res 
    
    except RequestException as e:
        return {"error": f"Failed to fetch DOI '{doi}': {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to parse DOI '{doi}': {str(e)}"}

def dictionary_to_entry(doi: str):
    bib = doi_to_dictionary(doi)

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

    repository.create(key, etype, fields)