# Joseph Sumlin, Andy Kincheloe, Sahil Posa

import sqlite3
from schema import Schema
from database import Database

conn = sqlite3.connect('flowershopdatabase.db')
cursor = conn.cursor()
db = Database(conn,cursor)
Schema.build(conn, cursor)
conn.close()
