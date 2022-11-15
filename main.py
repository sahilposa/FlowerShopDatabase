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
@app.route("/about")
def about():
    conn = get_db_connection()
    cursor = conn.cursor()
    conn.close()
    return render_template('about.html')

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
            customerID = request.form["customerID"]
            lname = request.form["lname"]
            fname = request.form["fname"]
            phone = request.form["phone"]
            if not customerID:
                if not lname or not fname or not phone:
                    flash("Last, first, and phone all required for adding.")
                    return render_template("customer.html", customers=customers)
                if Checks.is_phone_unique(phone, cursor):
                    db.add_cus(fname, lname, phone)
                else:
                    flash("Phone number already on file.")
                    return render_template("customer.html", customers=customers)
            elif cursor.execute("SELECT * FROM customer WHERE customerID=?", (customerID,)).fetchone() is None:
                flash("Customer ID does not exist. Only fill customer ID field for updating.")
                return render_template("customer.html", customers=customers)
            else:
                if not lname:
                    lname = None
                if not fname:
                    fname = None
                if not phone:
                    phone = None
                if phone is not None and not Checks.is_phone_unique(phone, cursor):
                    flash("Phone number already on file.")
                    return render_template("customer.html", customers=customers)
                db.upd_cus(customerID, fname, lname, phone)
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
            employeeID = request.form["employeeID"]
            lname = request.form["lname"]
            fname = request.form["fname"]
            position = request.form["position"]
            salary = request.form["salary"]
            if not employeeID:
                if not lname or not fname or not position or not salary:
                    flash("Last, First, Position, and Salary all required for adding.")
                    return render_template("employee.html", employees=employees)
                db.add_emp(fname, lname, position, salary)
            elif cursor.execute("SELECT * FROM employee WHERE employeeID=?", (employeeID,)).fetchone() is None:
                flash("Employee ID does not exist. Only fill employee ID field for updating.")
                return render_template("employee.html", employees=employees)
            else:
                if not lname:
                    lname = None
                if not fname:
                    fname = None
                if not position:
                    position = None
                if not salary:
                    salary = None
                db.upd_emp(employeeID, fname, lname, position, salary)
            employees = conn.execute("SELECT * FROM employee").fetchall()
            return render_template("employee.html", employees=employees)
        elif request.form.get('del') == 'del':
            employeeID = request.form["employeeID2"]
            if cursor.execute("SELECT * FROM employee WHERE employeeID=?", (employeeID,)).fetchone() is not None:
                db.del_emp(employeeID)
            else:
                flash("Employee ID does not exist.")
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
            productID = request.form["productID"]
            product = request.form["product"]
            price = request.form["price"]
            quantity = request.form["quantity"]
            if not productID:
                if not product or not price or not quantity:
                    flash("Product, price, and quantity all required for adding.")
                    return render_template("products.html", products=products)
                db.add_prod(product, price, quantity)
            elif cursor.execute("SELECT * FROM product WHERE productID=?", (productID,)).fetchone() is None:
                flash("Product ID does not exist. Only fill product ID field for updating.")
                return render_template("products.html", products=products)
            else:
                if not product:
                    product = None
                if not price:
                    price = None
                if not quantity:
                    quantity = None
                db.upd_prod(productID,product,price,quantity)
            products = conn.execute("SELECT * FROM product").fetchall()
            return render_template("products.html", products=products)
        elif request.form.get('del') == 'del':
            productID = request.form["productID2"]
            if cursor.execute("SELECT * FROM product WHERE productID=?", (productID,)).fetchone() is not None:
                db.del_prod(productID)
            else:
                flash("Product ID does not exist.")
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
            if not customerID:
                customerID = None
            if not employeeID:
                employeeID = None
            if not orderID:
                flash("Order # required for updates.")
                return render_template("orders.html", orders=orders)
            if customerID is None or not Checks.is_customerID_exist(customerID,cursor):
                if employeeID is None or not Checks.is_employeeID_exist(employeeID,cursor):
                    if not (Checks.is_order_exist(orderID,cursor)):
                        db.upd_ord(orderID ,customerID, employeeID)
                    else:
                        flash("Order # does not exist.")
                        return render_template("orders.html", orders=orders)
                else:
                    flash("Employee ID does not exist.")
                    return render_template("orders.html", orders=orders)
            else:
                flash("Customer ID does not exist.")
                return render_template("orders.html", orders=orders)
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
        if request.form.get('sort') == 'sort':
            filt_attr = request.form["filt_attr"]
            op = request.form["op"]
            value = request.form["value"]
            sort_attr = request.form["sort_attr"]
            asc = request.form["asc"]
            if not Checks.sort_filt_valid(filt_attr, op, value, sort_attr, asc):
                return render_template('purchase.html', purchases=purchases)
            purchases = get_table("purchase", db, filt_attr, op, value, sort_attr, asc)
            return render_template("purchase.html", purchases=purchases)
        elif request.form.get('add') == 'add':
            orderID = request.form["orderID"]
            productID = request.form["productID"]
            quantity = request.form["quantity"]
            if (not Checks.is_order_exist(orderID,cursor)) and (not Checks.is_productID_exist(productID,cursor)):
                if not (Checks.is_purchase_exist(orderID,productID,cursor)):
                    db.upd_pur(orderID,productID,quantity)
                else:
                    flash("Purchase does not exist.")
                    return render_template("purchase.html", purchases=purchases)
            purchases = conn.execute("SELECT * FROM purchase").fetchall()
            return render_template("purchase.html", purchases=purchases)
        elif request.form.get('del') == 'del':
            orderID = request.form["orderID2"]
            productID = request.form["productID2"]
            if not (Checks.is_purchase_exist(orderID,productID,cursor)):
                db.del_pur(orderID,productID)
            purchases = conn.execute("SELECT * FROM purchase").fetchall()
            return render_template("purchase.html", purchases=purchases)
    return render_template("purchase.html", purchases=purchases)


@app.route("/place-order", methods=("GET", "POST"))
def place_ord():
    conn = get_db_connection()
    cursor = conn.cursor()
    products = conn.execute("SELECT * FROM product")
    id = 1
    list = []
    if request.method == "POST":
        phone = request.form['phone']
        employeeID = request.form['employeeID']
        if not employeeID:
            employeeID = None
        elif cursor.execute("SELECT * FROM employee WHERE employeeID=?",
                            (int(employeeID),)).fetchone() is None:
            flash("EmployeeID not found")
            return render_template('placeOrder.html', products=products)
        else:
            employeeID=int(employeeID)
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
        db.ord_transaction(phone,employeeID, list)
        return redirect(url_for('index'))
    return render_template('placeOrder.html', products=products)

    
app.run(debug=True)
conn.close()




