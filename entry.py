class Entry:
    def __init__(self, val=None):
        self._val = val

    def set_val(self, val):
        self._val = val

    def get_val(self):
        return self._val

    @staticmethod
    def value_is_valid(val):
        return val is None or 1 <= val <= 9

    def __str__(self):
        return str(self._val)

