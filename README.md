# Machine-Learning-Mini-Projects
These are mini Machine Learning Projects that I had to do for my cmpsc 442 class
## Projects

### Uninformed Search Algorithms

This project explores classic search problems using uninformed search techniques and includes:

- **N-Queens Problem**  
  Place n queens on an n x n chessboard so that no two queens threaten each other. The solution only considers configurations with one queen per row and uses a depth-first search strategy to generate all valid arrangements.

- **Lights Out Puzzle**  
  Solve the puzzle where toggling a light (and its neighbors) turns them on or off. Implemented methods include board initialization, move execution, scrambling, generating successors, and finding optimal solutions using a breadth-first search.

- **Linear Disk Movement**  
  Move disks along a linear grid from the starting position to designated endpoints. This puzzle enforces movement constraints and uses breadth-first search to produce an optimal sequence of moves.

---

### Sudoku Constraint Satisfaction Solver

This project implements a Sudoku solver using constraint satisfaction and inference techniques:

- **Arc Consistency (AC-3):**  
  Applies the AC-3 algorithm to enforce arc consistency across cells, reducing possible values.

- **Improved Inference:**  
  Extends AC-3 by analyzing neighboring cells' possibilities to infer single-value placements.

- **Backtracking with Guessing:**  
  Integrates a backtracking search that utilizes the improved inference methods to solve more challenging puzzles where inference alone is insufficient.

This combination of strategies allows for solving puzzles ranging from easy to hard.

---

### Naive Bayes Spam Filter

This project builds a basic spam filter using a naive Bayes classifier:

- **Token Extraction and Laplace Smoothing:**  
  Extracts tokens from emails and computes Laplace-smoothed log-probabilities for words in both spam and ham classes.

- **Email Classification:**  
  Classifies emails as spam or ham by comparing aggregated log probabilities of tokens, ensuring unknown words are handled via a special `<UNK>` token.

- **Indicative Word Analysis:**  
  Determines the most indicative words for spam and ham, enhancing interpretability and refining classification accuracy.

This project demonstrates practical applications of text classification and probabilistic inference in Python.

---

## Getting Started

Each project is contained in its respective folder along with a starter code file (or template) to help you get started. Please refer to the individual project files for usage instructions, dependencies, and sample commands.

---

Feel free to explore the code and reach out if you have any questions!

