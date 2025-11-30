from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from entities.entry import (
    type_from_str, Type,
)
from repositories import entry_repository as repository
#from repositories.todo_repository import set_done #get_todos, #create_todo
from config import app, test_env
from util import validate_entry #, validate_todo


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

@app.route("/new_todo")
def new():
    return render_template("new_todo.html")

#@app.route("/create_todo", methods=["POST"])
#def todo_creation():
    #content = request.form.get("content")

    #try:
        #validate_todo(content)
        #create_todo(content)
        #return redirect("/")
    #except Exception as error:
        #flash(str(error))
        #return  redirect("/new_todo")

#@app.route("/toggle_todo/<todo_id>", methods=["POST"])
#def toggle_todo(todo_id):
    #set_done(todo_id)
    #return redirect("/")

#Entry functions
@app.route("/new_entry")
def new_entry():
    return render_template("select_entry_type.html", types=Type)

@app.route("/add_entry_form", methods=["GET"])
def add_entry_form():
    entry_type_str = request.args.get("type")
    entry_type = type_from_str(entry_type_str)

    # Invalid entry type
    if entry_type is None:
        return render_template("select_entry_type.html", types=Type)

    return render_template("add_entry.html", entry_type=entry_type)

@app.route("/create_entry", methods=["POST"])
def create_entry():
    entry_type_str = request.form.get("type")
    entry_type = type_from_str(entry_type_str)

    # Invalid entry type
    if entry_type is None:
        return render_template("select_entry_type.html", types=Type)

    fields = {}
    for key, value in request.form.items():
        if key not in ["type", "tags"]:
            fields[key] = value

    tags_str = request.form.get("tags", "")
    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
    
    # Validate user input
    error = validate_entry(request.form)

    # Return the same page with an error message if validation failed
    if error:
        return render_template(
            "add_entry.html",
            error=error,
            form=request.form,
            entry_type=entry_type
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
        return render_template("edit_entry.html", entry=entry)
    except ValueError:
        return redirect("/")

@app.route("/update_entry/<entry_id>", methods=["POST"])
def update_entry(entry_id):
    entry = repository.get(int(entry_id))

    fields = {}
    for key, value in request.form.items():
        if key not in ["type", "tags"]:
            fields[key] = value

    tags_str = request.form.get("tags", "")
    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
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
