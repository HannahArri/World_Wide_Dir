from flask import Flask, render_template
from queries import DB, Program

app = Flask(__name__)

@app.route("/stevens")
def stevens():
    DB_FILE = '/Users/jrr/Documents/Stevens/JonWWD/WWD.sqlite'

    db = DB(DB_FILE)

    with db.conn:
        data = [db.get_program('Stevens Institute of Technology').html()]

    return render_template('wwd.html',
                           title='WWD Organizations',
                           pgrms=data)

@app.route("/africa")
def africa():
    DB_FILE = '/Users/jrr/Documents/Stevens/JonWWD/WWD.sqlite'

    db = DB(DB_FILE)

    with db.conn:
        data = [pgrm.html() for pgrm in db.get_programs_continent('Africa')]

    return render_template('wwd.html',
                           title='WWD Organizations in Africa',
                           pgrms=data)

@app.route("/usa")
def usa():
    DB_FILE = '/Users/jrr/Documents/Stevens/JonWWD/WWD.sqlite'

    db = DB(DB_FILE)

    with db.conn:
        data = [pgrm.html() for pgrm in db.get_programs_country('USA')]

    return render_template('wwd.html',
                           title='WWD Organizations in USA',
                           pgrms=data)
app.run(debug=True)


if __name__ == '__main__':
    app.run(port=5000, debug=True)