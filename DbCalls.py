import sqlite3
import queries

sqlite_file = '/home/hannah/World_Wide_Dir/WWD.sqlite'
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
        query="insert into temp('org_name', 'school_name', 'address', 'city'," \
              "'state', 'country', 'cname', 'ctitle', 'email', 'phoneno', 'level', 'degree', 'url', 'logo') " \
              "values('{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')" \
              "".format(self.org_name,self.school_name, self.address1, self.city, self.state, self.country,
                         self.contact_name, self.contact_title, self.email, self.phone_no, self.degree_type,
                         self.degree_title, "", "" )
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute(query)
        print(c.lastrowid)

def getrecords():
    query = """select * from WWD Order By Continent;"""

    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    executed_query = c.execute(query)
    results = c.fetchall()
    col_name = [name[0] for name in executed_query.description]

    # convert the query results into a list of dictionaries to pass to the template
    data = [dict(zip(col_name, r)) for r in results]

    conn.close()  # close the connection to close the database
    return data

def get_continients():
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
