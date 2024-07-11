#-------------------------------------------------------------------------------
# Darie-Dragos Mitoiu
# User v1.0.0 15/02/2019
# An user module deisgned for a tailoring and alterations business
#-------------------------------------------------------------------------------


class User:
    """This class allows the creation of an user object.
    This class is not used in the current version."""

    def __init__(self, username, password, permission_level, email):
        self.username = username
        self.password = password
        self.permission_level = permission_level
        self.email = email

    # Declaring setters
    def set_username(self, newval):
        self.username = newval

    def set_password(self, newval):
        self.password = newval

    def set_permission_level(self, newval):
        self.permission_level = newval

    def set_email(self, newval):
        self.email = newval

    # Declaring Getters
    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_permission_level(self):
        return self.permission_level

    def get_email(self):
        return self.email

    def to_string(self):
        message = ""
        message += "Username: " + str(self.get_username()) + "\n"
        message += "Password: " + str(self.get_password()) + "\n"
        message += "Permission Level: " + str(self.get_permission_level()) + "\n"
        message += "Email: " + str(self.get_email()) + "\n"
        return message
