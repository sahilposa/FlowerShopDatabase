# Joseph Sumlin, Andy Kincheloe, Sahil Posa

import sqlite3
from schema import Schema
from database import Database

conn = sqlite3.connect('flowershopdatabase.db')
cursor = conn.cursor()
db = Database(conn,cursor)
Schema.build(conn, cursor)
db.upd_ord(1,1,1,70.97)
conn.close()
