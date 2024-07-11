#-------------------------------------------------------------------------------
# Darie-Dragos Mitoiu
# Controller v1.0.0 01/04/2019
# A controller module designed for a tailoring and alterations business
#-------------------------------------------------------------------------------


# Declaring constants
VALID_INTEGERS = "0123456789"
VALID_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.- "
VALID_CHARACTERS_EMAIL = ("abcdefghijklmnopqrstuvwxyz"
                          "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                          "_.@")

class Controller:
    """This class allows the creation of a data validation object."""

    def __init__(self, name):
        self.name = name

    def validate_integer(self, data):
        """This method will allow the user input to contain only integers."""

        # If all characters in the user input are integers return True
        if all(x in VALID_INTEGERS for x in data):
            return True
        else:
            return False

    def validate_float(self, data):
        """This method will allow the user input to contain
        only float numbers."""

        try:
            # Try to convert the input to float
            valid = float(data)
            return True
        except:
            return False

    def validate_float_list(self, data):
        """This method will allow a list to contain only float elements."""

        # If all elements in the list are float return True
        valid = [self.validate_float(x) for x in data]
        if all(valid):
            return True
        else:
            return False

    def validate_alpha(self, data):
        """This method will allow the user input to contain only
        alphabetical characters."""

        # If all characters are valid return True
        if all(x in VALID_CHARACTERS for x in data):
            return True
        else:
            return False

    def validate_integer_alpha(self, data):
        """This method will allow the user input to contain only alphabetical
        characters and integers."""

        # If all characters are valid return True
        valid = (VALID_INTEGERS + VALID_CHARACTERS)
        if all(x in valid for x in data):
            return True
        else:
            return False

    def validate_email(self, data):
        """This method will allow the user input to contain
        only characters that are valid for an email address."""

        # If all characters are valid return True
        valid = (VALID_INTEGERS + VALID_CHARACTERS_EMAIL)
        if all(x in valid for x in data):
            return True
        else:
            return False
