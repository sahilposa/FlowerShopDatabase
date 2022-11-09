from checks import Checks


class Database:

    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def add_emp(self, fname, lname, position, salary):
        if not Checks.is_pos_num(salary, "float", "Salary"):
            return
        if fname is None or lname is None or salary is None:
            print("Invalid input. First name, last name, and salary all require inputs.")
            return
        self.cursor.execute("""INSERT INTO employee (fname, lname, position, salary)
            VALUES (?, ?, ?, ?)""", (fname, lname, position, float(salary)))
        self.conn.commit()

    def add_cus(self, fname, lname, phone):
        if not Checks.is_phone(phone):
            print("Invalid input. Phone number must be a 10 digit number formatted 1234567890.")
            return
        if not Checks.is_phone_unique(phone, self.cursor):
            print("Invalid input. Phone number already exists.")
            return
        if fname is None or lname is None:
            print("Invalid input. First and last name required.")
            return
        self.cursor.execute("INSERT INTO customer (fname, lname, phone) VALUES (?, ?)", (fname, lname, int(phone)))
        self.conn.commit()

    def add_prod(self, p_desc, price, stock):
        if not Checks.is_pos_num(price, "float", "Price"):
            return
        if not Checks.is_pos_num(stock, "int", "Stock"):
            return
        if p_desc is None:
            print("Invalid input. Product description required.")
            return
        self.cursor.execute("INSERT INTO product (p_desc, price, stock) VALUES (?, ?, ?)",
                       (p_desc, float(price), int(stock)))
        self.conn.commit()

    def add_ord(self, customerID, employeeID, total):
        if not Checks.is_pos_num(total, "float", "Total"):
            return
        if not Checks.is_pos_num(customerID, "int", "customerID"):
            return
        if not Checks.is_pos_num(employeeID, "int", "employeeID"):
            return
        customerID = int(customerID)
        employeeID = int(employeeID)
        self.cursor.execute("SELECT customerID FROM customer WHERE customerID=?", (customerID,))
        if self.cursor.fetchone() is None:
            print("CustomerID does not exist. Setting to NULL.")
            customerID = None
        self.cursor.execute("SELECT employeeID FROM employee WHERE employeeID=?", (employeeID,))
        if self.cursor.fetchone() is None:
            print("EmployeeID does not exist. Setting to NULL.")
            employeeID = None
        self.cursor.execute("INSERT INTO orders (customerID, employeeID, total) VALUES (?, ?, ?)",
                       (customerID, employeeID, float(total)))
        self.conn.commit()