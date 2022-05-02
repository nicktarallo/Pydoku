from board import Board
from position import Position

b = Board()

print("Enter each row with spaces between each number, use 0 for empty spaces")

matrix = []
for i in range(1, 10):
    line = input(f'Enter Row {i}: ')
    row = [int(x) for x in line.split(" ")]
    matrix.append(row)

for i in range(9):
    for j in range(9):
        if matrix[i][j] != 0:
            b.set_val(matrix[i][j], Position(i, j))

b._solve_simple()
print(b)
