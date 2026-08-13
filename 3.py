def print_board(board):
    print("\n+-------+-------+-------+")

    for i in range(9):
        print("|", end=" ")

        for j in range(9):
            if board[i][j] == 0:
                print(".", end=" ")
            else:
                print(board[i][j], end=" ")

            if (j + 1) % 3 == 0:
                print("|", end=" ")

        print()

        if (i + 1) % 3 == 0:
            print("+-------+-------+-------+")


def is_valid(board, row, col, num):

    # Check row
    if num in board[row]:
        return False

    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


def find_empty(board):
    best_cell = None
    minimum_options = 10

    # Choose the empty cell with the fewest possibilities
    for row in range(9):
        for col in range(9):

            if board[row][col] == 0:

                options = 0

                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        options += 1

                if options < minimum_options:
                    minimum_options = options
                    best_cell = (row, col)

    return best_cell


def solve_sudoku(board):

    empty = find_empty(board)

    # No empty cells → Sudoku solved
    if empty is None:
        return True

    row, col = empty

    for num in range(1, 10):

        if is_valid(board, row, col, num):

            board[row][col] = num

            if solve_sudoku(board):
                return True

            # Backtracking
            board[row][col] = 0

    return False


# Sudoku puzzle
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


# Count empty cells
empty_cells = sum(row.count(0) for row in board)

print("========== SUDOKU SOLVER ==========")

print("\nOriginal Sudoku:")
print_board(board)

print(f"Empty cells: {empty_cells}")

# Solve
if solve_sudoku(board):

    print("\nSolved Sudoku:")
    print_board(board)

    print(f"Successfully solved {empty_cells} empty cells.")

else:
    print("\nNo solution exists!")