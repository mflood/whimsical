"""
    sudoku.py
    Matthew Flood

    Solve Sudoku Puzzles
"""
import copy
import random

class InvalidPuzzleException(Exception):
    pass

class UnsolvablePuzzleException(Exception):
    pass

def convert_array_to_board(board):
    converted_board = []
    for row in board:
        converted_row = []
        converted_board.append(converted_row)
        for cell in row:
            converted_row.append(cell.int_value())

    return converted_board

def convert_board_to_arrays(board):
    converted_board = []
    for row_index, row in enumerate(board):
        converted_row = []
        converted_board.append(converted_row)
        for cell_index, cell in enumerate(row):
            square = SudokuSquare(row_index, cell_index, cell)
            converted_row.append(square)

    return converted_board

def get_section_coordinates(row, cell):
    """
        returns all the cells in the section
        that contains row, cell, without
        returning row, cell
        without returning any cells in row or cell
    """
    return_coordinates = []

    row_start = int(row / 3) * 3
    cell_start = int(cell / 3) * 3
    for x in range(3):
        row_num = x + row_start
        for y in range(3):
            cell_num = y + cell_start
            #if row_num != row and cell_num != cell:
            #    return_coordinates.append((row_num, cell_num))
            if (row_num, cell_num) != (row, cell):
                return_coordinates.append((row_num, cell_num))

    return return_coordinates


class SudokuSquare(object):
    
    def __init__(self, row, cell, starting_value):
        self._row = row
        self._cell = cell
        if starting_value == 0:
            self._values = [9, 2, 8, 4, 5, 3, 7, 6, 1]
            self.locked = False
        else:
            self._values = [starting_value]
            self.locked = True
        self._hash = 0
        self._update_hash()
        self.section_coordinates = get_section_coordinates(row, cell)

    def _update_hash(self):
        values = copy.copy(self._values)
        values.sort()
        self.hash = hash(tuple(values))

    def count(self):
        return len(self._values)

    def __comp__(self, other):
        return cmp(self._hash, other._hash)

    def __hash__(self):
        return self._hash

    def values(self):
        return self._values

    def set_values(self, new_values):
        self._values = new_values
        self._update_hash()

    def __str__(self):
        if len(self._values) == 1:
            return "{}".format(self._values[0])

        return "{}".format(self._values)

    def int_value(self):
        if len(self._values) == 1:
            return self._values[0]
        return 0


    def get_possible_values(self, board):
        """
            Returns the values that are possible for this cell
        """
        possible_numbers = copy.copy(self._values)

        # sole candidate / naked subset
        section_reducer = {}

        # Which cells contain a number
        # find hidden subsets
        number_cells = {}

        # holds the distinct set of numbers
        # in all the other cells
        section_numbers = set()
        for coord in self.section_coordinates:
            examine_cell = board[coord[0]][coord[1]]
            tipping_point = examine_cell.count() - 1
            if section_reducer.get(examine_cell, 0) == tipping_point:
                for val in examine_cell.values():
                    if val in possible_numbers:
                        possible_numbers.remove(val)
                        if not possible_numbers:
                            raise InvalidPuzzleException()
            for z in examine_cell.values():
                number_cells.setdefault(z, [])
                number_cells[z].append(examine_cell)

            section_numbers = section_numbers.union(set(examine_cell.values()))
            section_reducer.setdefault(examine_cell, 0)
            section_reducer[examine_cell] += 1

        # unique candidatea
        # this is the only
        # square that allows this number
        for p in possible_numbers:
            if p not in section_numbers:
                possible_numbers = [p]
                break

        # hidden subsets
        for p in possible_numbers:
            cells = number_cells.get(p, [])
            if len(cells) == 1:
                pass
                
            if number_cells.get(p, []):
                pass


        row_reducers = {}
        col_reducers = {}

        row_section_numbers = set()
        col_section_numbers = set()
        for x in range(9):

            # check row
            if x != self._cell:
                examine_cell = board[self._row][x]
                tipping_point = examine_cell.count() - 1
                if row_reducers.get(examine_cell, 0) == tipping_point:
                    for val in examine_cell.values():
                        if val in possible_numbers:
                            possible_numbers.remove(val)
                            if not possible_numbers:
                                raise InvalidPuzzleException()
                row_section_numbers = row_section_numbers.union(set(examine_cell.values()))
                row_reducers.setdefault(examine_cell, 0)
                row_reducers[examine_cell] += 1

            # check column
            if x != self._row:
                examine_cell = board[x][self._cell]
                tipping_point = examine_cell.count() - 1
                if col_reducers.get(examine_cell, 0) == tipping_point:
                    for val in examine_cell.values():
                        if val in possible_numbers:
                            possible_numbers.remove(val)
                            if not possible_numbers:
                                raise InvalidPuzzleException()

                col_reducers.setdefault(examine_cell, 0)
                col_reducers[examine_cell] += 1
                col_section_numbers = col_section_numbers.union(set(examine_cell.values()))

        # unique candidate
        for p in possible_numbers:
            if p not in row_section_numbers or p not in col_section_numbers:
                possible_numbers = [p]
                break

        if not possible_numbers:
            raise InvalidPuzzleException()

        return possible_numbers

def reduce_board(board):
    global evals
    global reductions
    reduced_board = copy.deepcopy(board)
    reduced = False
    for row in reduced_board:
        for square in row:
            if square.locked:
                continue
            try:

                new_values = square.get_possible_values(board)
                evals += 1


                if len(new_values) < square.count():
                    #print("{},{} Changing {} to {}".format(square._cell, square._row, square.values(), new_values))
                    reductions += 1
                    reduced = True
                    square.set_values(new_values)
            except InvalidPuzzleException:
                return None

    if reduced:
        return reduce_board(reduced_board)

    return reduced_board

def recursive_solve(board):
    global iterations
    global global_board
    iterations += 1
    if iterations > 28:
        hell = Exception("{}".format(global_board))
        raise hell
        pass

    reduced_board = reduce_board(board)
    if not reduced_board:
        return None

    row_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    col_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(row_indexes)
    random.shuffle(col_indexes)

    square_counts = {}
    for row in row_indexes:
        for cell in col_indexes:
            square = reduced_board[row][cell]
            num_items = square.count()
            if num_items > 1 and num_items not in square_counts:
                square_counts[square.count()] = square
                if num_items == 2:
                    break

                #possible_values = copy.copy(square.values())
                #for value in possible_values:
                #    board_trial = reduced_board #copy.deepcopy(reduced_board)
                #    square.set_values([value])
                #    solved_board = recursive_solve(board_trial)
                #    if solved_board:
                #        return solved_board
                #return None

    if square_counts:
        keys = list(square_counts.keys())
        keys.sort()
        lowest_count = keys[0]
        square = square_counts[lowest_count]
        possible_values = copy.copy(square.values())
        # try each candidate value
        for value in possible_values:
            square.set_values([value])
            square.locked = True
            solved_board = recursive_solve(reduced_board)
            if solved_board:
                return solved_board
        return None





    return reduced_board

def check_solvability(board):
    num_start_values = 0
    for row in board:
        for cell in row:
            if cell > 0:
                num_start_values += 1

    if num_start_values < 17:
        raise(UnsolvablePuzzleException())

iterations = 0
reductions = 0
evals = 0
global_board = None
def solve(board):
    global iterations
    global reductions
    global evals
    global global_board
    iterations = 0
    # reductions = 0
    #evals = 0
    global_board = board

    check_solvability(board)
    converted_board = convert_board_to_arrays(board)
    solved = recursive_solve(converted_board)
    reconverted = convert_array_to_board(solved)
    print("Solved in {} iterations {} evals {} reductions ({}%)".format(iterations, evals, reductions, int(100 * reductions / evals)))
    return reconverted

def sudoku(board):
    """
        alias for solve
    """
    return solve(board)

