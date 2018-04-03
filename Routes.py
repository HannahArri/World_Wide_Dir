from flask import Flask, render_template, request, redirect, url_for
import DbCalls
from Forms import Organization_Form

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
        if search_criteria == 'Continent':
            data = DbCalls.get_programs_continent(value)
        elif search_criteria == 'Organization':
            data = DbCalls.search_organization(value)
        elif search_criteria == 'Country':
            data = DbCalls.search_country(value)
        elif search_criteria == 'Degree':
            data = DbCalls.search_degree(value)

    return render_template('Program.html', title="World Wide Directory", programs=data)


@app.route('/add', methods=['Post', 'Get'])
def add_org():
    form = Organization_Form(request.form)
    if form.validate() and request.method == 'POST':
        org_name =form.org_name.data
        sch=form.school_name.data
        add =form.address1.data
        city =form.city.data
        state = form.state.data
        zip = form.zip.data
        country = form.country
        cname = form.contact_name
        ctitle = form.contact_title
        email = form.email
        pnum = form.phone_no.data
        dtype = form.degree_type.data
        dtitle = form.degree_title.data

        data = DbCalls.Temp_org(org_name, sch, add, city, state, zip, country, cname, ctitle, email, pnum, dtype, dtitle)
        data.insert()

        return redirect(url_for('index'))

    return render_template('Form.html', form = form)

# @app.route('/add', methods = ['Post', 'Get'])
# def add():
#     return render_template('Form.html' )

# @app.route('/continent/<string:value>', methods=['POST'])
# def get_continent_programs(value):
#     data = DbCalls.get_programs_continent(value)
#     return render_template('Program.html', title='World Wide Directory', programs=data)


app.run(debug=True)