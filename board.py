from entry import Entry
from position import Position
import random
import copy


class Board:
    def __init__(self):
        self._matrix = [[Entry() for x in range(9)] for _ in range(9)]
        self._rows = [set() for _ in range(9)]
        self._cols = [set() for _ in range(9)]
        self._boxes = [[set() for x in range(3)] for _ in range(3)]

    def set_val(self, val, pos):
        if Entry.value_is_valid(val) and self.entry_non_conflicting(val, pos):
            if val is None:
                self.remove_val(self.get_val(pos), pos)
            elif 1 <= val <= 9:
                if self.get_val(pos):
                    self.remove_val(self.get_val(pos), pos)
                self.add_val(val, pos)
        else:
            raise ValueError("Not a valid value (None or 1-9) or Value already exists in column, row, or box")
        self._matrix[pos.get_row()][pos.get_col()].set_val(val)

    def remove_val(self, val, pos):
        if val in self.get_row(pos):
            self.get_row(pos).remove(val)
        if val in self.get_col(pos):
            self.get_col(pos).remove(val)
        if val in self.get_box(pos):
            self.get_box(pos).remove(val)

    def add_val(self, val, pos):
        self.get_row(pos).add(val)
        self.get_col(pos).add(val)
        self.get_box(pos).add(val)

    def solve(self, rand=False, restrict_val=None, restrict_pos=None):
        if not rand:
            self.solve_simple(restrict_val, restrict_pos)
        solved = self._solve(Position(0, 0), rand, restrict_val, restrict_pos)
        if not solved:
            raise ValueError("Given board is not solvable")

    def solve2(self, pos=Position(0, 0), rand=False, restrict_val=None, restrict_pos=None):
        if not rand:
            self.solve_simple(restrict_val, restrict_pos)
        solved = self._solve2(pos, rand, restrict_val, restrict_pos)
        return solved
        #if not solved:
        #    raise ValueError("Given board is not solvable")

    def _solve2(self, pos, rand=False, restrict_val=None, restrict_pos=None):
        if pos.get_row() == 9:
            solved = True
        elif self.get_val(pos) is not None:
            solved = self.solve2(pos.next(), rand, restrict_val, restrict_pos)
        else:
            vals = list(range(1, 10))
            solved = False
            if rand:
                random.shuffle(vals)
            if pos == restrict_pos:
                vals.remove(restrict_val)
            for val in vals:
                if Entry.value_is_valid(val) and self.entry_non_conflicting(val, pos):
                    self.set_val(val, pos)
                    solved = self._solve(pos.next(), rand, restrict_val, restrict_pos)
                    if solved:
                        break
                    self.remove_val(val, pos)
            if not solved:
                self.set_val(None, pos)
        return solved

    def solve_simple(self, restrict_val=None, restrict_pos=None):
        working = True
        while working:
            working = False
            for i in range(9):
                for j in range(9):
                    pos = Position(i, j)
                    if self.get_val(pos) is not None:
                        continue
                    union = self.get_box(pos) | self.get_col(pos) | self.get_row(pos)
                    if len(union) == 8:
                        val = ({1, 2, 3, 4, 5, 6, 7, 8, 9} - union).pop()
                        if pos == restrict_pos:
                            if restrict_val == val:
                                continue
                        working = True
                        self.set_val(val, pos)
            working = self.check_rows(restrict_val, restrict_pos) or working
            working = self.check_cols(restrict_val, restrict_pos) or working
            working = self.check_boxes(restrict_val, restrict_pos) or working

    def _solve(self, pos, rand=False, restrict_val=None, restrict_pos=None):
        if pos.get_row() == 9:
            solved = True
        elif self.get_val(pos) is not None:
            solved = self._solve(pos.next(), rand, restrict_val, restrict_pos)
        else:
            vals = list(range(1, 10))
            solved = False
            if rand:
                random.shuffle(vals)
            if pos == restrict_pos:
                vals.remove(restrict_val)
            for val in vals:
                if Entry.value_is_valid(val) and self.entry_non_conflicting(val, pos):
                    self.set_val(val, pos)
                    solved = self._solve(pos.next(), rand, restrict_val, restrict_pos)
                    if solved:
                        break
                    self.remove_val(val, pos)
            if not solved:
                self.set_val(None, pos)
        return solved

    def get_row(self, pos):
        return self._rows[pos.get_row()]

    def get_col(self, pos):
        return self._cols[pos.get_col()]

    def get_box(self, pos):
        return self._boxes[pos.get_row() // 3][pos.get_col() // 3]

    def get_val(self, pos):
        return self._matrix[pos.get_row()][pos.get_col()].get_val()

    def entry_non_conflicting(self, val, pos):
        return (val not in self.get_row(pos)) and (val not in self.get_col(pos)) and (val not in self.get_box(pos))

    @staticmethod
    def generate_board():
        b = Board.get_solved_board()
        posns = Position.get_all_positions()
        for pos in posns:
            valid = True
            val = b.get_val(pos)
            b_copy = copy.deepcopy(b)
            b_copy.set_val(None, pos)
            try:
                # valid = not b_copy.solve2(restrict_val=val, restrict_pos=pos)
                # valid = False
                b_copy.solve(restrict_val=val, restrict_pos=pos)
                valid = False
            except ValueError:
                pass
            if valid:
                b.set_val(None, pos)
        return b

    @staticmethod
    def get_solved_board():
        b = Board()
        b.solve(True)
        return b

    def __str__(self):
        s = ""
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[i])):
                if self._matrix[i][j].get_val() is None:
                    val = 0
                else:
                    val = str(self._matrix[i][j])
                s += str(val) + " "
                if j == 2 or j == 5:
                    s += "| "
            s += "\n"
            if i == 2 or i == 5:
                s += "-" * 21 + "\n"
        return s

    def copy(self):
        new_board = Board()
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[0])):
                pos = Position(i, j)
                new_board.set_val(self.get_val(pos), pos)
        return new_board

    def check_rows(self, restrict_val=None, restrict_pos=None):
        made_change = False
        for i in range(len(self._rows)):
            missing_vals = set(range(1, 10)) - self._rows[i]
            for val in missing_vals:
                possible_positions = []
                for j in range(9):
                    pos = Position(i, j)
                    if restrict_pos == pos:
                        if restrict_val == val:
                            continue
                    if self.get_val(pos) is None:
                        if self.entry_non_conflicting(val, pos):
                            possible_positions.append(pos)
                if len(possible_positions) == 1:
                    self.set_val(val, possible_positions.pop())
                    made_change = True
        return made_change

    def check_cols(self, restrict_val=None, restrict_pos=None):
        made_change = False
        for i in range(len(self._cols)):
            missing_vals = set(range(1, 10)) - self._cols[i]
            for val in missing_vals:
                possible_positions = []
                for j in range(9):
                    pos = Position(j, i)
                    if restrict_pos == pos:
                        if restrict_val == val:
                            continue
                    if self.get_val(pos) is None:
                        if self.entry_non_conflicting(val, pos):
                            possible_positions.append(pos)
                if len(possible_positions) == 1:
                    self.set_val(val, possible_positions.pop())
                    made_change = True
        return made_change

    def check_boxes(self, restrict_val=None, restrict_pos=None):
        made_change = False
        for i in range(3):
            for j in range(3):
                missing_vals = set(range(1, 10)) - self._boxes[i][j]
                for val in missing_vals:
                    possible_positions = []
                    for r in range(i * 3, (i + 1) * 3):
                        for c in range(j * 3, (j + 1) * 3):
                            pos = Position(r, c)
                            if restrict_pos == pos:
                                if restrict_val == val:
                                    continue
                            if self.get_val(pos) is None:
                                if self.entry_non_conflicting(val, pos):
                                    possible_positions.append(pos)
                    if len(possible_positions) == 1:
                        self.set_val(val, possible_positions.pop())
                        made_change = True
        return made_change







