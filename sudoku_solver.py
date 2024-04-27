from itertools import product

def is_valid_move(puzzle, row, col, num):
    """
    Check if it's valid to place the number 'num' in the position (row, col) on the 'puzzle'.
    
    Args:
    - puzzle: 2D list representing the Sudoku grid.
    - row: Integer, row index where number is to be placed.
    - col: Integer, column index where number is to be placed.
    - num: Integer, number to place on the Sudoku grid.
    
    Returns:
    - Boolean: True if the move is valid, False otherwise.
    """
    if num in puzzle[row] or num in [puzzle[i][col] for i in range(9)]:
        return False

    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if puzzle[i][j] == num:
                return False

    return True

def find_empty_cells(puzzle):
    """
    Find all empty cells in the Sudoku puzzle.
    
    Args:
    - puzzle: 2D list representing the Sudoku grid.
    
    Returns:
    - List of tuples: each tuple is a pair (row, col) indicating an empty cell.
    """
    return [(i, j) for i in range(9) for j in range(9) if puzzle[i][j] == 0]

def update_domains(puzzle, domains, row, col, num):
    """
    Update the domain of possible values for cells affected by placing 'num' at (row, col).
    
    Args:
    - puzzle: 2D list representing the Sudoku grid.
    - domains: Dictionary mapping (row, col) to a set of possible values.
    - row: Integer, row index of the placed number.
    - col: Integer, column index of the placed number.
    - num: Integer, number placed on the grid.
    """
    for i in range(9):
        if (row, i) in domains:
            domains[(row, i)].discard(num)
        if (i, col) in domains:
            domains[(i, col)].discard(num)

    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if (i, j) in domains:
                domains[(i, j)].discard(num)
    domains[(row, col)].add(num)

def restore_domain(puzzle, domains, row, col, num):
    """
    Restore the domain of possible values after backtracking from an invalid move.
    
    Args:
    - puzzle: 2D list representing the Sudoku grid.
    - domains: Dictionary mapping (row, col) to a set of possible values.
    - row: Integer, row index of the backtracked cell.
    - col: Integer, column index of the backtracked cell.
    - num: Integer, number removed from the grid during backtracking.
    """
    for i in range(9):
        if (row, i) in domains and is_valid_move(puzzle, row, i, num):
            domains[(row, i)].add(num)
        if (i, col) in domains and is_valid_move(puzzle, i, col, num):
            domains[(i, col)].add(num)

    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if (i, j) in domains and is_valid_move(puzzle, i, j, num):
                domains[(i, j)].add(num)

def solve_sudoku_csp(puzzle):
    """
    Solve the Sudoku puzzle using the Constraint Satisfaction Problem approach.
    
    Args:
    - puzzle: 2D list representing the Sudoku grid.
    
    Returns:
    - 2D list: Solved Sudoku grid if a solution is found, otherwise None.
    """
    def solve(puzzle, domains):
        empty_cells = find_empty_cells(puzzle)
        if not empty_cells:
            return True  # Puzzle is solved

        row, col = empty_cells[0]  # Prioritize first empty cell
        for num in list(domains[(row, col)]):
            if is_valid_move(puzzle, row, col, num):
                puzzle[row][col] = num
                update_domains(puzzle, domains, row, col, num)
                
                if solve(puzzle, domains):
                    return True

                puzzle[row][col] = 0  # Backtrack
                domains[(row, col)].add(num)  # Restore domain
                restore_domain(puzzle, domains, row, col, num)

        return False

    # Initialize domain for each empty cell
    domains = {(i, j): set(range(1, 10)) for i, j in product(range(9), repeat=2) if puzzle[i][j] == 0}

    if solve(puzzle, domains):
        return puzzle
    return None
        
def print_sudoku(puzzle):
    """
    Print the Sudoku grid formatted in a user-friendly way.
    
    Args:
    - puzzle: 2D list representing the Sudoku grid.
    """
    for i in range(9):
        print("| ", end="")
        for j in range(9):
            print(f"{puzzle[i][j]}" if puzzle[i][j] != 0 else "_", end=" ")
            if (j + 1) % 3 == 0:
                print("| ", end="")
        print()
        if (i + 1) % 3 == 0 and i < 8:
            print("=" * 25)

# Example of how to use the solve_sudoku_csp function with an initial board
initial_puzzle = [
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

print("Initial Sudoku:")
print_sudoku(initial_puzzle)

solution = solve_sudoku_csp(initial_puzzle)

if solution:
    print("\nSolved Sudoku:")
    print_sudoku(solution)
else:
    print("\nNo solution found.")