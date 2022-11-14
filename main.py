# Joseph Sumlin, Andy Kincheloe, Sahil Posa

import sqlite3
from database import Database
from schema import Schema
from flask import Flask, render_template, request, url_for, flash, redirect
import os
from checks import Checks

app = Flask(__name__)
app.config["SECRET_KEY"] = str(os.urandom(24).hex())

conn = sqlite3.connect('flowershopdatabase.db', check_same_thread=False)
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()
db = Database(conn,cursor)
Schema.build(conn, cursor)
conn.commit()

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

# retrieves tables for list pages
def get_table(table_name, db, filt_attr, op, value, sort_attr, asc):
    filt_blank = Checks.is_filt_blank(filt_attr, op, value)
    sort_blank = Checks.is_sort_blank(sort_attr, asc)
    if filt_blank and sort_blank:
        return db.conn.execute("SELECT * FROM " + table_name).fetchall()
    elif not filt_blank and sort_blank:
        return db.filter_table(table_name, filt_attr, value, op)
    elif filt_blank and not sort_blank:
        return db.sort_table(table_name, sort_attr, asc)
    else:
        return db.sort_filter(table_name, sort_attr, asc, filt_attr, value, op)


@app.route("/customer", methods=("GET", "POST"))
def customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    db = Database(conn,cursor)
    customers = conn.execute("SELECT * FROM customer").fetchall()
    if request.method == "POST":
        if request.form.get('sort') == 'sort':
            filt_attr = request.form["filt_attr"]
            op = request.form["op"]
            value = request.form["value"]
            sort_attr = request.form["sort_attr"]
            asc = request.form["asc"]
            if not Checks.sort_filt_valid(filt_attr, op, value, sort_attr, asc):
                return render_template('customer.html', customers=customers)
            customers = get_table("customer", db, filt_attr, op, value, sort_attr, asc)
            return render_template('customer.html', customers=customers)
        elif request.form.get('add') == 'add':
            lname = request.form["lname"]
            fname = request.form["fname"]
            phone = request.form["phone"]
            if not (Checks.is_phone_unique(phone, cursor)):
                x = conn.execute("SELECT customerID FROM customer where phone = "+phone).fetchall()[0][0]
                db.upd_cus(x,fname,lname,phone)
            else:
                db.add_cus(fname,lname,phone)
            customers = conn.execute("SELECT * FROM customer").fetchall()
            return render_template('customer.html', customers=customers)
        elif request.form.get('del') == 'del':
            phone = request.form["phone2"]
            if not (Checks.is_phone_unique(phone, cursor)):
                customerID = conn.execute("SELECT customerID FROM customer where phone = "+phone).fetchall()[0][0]
                db.del_cus(customerID)
            customers = conn.execute("SELECT * FROM customer").fetchall()
            return render_template('customer.html', customers=customers)
    return render_template('customer.html', customers=customers)


@app.route("/employee", methods=("GET", "POST"))
def employee():
    conn = get_db_connection()
    cursor = conn.cursor()
    db = Database(conn, cursor)
    employees = conn.execute("SELECT * FROM employee").fetchall()
    if request.method == "POST":
        if request.form.get('sort') == 'sort':
            filt_attr = request.form["filt_attr"]
            op = request.form["op"]
            value = request.form["value"]
            sort_attr = request.form["sort_attr"]
            asc = request.form["asc"]
            if not Checks.sort_filt_valid(filt_attr, op, value, sort_attr, asc):
                return render_template('employee.html', employees=employees)
            employees = get_table("employee", db, filt_attr, op, value, sort_attr, asc)
            return render_template("employee.html", employees=employees)
        elif request.form.get('add') == 'add':
            lname = request.form["lname"]
            fname = request.form["fname"]
            position = request.form["position"]
            salary = request.form["salary"]
            if not (Checks.is_employee_exist(fname,lname,cursor)):
                x = conn.execute("SELECT employeeID FROM employee where fname=? and lname=?",(fname,lname)).fetchall()[0][0]
                db.upd_emp(x,fname,lname,position,salary)
            else:
                db.add_emp(fname,lname,position,salary)
            employees = conn.execute("SELECT * FROM employee").fetchall()
            return render_template("employee.html", employees=employees)
        elif request.form.get('del') == 'del':
            lname = request.form["lname2"]
            fname = request.form["fname2"]
            if not (Checks.is_employee_exist(fname,lname,cursor)):
                employeeID = conn.execute("SELECT employeeID FROM employee where fname=? and lname=?",(fname,lname)).fetchall()[0][0]
                db.del_emp(employeeID)
            employees = conn.execute("SELECT * FROM employee").fetchall()
            return render_template("employee.html", employees=employees)
    return render_template("employee.html", employees=employees)


@app.route("/products", methods=("GET", "POST"))
def product():
    conn = get_db_connection()
    cursor = conn.cursor()
    db= Database(conn, cursor)
    products = conn.execute("SELECT * FROM product").fetchall()
    if request.method == "POST":
        if request.form.get('sort') == 'sort':
            filt_attr = request.form["filt_attr"]
            op = request.form["op"]
            value = request.form["value"]
            sort_attr = request.form["sort_attr"]
            asc = request.form["asc"]
            if not Checks.sort_filt_valid(filt_attr, op, value, sort_attr, asc):
                return render_template('products.html', products=products)
            products = get_table("product", db, filt_attr, op, value, sort_attr, asc)
            return render_template("products.html", products=products)
        elif request.form.get('add') == 'add':
            product = request.form["product"]
            price = request.form["price"]
            quantity = request.form["quantity"]
            if not (Checks.is_product_exist(product,cursor)):
                productID = conn.execute("SELECT productID FROM product where p_desc=?",(product,)).fetchall()[0][0]
                db.upd_prod(productID,product,price,quantity)
            else:
                db.add_prod(product,price,quantity)
            products = conn.execute("SELECT * FROM product").fetchall()
            return render_template("products.html", products=products)
        elif request.form.get('del') == 'del':
            product = request.form["product2"]
            if not (Checks.is_product_exist(product,cursor)):
                productID = conn.execute("SELECT productID FROM product where p_desc=?",(product,)).fetchall()[0][0]
                db.del_prod(productID)
            products = conn.execute("SELECT * FROM product").fetchall()
            return render_template("products.html", products=products)
    return render_template("products.html", products=products)


@app.route("/orders", methods=("GET", "POST"))
def orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    db = Database(conn, cursor)
    orders = conn.execute("SELECT * FROM orders").fetchall()
    if request.method == "POST":
        if request.form.get('sort') == 'sort':
            filt_attr = request.form["filt_attr"]
            op = request.form["op"]
            value = request.form["value"]
            sort_attr = request.form["sort_attr"]
            asc = request.form["asc"]
            if not Checks.sort_filt_valid(filt_attr, op, value, sort_attr, asc):
                return render_template('orders.html', orders=orders)
            orders = get_table("orders", db, filt_attr, op, value, sort_attr, asc)
            return render_template("orders.html", orders=orders)
        elif request.form.get('add') == 'add':
            orderID = request.form["orderID"]
            customerID = request.form["customerID"]
            employeeID = request.form["employeeID"]
            total = request.form["total"]
            if (not Checks.is_customerID_exist(customerID,cursor)) and (not Checks.is_employeeID_exist(employeeID,cursor)):
                if not (Checks.is_order_exist(orderID,cursor)):
                    db.upd_ord(int(orderID),int(customerID),int(employeeID),float(total))
                else:
                    db.add_ord(int(customerID),int(employeeID),float(total))
            orders = conn.execute("SELECT * FROM orders").fetchall()
            return render_template("orders.html", orders=orders)
        elif request.form.get('del') == 'del':
            orderID = request.form["orderID2"]
            if not (Checks.is_order_exist(orderID,cursor)):
                db.del_ord(int(orderID))
            orders = conn.execute("SELECT * FROM orders").fetchall()
            return render_template("orders.html", orders=orders)
    return render_template("orders.html", orders=orders)


@app.route("/purchase", methods=("GET", "POST"))
def purchase():
    conn = get_db_connection()
    cursor = conn.cursor()
    db = Database(conn, cursor)
    purchases = conn.execute("SELECT * FROM purchase").fetchall()
    if request.method == "POST":
        filt_attr = request.form["filt_attr"]
        op = request.form["op"]
        value = request.form["value"]
        sort_attr = request.form["sort_attr"]
        asc = request.form["asc"]
        if not Checks.sort_filt_valid(filt_attr, op, value, sort_attr, asc):
            return render_template('purchase.html', purchases=purchases)
        purchases = get_table("purchase", db, filt_attr, op, value, sort_attr, asc)
    return render_template("purchase.html", purchases=purchases)


@app.route("/place-order", methods=("GET", "POST"))
def place_ord():
    conn = get_db_connection()
    cursor = conn.cursor()
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
conn.close()




