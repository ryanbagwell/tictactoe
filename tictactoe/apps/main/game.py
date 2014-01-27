from django.core.cache import get_cache
from .exceptions import *
from functools import partial
import random
import uuid
import json


""" The list of winnable sequences """
WINNING_SEQUENCES = [
    (0, 4, 8),
    (2, 4, 6),
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
]


class BoardSequence(list):

    """ A utility object that represents a winnable
        trio of squares in its current state.

        Arguments:

        lst   -- list or tuple representing a winnable sequence
        board -- a dictionary representing a board

    """

    def __init__(self, lst, board):
        super(BoardSequence, self).__init__(lst)
        self.update(board)

    def update(self, board):
        """ Updates various informative values
            based on the value of the given board. """

        self.squares = [v for k, v in board.iteritems() if k in self]
        self.ohs = self.squares.count('o')
        self.exes = self.squares.count('x')
        self.empties = self.squares.count('')
        self.occupied = 3 - self.empties
        self.diagonal = (self == [0, 4, 8] or self == [2, 4, 6])
        self.won = self.squares[
            0] if self.exes is 3 or self.ohs is 3 else False

    def get_rank(self, symbol):
        """ Rank the importance of the sequence
            for placement purposes.

            Ranks are based on:

            2 - the sequence has two squares with given symbol
                and one empty square, and the game can be won

            1 - the sequence has two squares with the opposite
                symbol and one empty square, and should be blocked

            0 - a neutral ranking

            -1 - at least one square in the sequence contains the
                opposite symbol, and cannot be won, so we don't want
                to play it.

            Arguments:

            symbol -- the symbol to place in the square ('x' or 'o')

            Returns the numerical rank of sequence.

        """

        if self.squares.count(symbol) - self.empties == 2:
            return 2

        if 3 - self.squares.count(symbol) - self.empties == 2:
            return 1

        if 3 - self.squares.count(symbol) - self.empties > 0:
            return -1

        return 0


class Board(dict):

    """ A Board object represents all of the game tiles
        and provides methods for modifying the board and
        retrieving information about the board. """

    """ A list of BoardSequence instances """
    sequences = []

    def __init__(self, data=None):
        """ Create a new board if one is not provided """
        if not data:
            data = self._get_new_board()

        """ Call the parent method to initialze our list """
        super(Board, self).__init__(data)

        """ Populate the sequences list """
        self._initialize_sequences()

    def move(self, square, symbol):
        """ Places a symbol on a square if the
            placement is valid.

            Arguments:

            square -- an integer representing the square to place the symbol on
            symbol -- the symbol to place in the square ('x' or 'o')

            Returns True upon success, False on error

        """

        is_valid = self.validate_move(square, symbol)

        if is_valid:
            self[square] = symbol
            self._update_sequences()
            return True

        return False

    def validate_move(self, square, symbol):
        """ Validate's the proposed placement of a symbol
            in a square. Checks that:

            1. the symbol is an 'x' or an 'o'
            2. the square is between 0 and 9
            3. the target square is empty

            Arguments:

            square -- an integer representing the square to place the symbol on
            symbol -- the symbol to place in the square ('x' or 'o')

            Returns True if valid, raises an error if invalid

        """

        if symbol != 'x' and symbol != 'o':
            raise InvalidSymbol

        if 0 < square >= 9:
            raise InvalidSquare

        if self[square] is not '':
            raise NonEmptySquare

        return True

    def _get_new_board(self):
        """ Return a dictionary with 9 key->value pairs to
            represent our board, and place an 'x' in a corner
            of the board for the computer's first move """

        board = dict((v, '') for v in range(9))

        """ Pick a corner for the computer's first move """
        start = random.choice([0, 2, 6, 8])

        """ Then mark the corner as played """
        board[start] = 'x'

        return board

    def _get_empty_squares(self):
        """ Returns a list of squares that are empty """

        return [k for k, v in self.iteritems() if v is '']

    def _get_occupied_squares(self, symbol='xo'):
        """ Returns a list of squares that are occupied """

        return [k for k, v in self.iteritems() if v in list(symbol)]

    def _initialize_sequences(self):
        """ Creates instances of BoardSequence and
            adds them to self.sequences """

        for sequence in WINNING_SEQUENCES:
            self.sequences.append(BoardSequence(sequence, self))

    def _update_sequences(self):
        """ Updates each instance of BoardSequence
            in self.sequences
        """

        for sequence in self.sequences:
            sequence.update(self)

    def _get_player_squares(self):
        """ Returns lists of squares that each symbol has occupied """

        return {
            'x': self._get_occupied_squares(symbol='x'),
            'o': self._get_occupied_squares(symbol='o'),
        }

    def visualize(self):
        """ Prints a graphical representation of
            the board for development purposes.
        """

        vals = [x if x else ' ' for x in self.values()]

        print '\n' .join(['-' * 9,
                          ' | '.join(vals[0:3]),
                          '-' * 9,
                          ' | '.join(vals[3:6]),
                          '-' * 9,
                          ' | '.join(vals[6:9]),
                          '-' * 9,
                          ])

    def _get_winner(self):
        """ Get the game winner if one exists.

            Returns a tuple consisting of:

            winner   -- either 'x' or 'o', or None
            sequence -- a list representing the three squares, or None

        """

        self._update_sequences()

        for sequence in self.sequences:
            if sequence.won:
                return (sequence.won, sequence,)

        return (None, None)


class TicTacToeGame(object):

    """ A TicTacToeGame object represents a
        game and provides methods to create unique game IDs,
        place symbols in square and track the status of the game.

        This should only be instantiated once. When instantiated, it should be
        stored in the default cache using utils.save_game().
    """

    """ An instance of a Board object """
    board = None

    """ The game's unique ID """
    game_id = None

    """ The game's status (either 'game over' or 'in progress') """
    status = 'in progress'

    """ If the game has been won, identifies the winner ('x' or 'oh') """
    winner = None

    def __init__(self, game_id=None):
        """ Generate a game_id if we don't specify one """
        self.game_id = game_id or uuid.uuid4().hex

        """ Create a new Board() object """
        self.board = Board()

    def move(self, square, symbol):
        """ Place a symbol on a square, save the board,
            and return a response  with the result of the move.

            Arguments:

            square -- an integer representing the square to place the symbol on
            symbol -- the symbol to place in the square ('x' or 'o')

            Returns a boolean representing whether the placement was successful
        """

        if self.winner:
            raise GameOver

        result = self.board.move(square, symbol)

        self.update_status()

        return result

    def generate_move(self, symbol=None):
        """ Generate a move for the given symbol by comparing
            the importance of each winnable sequence. The rating
            criteria is contained in the board sequence.

            If no symbol is found, we determined what the next
            symbol should be.

            Arguments:

            symbol -- the symbol to generate a move for (either 'x' or 'o')

            Returns a dictionary consiting of:

            square -- an integer identifying the square to place the symbol on
            symbol -- the symbol to place in the square

        """

        if symbol is None:
            symbol = 'o' if self.board.values().count(
                'x') > self.board.values().count('o') else 'x'

        """ Wrap our comparison method in a function whose
            first argument is the symbol we want to place """
        cmp = partial(self.compare_ranks, symbol)

        """ Now call the comparison method """
        self.board._update_sequences()
        best = sorted(self.board.sequences, cmp, reverse=True)

        """ Remove any fully occupied sequences """
        best = [b for b in best if BoardSequence(b, self.board).empties > 0]

        return {
            'square': next(i for i in best[0] if self.board[i] is ''),
            'symbol': symbol
        }

    def compare_ranks(self, symbol, seq1, seq2):
        """ Compare the ranks of two sequences using sorted().

            Arguments:
            symbol -- the symbol to place on a square
            seq1   -- the first winable sequence to rank
            seq2   -- the other winable sequence to rank

        """

        return seq1.get_rank(symbol) - seq2.get_rank(symbol)

    def update_status(self):
        """ Update the status of the game. """

        self.winner, self.winning_sequence = self.board._get_winner()

        if len(self.board._get_empty_squares()) is 0:
            self.status = 'game over'
        elif self.winner:
            self.status = 'game over'
        else:
            self.status = 'in progress'
