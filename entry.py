class Entry:
    """Represents and holds the value of a single cell on a sudoku board"""

    def __init__(self, val=None):
        """
        Create an Entry object
        :param val: None or Integer: The value to be held in that entry
        """
        self._val = val  # Set the value to what was given

    def set_val(self, val):
        """
        Set the value of the Entry object
        :param val: None or Integer: The value to set the entry to
        :return: None
        """
        self._val = val  # Set the value to what was given

    def get_val(self):
        """
        Get the value of the entry
        :return: None or Integer: The value of the entry
        """
        return self._val  # Return the value

    @staticmethod
    def value_is_valid(val):
        """
        Check if a given value would be valid to be held by an entry
        :param val: None or Integer: The value to check if it is valid
        :return: Boolean: Is the given value None or in the range [1, 9]?
        """
        return val is None or 1 <= val <= 9  # Return True if None or int from 1 to 9 inclusive, False otherwise

    def __str__(self):
        """
        Convert the entry to a string
        :return: String: The value of the entry in string form
        """
        return str(self._val)  # Convert val to string and return

