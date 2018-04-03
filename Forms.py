from wtforms import Form, StringField, validators

class Organization_Form(Form):
    org_name = StringField('University Name', [validators.DataRequired()])
    school_name = StringField('School Name', [validators.DataRequired()])
    address1 = StringField('Address', [validators.DataRequired()])
    city = StringField('City')
    state = StringField('State')
    zip = StringField('Zip code')
    country = StringField('Country')
    contact_name = StringField('Contact Name', [validators.DataRequired()])
    contact_title = StringField('Contact Title', [validators.DataRequired()])
    email = StringField('Email')
    phone_no = StringField('Phone Number')
    degree_type = StringField('Degree Type', [validators.DataRequired()])
    degree_title = StringField('Degree Title', [validators.DataRequired()])