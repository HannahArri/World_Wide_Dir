from flask import Flask, render_template, request
import DbCalls
import collections
import jinja2

app = Flask(__name__)


@app.route('/')
def index():
    data = DbCalls.get_continients()
    return render_template('Index.html', title='World Wide Directory', programs=data)


@app.route('/search', methods=['POST'])
def get_programs():
    if request.method == 'POST':
        value = request.form['searchitem']
        search_criteria = request.form['searchcriteria']
        print(search_criteria + ":" + value)
        if search_criteria == 'Continent':
            data = DbCalls.get_programs_continent(value)
        elif search_criteria == 'Organization':
            data = DbCalls.search_organization(value)
        elif search_criteria == 'Country':
            data = DbCalls.search_country(value)
        elif search_criteria == 'Degree':
            data = DbCalls.search_degree(value)

    return render_template('Program.html', title="World Wide Directory", programs=data)


@app.route('/continent/<string:value>', methods=['POST'])
def get_continent_programs(value):
    data = DbCalls.get_programs_continent(value)
    return render_template('Program.html', title='World Wide Directory', programs=data)


app.run(debug=True)