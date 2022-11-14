# Joseph Sumlin, Andy Kincheloe, Sahil Posa

import sqlite3
from database import Database
from schema import Schema
from flask import Flask, render_template, request, url_for, flash, redirect
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = str(os.urandom(24).hex())

conn = sqlite3.connect('flowershopdatabase.db', check_same_thread=False)
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()
db = Database(conn,cursor)
Schema.build(conn, cursor)
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
    conn.close()
    return render_template('index.html')

@app.route("/customer")
def customers():
    conn = get_db_connection()
    db = Database(conn,cursor)
    customers = db.sort_filter('customer','customerID','DESC','lname','\'Kincheloe\'','=')
    return render_template('customer.html', customers=customers)


@app.route("/place-order", methods=("GET", "POST"))
def place_ord():
    conn = get_db_connection()
    cursor = conn.cursor()
    products = conn.execute("SELECT * FROM product")
    id = 1
    list = []
    if request.method == "POST":
        phone = request.form['phone']
        if not phone:
            phone = None
        elif cursor.execute("SELECT * FROM customer WHERE phone=?", (int(phone),)).fetchone() is None:
            flash("Phone not found")
            return render_template('placeOrder.html', products=products)
        else:
            phone=int(phone)
        for x in conn.execute("SELECT productID FROM product"):
            list.append(request.form[''+str(id)])
            id = id+1
        db = Database(conn, cursor)
        db.ord_transaction(phone, list)
        return redirect(url_for('index'))
    return render_template('placeOrder.html', products=products)

    
app.run(debug=True)




