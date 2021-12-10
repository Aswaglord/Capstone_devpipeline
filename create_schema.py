import sqlite3

connection = sqlite3.connect('competency_tracker.db')
cursor = connection.cursor()

# create database and tables with mock data, only run one time
def create_schema(cursor):
    with open('schema.sql') as my_file:
        sqlfile = my_file.read()
        cursor.executescript(sqlfile)
    connection.commit()

create_schema(cursor)