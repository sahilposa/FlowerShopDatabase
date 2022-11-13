# Joseph Sumlin, Andy Kincheloe, Sahil Posa
def get_db_connection():
    conn = sqlite3.connect('flowershopdatabase.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

import sqlite3
from database import Database
from schema import Schema
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
from database import Database

conn = sqlite3.connect('flowershopdatabase.db', check_same_thread=False)
cursor = conn.cursor()
db = Database(conn,cursor)
Schema.build(conn, cursor)
conn.close()
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    db = Database(conn,cursor)
    customers = db.sort_table('customer','fname','ASC')
    conn.close()
    return render_template('index.html', customers=customers)

app.run()




