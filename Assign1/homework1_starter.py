############################################################
# CMPSC 442: Uninformed Search
############################################################

student_name = "Jaden Peacock"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from math import comb
import random
from collections import deque


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    return comb(n * n, n)


def num_placements_one_per_row(n):
    return n ** n


def n_queens_valid(board):
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            # Check for same column
            if board[i] == board[j]:
                return False
            # Check for same diagonal
            if abs(board[i] - board[j]) == abs(i - j):
                return False
    return True


def n_queens_solutions(n):
    def is_valid(board, row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
        return True

    def solve(row, board):
        if row == n:
            yield board[:]  # Yield a copy of the valid board
            return
        for col in range(n):
            if is_valid(board, row, col):
                board[row] = col  # Place queen at (row, col)
                yield from solve(row + 1, board)  # Recur for the next row
                board[row] = -1  # Backtrack

    board = [-1] * n  # Initialize the board (-1 means no queen placed)
    return solve(0, board)


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self):
        return [row[:] for row in self.board]

    def perform_move(self, row, col):
        for r, c, in [(row, col), (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.board[r][c] = not self.board[r][c]

    def scramble(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        return all(all(not cell for cell in row) for row in self.board)

    def copy(self):
        return LightsOutPuzzle(self.get_board())

    def successors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                new_puzzle = self.copy()
                new_puzzle.perform_move(row, col)
                yield (row, col), new_puzzle

    def find_solution(self):
        queue = deque([(self, [])])
        visited = set()
        while queue:
            current_puzzle, path = queue.popleft()
            print(f"Checking state:\n{current_puzzle.get_board()}")  # Debugging

            if current_puzzle.is_solved():
                return path

            for move, new_puzzle in current_puzzle.successors():
                state_tuple = tuple(map(tuple, new_puzzle.board))

                if state_tuple not in visited:
                    visited.add(state_tuple)
                    queue.append((new_puzzle, path + [move]))

        return None


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False] * cols for _ in range(rows)])


############################################################
# Section 3: Linear Disk Movement
############################################################


def solve_identical_disks(length, n):
    """Finds the shortest sequence of moves to move identical disks to the end of a row."""
    initial_state = tuple(1 if i < n else 0 for i in range(length))
    goal_state = tuple(0 for _ in range(length - n)) + tuple(1 for _ in range(n))

    queue = deque([(initial_state, [])])
    visited = set()
    visited.add(initial_state)

    while queue:
        state, moves = queue.popleft()
        if state == goal_state:
            return moves

        for i in range(length):
            if state[i] == 1:
                for delta in [1, 2]:
                    new_pos = i + delta
                    if new_pos < length and state[new_pos] == 0 and (delta == 1 or state[i + 1] == 1):
                        new_state = list(state)
                        new_state[i], new_state[new_pos] = new_state[new_pos], new_state[i]
                        new_state = tuple(new_state)
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_state, moves + [(i, new_pos)]))
    return None  # No solution found


def solve_distinct_disks(length, n):
    """Finds the shortest sequence of moves to move distinct disks to the end in reverse order."""
    initial_state = tuple(range(n)) + tuple(-1 for _ in range(length - n))
    goal_state = tuple(-1 for _ in range(length - n)) + tuple(range(n - 1, -1, -1))

    queue = deque([(initial_state, [])])
    visited = set()
    visited.add(initial_state)

    while queue:
        state, moves = queue.popleft()
        if state == goal_state:
            return moves

        for i in range(length):
            if state[i] != -1:
                for delta in [1, 2]:
                    new_pos = i + delta
                    if new_pos < length and state[new_pos] == -1 and (delta == 1 or state[i + 1] != -1):
                        new_state = list(state)
                        new_state[i], new_state[new_pos] = new_state[new_pos], new_state[i]
                        new_state = tuple(new_state)
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_state, moves + [(i, new_pos)]))
    return None  # No solution found