""" Extract the data from the WWD Sqlite3 database to recreate the WWD directory """

import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'WWD.sqlite')

def n2br(s):
    """ replace \n with <br> for adding a break in Flask """
    return s.replace("\n", "<br>")

class Program:
    """ Gather all of information about a program """
    def __init__(self, org, school, continent, country, address="", city="", state="", zip=""):
        self.org = org
        self.school = school
        self.continent = continent
        self.country = country
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip

        self.urls = list()  # list of strings of urls

        self.contacts = list() # list of class Contact

        self.degrees = list() # list of strings

        self.logo = None # path for logo

    def addr_str(self):
        addr_blk =  "{}\n{}\n".format(self.school, self.address)

        if self.city != "" and self.state != "":
            addr_blk += "{}, {}".format(self.city, self.state)
        elif self.city != "" and self.state == "":
            addr_blk += "{}".format(self.city)
        elif self.city == "" and self.state != "":
            addr_blk += "{}".format(self.state)

        if self.zip:
            addr_blk += " {}".format(self.zip)

        if self.country != "":
            addr_blk += ", {}".format(self.country)

        return addr_blk

    def urls_str(self):
        return "\n".join(self.urls)

    def contacts_str(self):
        return "\n\n".join([str(contact) for contact in self.contacts])

    def degrees_str(self):
        return "\n".join([str(deg) for deg in self.degrees])

    def logo_str(self):
        return "\n".join([str(logo) for logo in self.logo])

    def __str__(self):
        """ format a program in the appropriate format including all data as a single, multiline string """
        return "{}\n\n{}\n\n{}\n\n{}\n\n{}\n".format(self.org, self.addr_str(), self.urls_str(), self.contacts_str(), self.degrees_str())

    def html(self):
        """ return the various fields as JSON ready to present in HMTL
            newlines are replaced by <br> to format properly in HTML/Flask
        """
        return {'org': n2br(self.org),
                'continent': n2br(self.continent), 
                'school': n2br(self.school), 
                'country': n2br(self.country), 
                'addr': n2br(self.addr_str()),
                'urls': n2br(self.urls_str()),
                'contacts': n2br(self.contacts_str()),
                'degrees': n2br(self.degrees_str()),
                'logo': n2br(self.logo_str())}


class Contact:
    """ a WWD contact """
    def __init__(self, org, prefix, first_name, last_name, suffix="", title="", email="", dept="", office="", phone=""):
        self.org = org
        self.prefix = prefix
        self.first_name = first_name
        self.last_name = last_name
        self.suffix = suffix
        self.title = title
        self.email = email
        self.dept = dept
        self.office = office
        self.phone = phone

    def __str__(self):
        name = "{} {}, {}, {}".format(self.first_name, self.last_name, self.suffix, self.title)

        dept = ""
        if self.dept:
            dept = "{}\n".format(self.dept)

        email = ""
        if self.email:
            email = "Email: {}\n".format(self.email)

        phone = ""
        if self.phone:
            phone = "Phone: {}".format(self.phone)

        return "{}{}{}{}".format(name, dept, email, phone)


class Degree:
    """ Degree offered by an org """
    def __init__(self, level, desc=""):
        self.level = level
        self.desc = desc

    def __str__(self):
        return self.desc


class DB:
    """ manage the database connection and queries """
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def get_continents(self):
        """ return the list strings of continents """
        query = "select continent from orgs group by continent order by continent"
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()
        return [result[0] for result in results]

    def get_countries(self):
        """ return a list of countries as strings """
        query = "select distinct(country) from orgs order by country collate nocase"
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()
        return [result[0] for result in results]

    def get_orgs(self):
        """ return a list of organizations as strings """
        query = "select distinct(org) from orgs order by org"
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()
        return [result[0] for result in results]

    def get_programs_continent(self, continent):
        """ return a list of Programs for by continent """
        query = "select org from orgs where continent='{}' collate nocase".format(continent)
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()

        return [self.get_program(result[0]) for result in results]

    def get_records(self):
        query = "select org from orgs"

        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()

        return [self.get_program(result[0]) for result in results]

    def get_programs_degree(self, degree):
        """ return a list of Programs for by continent """
        query = "select org from degrees where level='{}' collate nocase".format(degree)
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()

        return [self.get_program(result[0]) for result in results]

    def get_programs_country(self, country):
        """ return a list of Programs for by country """
        query = "select org from orgs where country='{}' collate nocase".format(country)
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()

        return [self.get_program(result[0]) for result in results]

    def get_program(self, org):
        """ Retrieve a specific org and all of its data from the database
            Return and instance of class Program to reflect the data or return None
        """

        query = 'select org, school, continent, country, address, city, state, zip\
                   from orgs where org="{}" collate nocase'.format(org)
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()

        pgrm = None
        if results:
            # assert 0 <= len(results) <= 1
            org, school, continent, country, address, city, state, zip = results[0]
            pgrm = Program(org, school, continent, country, address, city, state, zip)

            pgrm.urls = self.get_urls(org)
            pgrm.contacts = self.get_contacts(org)
            pgrm.degrees = self.get_degrees(org)
            pgrm.logo = self.get_logo(org)
        
        return pgrm

    def get_contacts(self, org):
        """ Retrieve a list of contacts for a specific org 
        """
        query = 'select org, prefix, first_name, last_name, suffix, title, email1, dept, office, phone\
                   from contacts where org="{}" collate nocase'.format(org)
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()

        contacts = [Contact(org, prefix, first_name, last_name, suffix, title, email1, dept, office, phone) \
                    for org, prefix, first_name, last_name, suffix, title, email1, dept, office, phone in results]

        return contacts
    
    def get_degrees(self, org):
        """ Retrieve a the contacts for a specific org and all of its data from the database
            Return a list of instances of class Contact to reflect the data or return None
        """
        query = 'select degree from degrees where org="{}" order by level collate nocase'.format(org)
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()
        # results is a list of tuples of length 1
        return [result[0] for result in results]

    def get_urls(self, org):
        """ Retrieve a list of urls for a specific org 
        """
        query = 'select url from urls where org="{}"'.format(org)
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()
        # results is a list of tuples of length 1
        return [result[0] for result in results]

    def get_logo(self, org):
        """retrieve logo name for a specific org"""
        query = 'select logo_name from logos where org="{}"'.format(org)
        c = self.conn.cursor()
        c.execute(query)
        results = c.fetchall()

        return [result[0] for result in results]



def main():
    db = DB(DB_FILE)

    with db.conn:

        # example of working with a single Program and printing the individual pieces
        print('--------------')
        print("Example printing components")
        stevens = db.get_program('Stevens Institute of Technology')
        print("HTML:", stevens.html())
        print("Org:\n{}\n".format(stevens.org))  # name of the organization
        print("Address:\n{}\n".format(stevens.addr_str())) # multiline string from the top of the description
        print("URLs:\n{}\n".format(stevens.urls_str()))  # multiline string with the URLs
        print("Contacts:\n{}\n".format(stevens.contacts_str()))  # multiline string with the contacts section
        print("Degrees:\n{}\n".format(stevens.degrees_str()))  # multiline string with the degrees offered

        # or you can print the whole thing at once
        print('--------------')
        print("Example: Stevens all at once:")
        print("{}\n".format(str(stevens)))

        # here's a really big description
        print('--------------')
        print("Example: big description:\n")
        joburg = db.get_program('University of Johannesburg')
        print(str(joburg))

        """ I'm using the following for testing and cleaning up the database 
        # print all programs by continent
        for continent in db.get_continents()
            for pgrm in db.get_programs_continent(continent):  
                print('---------------------')   
                print(str(pgrm))
        """
        

if __name__ == '__main__':
    main()
    
