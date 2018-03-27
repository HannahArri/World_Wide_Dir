import sqlite3
import queries

sqlite_file = '/home/hannah/World_Wide_Dir/WWD.sqlite'
db = queries.DB(sqlite_file)

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
