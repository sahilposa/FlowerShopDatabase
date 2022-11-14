class Checks:

    @staticmethod
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

    @staticmethod
    def is_pos(testInput, type):
        if type == "float" and float(testInput) < 0:
            return False
        if type == "int" and int(testInput) < 0:
            return False
        return True

    @staticmethod
    def is_pos_num(testInput, type, varName):
        if not Checks.is_num(testInput, type) or not Checks.is_pos(testInput, type):
            print("Invalid input. " + varName + " must be a positive number.")
            return False
        return True

    @staticmethod
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

    @staticmethod
    def is_phone_unique(phone, cursor):
        cursor.execute("SELECT * FROM customer WHERE phone=?", (phone,))
        if cursor.fetchone() is None:
            return True
        return False

    @staticmethod
    def is_sort_valid(attribute, asc):
        if (attribute == "") != (asc == ""):
            return False
        return True

    @staticmethod
    def is_filt_valid(attribute, op, value):
        if (attribute == "") != (op == ""):
            return False
        if attribute+op == "" and value:
            return False
        if attribute+op != "" and not value:
            return False
        return True

    @staticmethod
    def is_sort_blank(attribute, asc):
        if attribute+asc == "":
            return True
        return False

    @staticmethod
    def is_filt_blank(attribute, op, value):
        if attribute+op == "" and not value:
            return True
        return False
