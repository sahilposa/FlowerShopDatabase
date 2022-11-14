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
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()
db = Database(conn,cursor)
Schema.build(conn, cursor)
db.add_cus('Andy','Not',9999999999)
conn.close()


def get_db_connection():
    conn = sqlite3.connect('flowershopdatabase.db', check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = 1")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    db = Database(conn,cursor)
    customers = db.sort_filter('customer','customerID','DESC','lname','\'Kincheloe\'','=')
    conn.close()
    return render_template('index.html', customers=customers)


@app.route("/place-order", methods=("GET", "POST"))
def place_ord():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM product")
    if request.method == "POST":
        print("in post")
        roses = request.form['1']
        flower2 = request.form['2']
        flower3 = request.form['3']
        flower4 = request.form['4']
        flower5 = request.form['5']
        print(roses)
        redirect(url_for('index'))
    return render_template('placeOrder.html', products=products)

    
app.run()




