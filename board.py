from entry import Entry


class Board:
    def __init__(self):
        self.matrix = [[Entry()] * 9 for _ in range(9)]

    