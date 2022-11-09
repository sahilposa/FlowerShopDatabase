# Joseph Sumlin, Andy Kincheloe, Sahil Posa

import sqlite3
from schema import Schema

conn = sqlite3.connect('flowershopdatabase.db')
cursor = conn.cursor()
Schema.build(conn, cursor)
conn.close()
