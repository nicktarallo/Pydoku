from board import Board
from position import Position

b = Board.generate_board()
print(b)
print()
b.solve()
print(b)
