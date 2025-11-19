from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from repositories.entry_repository import add_entry, get_entries, delete_entry
from config import app, test_env
from util import validate_todo, validate_entry


@app.route("/")
def index():
    entries = get_entries()
    entries_dict = [entry.__dict__ for entry in entries]
    return render_template("index.html", entries_dict=entries_dict)

@app.route("/all_entries", methods=["GET"])
def get_all_entries():
    entries = get_entries()
    entries_json = [entry.__dict__ for entry in entries]
    return jsonify(entries_json)

@app.route("/new_todo")
def new():
    return render_template("new_todo.html")

@app.route("/create_todo", methods=["POST"])
def todo_creation():
    content = request.form.get("content")

    try:
        validate_todo(content)
        create_todo(content)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_todo")

@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    set_done(todo_id)
    return redirect("/")


#Entry functions
@app.route("/new_entry")
def new_entry():
    return render_template("add_entry.html")

@app.route("/create_entry", methods=["POST"])
def create_entry():
    title = request.form["title"]
    year = request.form["year"]
    author = request.form["author"]
    publisher = request.form["publisher"]
    field = request.form["field"]

    # Validate user input
    error = validate_entry(request.form)

    # Return the same page with an error message if validation failed
    if error:
        return render_template("add_entry.html", error=error, form=request.form)

    # Add the entry to DB
    add_entry(title, year, author, publisher, field)

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
    delete_entry(entry_id)
    return redirect("/")
