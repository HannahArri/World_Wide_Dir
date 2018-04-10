import sqlite3
import queries
import os

sqlite_file = os.path.join(os.path.dirname(__file__), 'WWD.sqlite')
db = queries.DB(sqlite_file)

class Temp_org():
    def __init__(self, org, sch, add, city, st, zp, cntry, cname, ctitle, email, pnum, dtype, dtitle):
        self.org_name = org
        self.school_name = sch
        self.address1 = add
        self.city = city
        self.state = st
        self.zip = zp
        self.country = cntry
        self.contact_name = cname
        self.contact_title = ctitle
        self.email = email
        self.phone_no = pnum
        self.degree_type = dtype
        self.degree_title = dtitle

    def insert(self):
        query='''INSERT INTO temp( org_name, school_name, address, city, state, country, cname,
        ctitle, email, phoneno, level, degree, url, logo)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        data=(self.org_name,self.school_name, self.address1, self.city, self.state, self.country, self.contact_name,
                         self.contact_title, self.email, self.phone_no, self.degree_type,self.degree_title, "", "" )
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute(query, data)
        conn.commit()



def get_all_records():
    db = queries.DB(sqlite_file)
    with db.conn:
        data = [prgm.html() for prgm in db.get_records()]
    return data


def get_continents():
    db = queries.DB(sqlite_file)
    with db.conn:
        results = db.get_continents()

    return results


def get_programs_continent(continent):
    db = queries.DB(sqlite_file)
    with db.conn:
        results = [prgm.html() for prgm in db.get_programs_continent(continent=continent)]
    return results


def search_country(country):
    db = queries.DB(sqlite_file)
    with db.conn:
        results = [ prgm.html() for prgm in db.get_programs_country(country)]

    return results


def search_degree(degree):
    db = queries.DB(sqlite_file)
    with db.conn:
        results = [prgm.html() for prgm in db.get_programs_degree(degree)]
    return results


def search_organization(org):
    db = queries.DB(sqlite_file)
    with db.conn:
        results = [db.get_program(org).html()]
        print(results)
    return results

def search_contact():
    pass
