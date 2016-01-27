from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student_add", methods=['POST'])
def student_add():
    """Show that the student was successfully added to the db"""
    # return render_template("success_add.html")

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    QUERY = """INSERT INTO students (first_name, last_name, github)
               VALUES (:first_name, :last_name, :github)"""

    db_cursor = hackbright.db.session.execute(QUERY, {'first_name': first_name, 'last_name': last_name, 'github': github})
    hackbright.db.session.commit()
    return "Successfully assigned new student %s %s to database. Github: %s" % (
        first_name, last_name, github)


@app.route("/student_form")
def show_student_form():
    """Add a student."""
    return render_template("student_add.html")


@app.route('/student_search')
def get_student_form():
    """Show form for searching for students."""

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github)
    return html


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
