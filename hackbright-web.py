from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html", first=first, last=last, github=github, grades=grades)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def new_student_form():
    """Add a student."""

    return render_template("new_student.html")


@app.route("/student-processed", methods=['POST'])
def process_student():

    github = request.form.get('github')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')

    QUERY = """
            INSERT INTO students (github, first_name, last_name)
            VALUES (:github, :firstname, :lastname)"""

    hackbright.db.session.execute(QUERY, {'firstname': firstname, 'lastname': lastname, 'github': github})

    hackbright.db.session.commit()

    return render_template("student_processed.html", firstname=firstname, lastname=lastname, github=github)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
