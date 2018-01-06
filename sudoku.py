# stdlib imports
import copy
import math


class InvalidProblemError(Exception):
    """An exception raised when:

    1) The problem is not a square grid
    2) The problem size is not a square number
    3) The problem has a row that is not a list
    """


def import_problems(filename, problem_size = 9):
    """A method for parsing problems from a file. In the file each line must 
    be a string of integers encoding a problem, where the order of the digits is
    that of a walk through the grid from left to right and top to bottom.

    Args:
        filename (str): The location of the problems.
        problem_size (int, optional): The size of the sudoku grids encoded in
            the file.
    """
    file = open(filename, 'r')
    problems = []

    for line in file:
        line = line.strip()
        problem = []
        for i in range(0, len(line), problem_size):
            row = [int(character) for character in list(line[i: i+problem_size])]
            problem.append(row)
        problems.append(problem)

    return problems


class Solver:
    """A class for solving sudoku problems.
    """

    def __init__(self, problem):
        """
        Initializes the solver class with a given problem. The solution is 
        initialized as a deep copy of the problem to avoid altering it during 
        the solving process. It also initializes the problem size and box size 
        for later use.

        Args:
            problem (list of lists of ints): This list characterizes a sudoku 
                grid. The ints are in 0-9, where 0 denotes an empty cell and any
                other number is a filled cell.
        """
        self.problem = problem
        self.size = len(self.problem)
        self.box_size = int(math.sqrt(self.size))
        self.solution = copy.deepcopy(problem)

    def solve(self):
        """Attempts to solves the sudoku problem recursively with backtracking. 
        We attempt to fill in each empty cell successively with one of the 
        available options, and return to change previous cells if we are no 
        longer able to make valid moves. Having made only valid moves, we stop
        when the grid is completely filled.

        Returns:
            The solution grid if successful, False otherwise.

        Raises:
            InvalidProblemError: If `problem` isn't a valid sudoku grid.
        """
        self._validate_problem()

        next_empty_cell = self._next_empty_cell()

        if not next_empty_cell:
            return self.solution
        else:
            row, column = next_empty_cell

        for number in range(1, self.size + 1):
            if self._is_valid_move(row, column, number):
                self.solution[row][column] = number

                if self.solve():
                   return self.solution 
                else:
                    self.solution[row][column] = 0

        return False

    def _validate_problem(self):
        square_root = math.sqrt(self.size)
        if square_root != self.box_size:
            raise InvalidProblemError('problem size is not a square')

        for row in self.problem:
            if not isinstance(row, list):
                raise InvalidProblemError('problem is not a list of lists')

            number_of_columns = len(row)
            if self.size != number_of_columns:
                raise InvalidProblemError('problem is not a square grid')

    def _is_valid_move(self, row, column, value):
        return not self._used_in_row(row, value) and \
               not self._used_in_column(column, value) and \
               not self._used_in_box(row, column, value)

    def _next_empty_cell(self):
        for row in range(self.size):
            for column in range(self.size):
                if self.solution[row][column] == 0:
                    return (row, column)

    def _used_in_row(self, row, value):
        return value in self.solution[row]

    def _used_in_column(self, column, value):
        for row in range(self.size):
            if self.solution[row][column] == value:
                return True
        return False

    def _used_in_box(self, row, column, value):
        box_rows, box_columns = self._find_box(row, column)

        for box_row in box_rows:
            for box_column in box_columns:
                if self.solution[box_row][box_column] == value:
                    return True
        return False

    def _find_box(self, row, column):
        box_row_start = (row / self.box_size) * self.box_size
        box_rows = range(box_row_start, box_row_start + self.box_size)

        box_column_start = (column / self.box_size) * self.box_size
        box_columns = range(box_column_start, box_column_start + self.box_size)

        return (box_rows, box_columns)