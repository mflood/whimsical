"""
    Find a shortest path through chutes and ladders board
"""
import queue

# number of sides on the die
DIE_FACES = 6

class _BoardSquare(object):
    """
        Internal Class

        A chutes and ladder board square
        keeps track of the previous square
        and previous roll that gave it it's die_rolls score

    """

    def __init__(self, square_number, die_rolls, previous_square, previous_roll):
        """
            square_number:
                In chutes and ladders, this would be
                From Square 1 to 100
            die_rolls:
                The number of times the die has been rolled to get to this square
            previous_square:
                The _BoardSquare from the previous "turn"
            previous_roll:
                What roll of the die led from the previous square to this one
        """
        self.square_number = square_number
        self.die_rolls = die_rolls
        self.previous_square = previous_square
        self.previous_roll = previous_roll


    def __repr__(self):
        if self.previous_square:
            ret = "roll %d -> %d" % (self.previous_roll, self.square_number)
        else:
            ret = "Start"
        return ret


class ChutesAndLaddersSolver(object):

    def __init__(self):
        # Board is a list for O(1) lookup
        self._board = [None for _ in range(100)]
        # defines the chutes and ladders on the board
        self._shortcuts = []
        # keeps track of squares that need to be processed
        self._board_square_queue = queue.Queue()

    def solve(self):
        """
            Start the process of solving the board
        """

        # Create the square the represents the beginning of the game when no-one is on the board
        # and add it to the queue
        #
        zero_square = _BoardSquare(square_number=0,
                                   die_rolls=0,
                                   previous_square=None,
                                   previous_roll=0)
        self._board_square_queue.put(zero_square)

        while not self._board_square_queue.empty():
            next_node = self._board_square_queue.get()
            square_number = next_node.square_number
            for die_value in range(0, DIE_FACES):
                roll = die_value + 1
                next_square_number = square_number + roll

                # when we are near the end, we will get
                # rolls that put us past the last square
                # we can skip those
                if next_square_number > 100:
                    continue

                # if the board square we land on is a chute or ladder
                # we jump to the target board square instead
                if next_square_number in self._shortcuts:
                    next_square_number = self._shortcuts[next_square_number]

                # Look up the square in the board list
                # which acts as a hash lookup on board square number
                try:
                    existing_square = self._board[next_square_number - 1]
                except Exception:
                    # this would happen if we tried to access the
                    # hash list oustside of its bounds
                    print "next_square_number: %d" % next_square_number
                    raise

                if existing_square == None:
                    # The square is not in the list yet, so this is
                    # the first time we have landed on it
                    # create a BoardSquare to represent it
                    # and add it to the hash-list
                    # and add it to the queue
                    square = _BoardSquare(square_number=next_square_number,
                                          die_rolls=next_node.die_rolls + 1,
                                          previous_square=next_node,
                                          previous_roll=roll)

                    self._board[next_square_number - 1] = square
                    self._board_square_queue.put(square)
                elif existing_square.die_rolls > next_node.die_rolls + 1:
                    existing_square.die_rolls = next_node.die_rolls + 1
                    existing_square.previous_square = next_node
                    existing_square.previous_roll = roll
                    self._board_square_queue.put(existing_square)

        #print(self)
        #self.print_solution()

    def print_solution(self):
        """
            Prints the boards squares you land on
            and the die roll needed to get through the board
        """
        solution_list = [self._board[99]]
        while solution_list[0].previous_square:
            solution_list.insert(0, solution_list[0].previous_square)

        for spot in solution_list:
            print spot 

    def setShortCuts(self):
        self._shortcuts = {
            1:38,
            5:14,
            9:31,
            16:6,
            28:84,
            36:44,
            40:42,
            47:26,
            49:11,
            51:67,
            56:53,
            62:19,
            64:60,
            71:91,
            80:100,
            87:24,
            93:73,
            95:75,
            98:78,
        }

    def __repr__(self):
        ret = ""
        for index, board_square in enumerate(self._board):

            ret += "\n%d: %s" % (index + 1, board_square)
        return ret

if __name__ == "__main__":

    solver = ChutesAndLaddersSolver()
    solver.setShortCuts()
    solver.solve()
    solver.print_solution()

