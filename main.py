#Joseph Sumlin, Andy Kincheloe, Sahil Posa
import sqlite3
conn = sqlite3.connect('flowershopdatabase.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE product (
        productID INTEGER PRIMARY KEY,
        p_desc TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL CHECK (stock>=0)
    )""")
cursor.execute("""CREATE TABLE customer(
        customerID INTEGER PRIMARY KEY,
        fname TEXT NOT NULL,
        lname TEXT NOT NULL
    )""")
cursor.execute("""CREATE TABLE employee(
        employeeID INTEGER PRIMARY KEY,
        fname TEXT NOT NULL,
        lname TEXT NOT NULL,
        position TEXT,
        salary REAL NOT NULL CHECK (salary>=0)
    )""")
cursor.execute("""CREATE TABLE orders(
        orderID INTEGER PRIMARY KEY,
        customerID INTEGER,
        employeeID INTEGER,
        total NOT NULL CHECK (total>=0),
        FOREIGN KEY (customerID)
            REFERENCES customer (customerID)
            ON DELETE SET NULL,
        FOREIGN KEY (employeeID)
            REFERENCES employee (employeeID)
            ON DELETE SET NULL
    )""")
cursor.execute("""CREATE TABLE purchase(
        orderID INTEGER NOT NULL,
        productID INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity>0),
        PRIMARY KEY(orderID, productID)
        FOREIGN KEY (orderID)
            REFERENCES orders (orderID)
            ON DELETE CASCADE,
        FOREIGN KEY (productID)
            REFERENCES product (productID)
            ON DELETE CASCADE
    )""")
conn.commit()
conn.close()