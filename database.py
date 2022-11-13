from checks import Checks


class Database:
    #constructor
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
    #insert function for employee table
    def add_emp(self, fname, lname, position, salary):
        if not Checks.is_pos_num(salary, "float", "Salary"):
            return
        if fname is None or lname is None or salary is None:
            print("Invalid input. First name, last name, and salary all require inputs.")
            return
        self.cursor.execute("""INSERT INTO employee (fname, lname, position, salary)
            VALUES (?, ?, ?, ?)""", (fname, lname, position, float(salary)))
        self.conn.commit()
    #insert function for customer table
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
        self.cursor.execute("INSERT INTO customer (fname, lname, phone) VALUES (?, ?,?)", (fname, lname, int(phone)))
        self.conn.commit()
    #insert function for product table
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
    #insert function for orders table
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
    #update function for customer table
    def upd_cus(self, customerID, fname, lname, phone):
        if not Checks.is_phone(phone):
            print("Invalid input. Phone number must be a 10 digit number formatted 1234567890.")
            return
        if fname is None or lname is None:
            print("Invalid input. First and last name required.")
            return
        if not Checks.is_pos_num(customerID, "int", "customerID"):
            return
        self.cursor.execute("UPDATE CUSTOMER SET FNAME = ?, LNAME = ?, PHONE = ? WHERE CUSTOMERID = ?",(fname,lname,phone,customerID))
        self.conn.commit()
    #update function for employee table
    def upd_emp(self,employeeID, fname, lname, position, salary):
        if not Checks.is_pos_num(salary, "float", "Salary"):
            return
        if fname is None or lname is None or salary is None:
            print("Invalid input. First name, last name, and salary all require inputs.")
            return
        if not Checks.is_pos_num(employeeID, "int", "employeeID"):
            return
        self.cursor.execute("UPDATE EMPLOYEE SET FNAME = ?, LNAME = ?, POSITION = ?,SALARY=? WHERE EMPLOYEEID = ?",(fname,lname,position,salary,employeeID))
        self.conn.commit()
    #update function for product table
    def upd_prod(self,productID, p_desc, price, stock):
        if not Checks.is_pos_num(price, "float", "Price"):
            return
        if not Checks.is_pos_num(stock, "int", "Stock"):
            return
        if p_desc is None:
            print("Invalid input. Product description required.")
            return
        if not Checks.is_pos_num(productID, "int", "productID"):
            return
        self.cursor.execute("UPDATE PRODUCT SET P_DESC = ?, PRICE = ?, STOCK = ? WHERE PRODUCTID = ?",(p_desc, price, stock,productID))
        self.conn.commit()
    #update function for orders table
    def upd_ord(self,orderID, customerID, employeeID, total):
        if not Checks.is_pos_num(total, "float", "Total"):
            return
        if not Checks.is_pos_num(customerID, "int", "customerID"):
            return
        if not Checks.is_pos_num(employeeID, "int", "employeeID"):
            return
        if not Checks.is_pos_num(orderID, "int", "orderID"):
            return
        self.cursor.execute("UPDATE ORDERS SET CUSTOMERID = ?, EMPLOYEEID = ?, TOTAL = ? WHERE ORDERID = ?",(customerID, employeeID, total,orderID))
        self.conn.commit()
    #delete function for customer table
    def del_cus(self,customerID):
        if not Checks.is_pos_num(customerID, "int", "customerID"):
            return
        self.cursor.execute("DELETE FROM CUSTOMER WHERE CUSTOMERID = "+str(customerID))
        self.conn.commit()
    #delete function for employee table
    def del_emp(self,employeeID):
        if not Checks.is_pos_num(employeeID, "int", "employeeID"):
            return
        self.cursor.execute("DELETE FROM EMPLOYEE WHERE EMPLOYEEID = "+str(employeeID))
        self.conn.commit()
    #delete function for product table
    def del_prod(self,productID):
        if not Checks.is_pos_num(productID, "int", "productID"):
            return
        self.cursor.execute("DELETE FROM PRODUCT WHERE PRODUCTID = "+str(productID))
        self.conn.commit()
    #delete function for orders table
    def del_ord(self,orderID):
        if not Checks.is_pos_num(orderID, "int", "orderID"):
            return
        self.cursor.execute("DELETE FROM ORDERS WHERE ORDERID = "+str(orderID))
        self.conn.commit()
    #sorted select functions
    def sort_table(self,table,target,asc):
        return self.conn.execute("SELECT * FROM "+table+" ORDER BY "+target+" "+asc).fetchall()