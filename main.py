# Joseph Sumlin, Andy Kincheloe, Sahil Posa

import sqlite3
from database import Database
from schema import Schema
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)

conn = sqlite3.connect('flowershopdatabase.db', check_same_thread=False)
cursor = conn.cursor()
Schema.build(conn, cursor)
conn.close()

def get_db_connection():
    conn = sqlite3.connect('flowershopdatabase.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    customers = conn.execute("SELECT * FROM customer").fetchall()
    conn.close()
    return render_template('index.html', customers=customers)

app.run()
