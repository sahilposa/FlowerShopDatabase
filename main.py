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
        lname TEXT NOT NULL,
        phone INTEGER UNIQUE CHECK (phone>=1000000000 and phone<10000000000)
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


def is_num(testInput, type):
    if testInput is None:
        return False
    try:
        if type == "float":
            testFloat = float(testInput)
        elif type == "int":
            testInt = int(testInput)
        else:
            raise Exception("Invalid type.")
        return True
    except ValueError:
        return False


def is_pos(testInput, type):
    if type == "float" and float(testInput)<0:
        return False
    if type == "int" and int(testInput)<0:
        return False
    return True


def is_pos_num(testInput, type, varName):
    if not is_num(testInput, type) or not is_pos(testInput, type):
        print("Invalid input. " + varName + " must be a positive number.")
        return False
    return True


def add_emp(fname, lname, position, salary):
    if not is_pos_num(salary, "float", "Salary"):
        return
    if fname is None or lname is None or salary is None:
        print("Invalid input. First name, last name, and salary all require inputs.")
        return
    cursor.execute("""INSERT INTO employee (fname, lname, position, salary)
        VALUES (?, ?, ?, ?)""", (fname, lname, position, float(salary)))
    conn.commit()


def is_phone(phone):
    if phone is None:
        return False
    try:
        testInt = int(phone)
    except ValueError:
        return False
    if len(str(phone)) != 10:
        return False
    return True


def is_phone_unique(phone):
    cursor.execute("SELECT * FROM customer WHERE phone=?", (phone,))
    if cursor.fetchone() is None:
        return True
    return False


def add_cus(fname, lname, phone):
    if not is_phone(phone):
        print("Invalid input. Phone number must be a 10 digit number formatted 1234567890.")
        return
    if not is_phone_unique(phone):
        print("Invalid input. Phone number already exists.")
        return
    if fname is None or lname is None:
        print("Invalid input. First and last name required.")
        return
    cursor.execute("INSERT INTO customer (fname, lname, phone) VALUES (?, ?)", (fname, lname, int(phone)))
    conn.commit()


def add_prod(p_desc, price, stock):
    if not is_pos_num(price, "float", "Price"):
        return
    if not is_pos_num(stock, "int", "Stock"):
        return
    if p_desc is None:
        print("Invalid input. Product description required.")
        return
    cursor.execute("INSERT INTO product (p_desc, price, stock) VALUES (?, ?, ?)", (p_desc, float(price), int(stock)))
    conn.commit()


def add_ord(customerID, employeeID, total):
    if not is_pos_num(total, "float", "Total"):
        return
    if not is_pos_num(customerID, "int", "customerID"):
        return
    if not is_pos_num(employeeID, "int", "employeeID"):
        return
    customerID = int(customerID)
    employeeID = int(employeeID)
    cursor.execute("SELECT customerID FROM customer WHERE customerID=?", (customerID,))
    if cursor.fetchone() is None:
        print("CustomerID does not exist. Setting to NULL.")
        customerID = None
    cursor.execute("SELECT employeeID FROM employee WHERE employeeID=?", (employeeID,))
    if cursor.fetchone() is None:
        print("EmployeeID does not exist. Setting to NULL.")
        employeeID = None
    cursor.execute("INSERT INTO orders (customerID, employeeID, total) VALUES (?, ?, ?)", (customerID, employeeID, float(total)))
    conn.commit()


conn.close()
