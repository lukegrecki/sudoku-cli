# stdlib imports
import copy
import math


def from_file(filename, problem_size = 9):
    """Creates sudoku problems from a file.

    Args:
        filename (str): A file that contains one line per problem. All problems 
            must be the same size. The line consists of ints in 0-9, where 0 
            denotes an empty cell and any other number is a filled cell. The 
            cells in the string are ordered top to bottom and left to right.

        problem_size (int): A number specifying the size of the sudoku grids in
            the given file.

    Returns:
        list: A list of the sudoku problems defined in the file.
    """
    with open(filename, 'r') as file:
        return [deserialize(line.strip(), problem_size) for line in file]


def to_file(solutions, output_filename):
    """Writes sudoku solutions to a file.

    Args:
        solutions (list of solutions): The list of solutions to be written in 
            the standard form.

        output_filename (str): The file that will be overwritten with the 
            solutions in the standard format specified above.
    """
    with open(output_filename, 'w') as file:
        for i in range(len(solutions)):
            file.write(serialize(solutions[i]))
            if i < len(solutions) - 1:
                file.write('\n')


def serialize(grid):
    """Serializes sudoku grids into a string.
    
    Args:
        grid (list of lists of ints): This list characterizes a sudoku 
            grid. The ints are in 0-9, where 0 denotes an empty cell and any
            other number is a filled cell.
        
    Returns:
        str: This string represents a walk through the grid from top to bottom 
            and left to right.
    """
    string = ''
    for row in grid:
        for cell in row:
            string += str(cell)

    return string


def deserialize(string, size):
    """Deserializes sudoku grid strings into lists.

    Args:
        string (str): This string represents a sudoku grid in the standard 
        format.

        size (int): A number specifying the size of the sudoku grid 
        encoded in `string`.
    """
    grid = []
    for i in range(0, len(string), size):
        cell_characters = list(string[i:i+size])
        row = [int(character) for character in cell_characters]
        grid.append(row)

    return grid


class InvalidProblemError(Exception):
    """An exception raised when:

    1) The problem is not a square grid
    2) The problem size is not a square number
    3) The problem has a row that is not a list
    """
    pass


class Solver:
    """A class for solving sudoku problems.
    """

    def __init__(self, problem):
        """Initializes the solver class with a given problem. The solution is 
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

    def solve(self, validate=False):
        """Attempts to solves the sudoku problem recursively with backtracking. 
        We attempt to fill in each empty cell successively with one of the 
        available options, and return to change previous cells if we are no 
        longer able to make valid moves. Having made only valid moves, we stop
        when the grid is completely filled.

        Args:
            validate (bool): Determines whether to validate the problem.

        Returns:
            The solution grid if successful, False otherwise.

        Raises:
            InvalidProblemError: If `problem` isn't a valid sudoku grid.
        """
        if validate:
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
        box_row_start = (row // self.box_size) * self.box_size
        box_rows = range(box_row_start, box_row_start + self.box_size)

        box_column_start = (column // self.box_size) * self.box_size
        box_columns = range(box_column_start, box_column_start + self.box_size)

        return (box_rows, box_columns)