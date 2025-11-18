from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from repositories.entry_repository import add_entry, get_entries
from config import app, test_env
from util import validate_todo

@app.route("/")
def index():
    todos = get_todos()
    entries = get_entries()
    unfinished = len([todo for todo in todos if not todo.done])
    return render_template("index.html", todos=todos, unfinished=unfinished, entries=entries)

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

    add_entry(title, year, author, publisher, field)

    flash("Entry added")
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
