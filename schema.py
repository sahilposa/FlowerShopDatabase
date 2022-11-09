class Schema:

    @staticmethod
    def __create_cus(conn, cursor):
        cursor.execute("""CREATE TABLE customer(
                customerID INTEGER PRIMARY KEY,
                fname TEXT NOT NULL,
                lname TEXT NOT NULL,
                phone INTEGER UNIQUE CHECK (phone>=1000000000 and phone<10000000000)
            )""")
        conn.commit()

    @staticmethod
    def __create_emp(conn, cursor):
        cursor.execute("""CREATE TABLE employee(
                employeeID INTEGER PRIMARY KEY,
                fname TEXT NOT NULL,
                lname TEXT NOT NULL,
                position TEXT,
                salary REAL NOT NULL CHECK (salary>=0)
            )""")
        conn.commit()

    @staticmethod
    def __create_prod(conn, cursor):
        cursor.execute("""CREATE TABLE product (
                productID INTEGER PRIMARY KEY,
                p_desc TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL CHECK (stock>=0)
            )""")
        conn.commit()

    @staticmethod
    def __create_orders(conn, cursor):
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
        conn.commit()

    @staticmethod
    def __create_purchase(conn, cursor):
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

    @staticmethod
    def build(conn, cursor):
        Schema.__create_cus(conn, cursor)
        Schema.__create_emp(conn, cursor)
        Schema.__create_prod(conn, cursor)
        Schema.__create_orders(conn, cursor)
        Schema.__create_purchase(conn, cursor)