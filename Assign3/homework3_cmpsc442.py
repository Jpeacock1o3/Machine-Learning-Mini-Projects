############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Jaden Peacock"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

from collections import deque

############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    return [(i, j) for i in range(9) for j in range(9)]

def sudoku_arcs():
    arcs = []
    cells = sudoku_cells()
    for cell1 in cells:
        for cell2 in cells:
            if cell1 == cell2:
                continue
            # Check if same row, same column, or same block.
            if (cell1[0] == cell2[0] or
                    cell1[1] == cell2[1] or
                    ((cell1[0] // 3 == cell2[0] // 3) and (cell1[1] // 3 == cell2[1] // 3))):
                arcs.append((cell1, cell2))
    return arcs

def read_board(path):
    board = {}
    with open(path, 'r') as f:
        # Remove empty lines and strip newline characters.
        lines = [line.strip() for line in f if line.strip()]
        if len(lines) < 9:
            raise ValueError("Board file must have at least 9 non-empty lines.")
        for i in range(9):
            line = lines[i]
            if len(line) < 9:
                raise ValueError("Each line must have at least 9 characters.")
            for j in range(9):
                ch = line[j]
                if ch in '123456789':
                    board[(i, j)] = {int(ch)}
                elif ch == '*':
                    board[(i, j)] = set(range(1, 10))
                else:
                    raise ValueError("Invalid character in board: " + ch)
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        removed = False
        to_remove = set()
        for val in self.board[cell1]:
            # For the inequality constraint, cell1's value must be different from some value in cell2.
            # If cell2's domain consists solely of the same value, then val is inconsistent.
            if not any(val != other for other in self.board[cell2]):
                to_remove.add(val)
        if to_remove:
            self.board[cell1] -= to_remove
            removed = True
        return removed

    def infer_ac3(self):
        queue = deque(Sudoku.ARCS)
        while queue:
            (xi, xj) = queue.popleft()
            if self.remove_inconsistent_values(xi, xj):
                if not self.board[xi]:
                    return False  # Failure: domain wiped out
                # Add all arcs (xk, xi) where xk is a neighbor of xi (other than xj)
                for xk in Sudoku.CELLS:
                    if xk != xi and (
                            xk[0] == xi[0] or
                            xk[1] == xi[1] or
                            ((xk[0] // 3 == xi[0] // 3) and (xk[1] // 3 == xi[1] // 3))
                    ):
                        if xk != xj:
                            queue.append((xk, xi))
        return True

    def _all_units(self):
        """
        Helper function that returns a list of all units (rows, columns, and blocks)
        in the Sudoku puzzle. Each unit is a list of cell coordinates.
        """
        units = []
        # Rows
        for i in range(9):
            units.append([(i, j) for j in range(9)])
        # Columns
        for j in range(9):
            units.append([(i, j) for i in range(9)])
        # Blocks
        for blk in range(3):
            for bj in range(3):
                block = []
                for i in range(blk * 3, blk * 3 + 3):
                    for j in range(bj * 3, bj * 3 + 3):
                        block.append((i, j))
                units.append(block)
        return units

    def infer_improved(self):
        changed = True
        while changed:
            changed = False
            # First, prune with AC-3.
            if not self.infer_ac3():
                return False
            # Check each unit for unique possibilities.
            for unit in self._all_units():
                for num in range(1, 10):
                    possible_cells = [cell for cell in unit if num in self.board[cell]]
                    if len(possible_cells) == 1:
                        cell = possible_cells[0]
                        if self.board[cell] != {num}:
                            self.board[cell] = {num}
                            changed = True
        return True

    def infer_with_guessing(self):
        if not self.infer_improved():
            return False

            # Check if the puzzle is solved.
        if all(len(self.board[cell]) == 1 for cell in Sudoku.CELLS):
            return self.board

            # Choose a cell with the smallest domain (greater than 1) to try guessing.
        cell = min((c for c in Sudoku.CELLS if len(self.board[c]) > 1), key=lambda c: len(self.board[c]))

        # Try each possible value in that cell.
        for value in self.board[cell]:
            # Make a deep copy of the board.
            new_board = {c: set(self.board[c]) for c in Sudoku.CELLS}
            new_board[cell] = {value}
            sudoku_copy = Sudoku(new_board)
            result = sudoku_copy.infer_with_guessing()
            if result:
                # If a solution is found, update self.board and return the solved board.
                self.board = sudoku_copy.board
                return self.board

        # If none of the guesses work, the puzzle is unsolvable.
        return False

