from django.core.cache import get_cache
import random
import uuid
import json


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
        trio of squares its its current state.

        Takes two arguments:

        1. a list representing a winnable sequence
        2. a game board

    """

    def __init__(self, lst, board):
        super(BoardSequence, self).__init__(lst)
        self.update(board)

    def update(self, board):
        self.squares = [v for k, v in board.iteritems() if k in self]
        self.ohs = self.squares.count('o')
        self.exes = self.squares.count('x')
        self.empties = self.squares.count('')
        self.occupied = 3 - self.empties
        self.diagonal = (self == [0,4,8] or self == [2,4,6])
        self.won = self.squares[0] if self.exes is 3 or self.ohs is 3 else False




class Board(dict):
    """ A Board object represents all of the game tiles. """

    sequences = []

    def __init__(self, data=None):

        if not data:
            data = self._get_new_board()

        super(Board, self).__init__(data)

        self._initialize_sequences()


    def update(self, new_board):
        pass


    def move(self, square, symbol):

        is_valid = self.validate_move(square, symbol)

        if is_valid:
            self[square] = symbol
            self._update_sequences()
            return True

        return False


    def validate_move(self, square, symbol):

        """ ensure that the symbol is an x or an o """
        if symbol is not 'x' and symbol is not 'o': return False

        """ ensure that the square is less than 9 """
        if square >= 9: return False

        """ ensure that the square is empty """
        if self[square] is not '': return False

        return True


    def _get_new_board(self):

        """ Create an empty dictionary with 9 places to
            represent our board """
        board = dict((v, '') for v in range(9))

        """ Pick a corner for the computer's first move """
        start = random.choice([0,2,6,8])

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

        for sequence in WINNING_SEQUENCES:
            self.sequences.append(BoardSequence(sequence, self))

    def _update_sequences(self):

        for sequence in self.sequences:
            sequence.update(self)

    def _get_player_squares(self):
        """ Returns lists of squares that each symbol has occupied """

        return {
            'x': self._get_occupied_squares(symbol='x'),
            'o': self._get_occupied_squares(symbol='o'),
        }

    def visualize(self):
        """ Prints a GUI representation of the board """

        vals = [ x if x else ' ' for x in self.values()]

        print '-' * 9
        print ' | '.join(vals[0:3])
        print '-' * 9
        print ' | '.join(vals[3:6])
        print '-' * 9
        print ' | '.join(vals[6:9])
        print '-' * 9

    def _get_winner(self):

        for sequence in self.sequences:
            #print sequence.won
            if sequence.won: return sequence.won







class TicTacToeGame(object):
    board = None
    game_id = None
    status = 'playing'
    _cache = get_cache('default')

    def __init__(self, game_id=None):

        """ Create a new game if we don't specify a game id """
        if game_id:
            self.game_id = game_id
        else:
            self.game_id = uuid.uuid1().hex

        if game_id:
            self.load_board(game_id)
        else:
            self.create_new_board()


    def load_board(self, game_id):

        """ Loads a board object from memory """

        self.board = self._cache.get(game_id)

    def create_new_board(self):

        """ Creates a new board object and saves it
            to the game cache """

        self.board = Board()
        self.save()

    def save(self):
        """ Saves a board object to memory cache """
        self._cache.set(self.game_id, self.board)


    def move(self, square, symbol):
        return self.board.move(square, symbol)


    def generate_move(self, symbol=None):

        """ Generate the computer's move by sorting
            the winning sequences based on the number of
            exes the sequences contains and
            whether it's a diagonal play.

            Moves are ranked in order of:

            1. Ability to complete a winning sequence

            2. Ability to prevent the user from completing a winning sequence

            3. An empty corner

            4. The number of exes in a winnable sequence

        """

        best = sorted(WINNING_SEQUENCES, self._rank_by_squares, reverse=True)

        """ Remove any fully occupied sequences """
        best = [b for b in best if BoardSequence(b, self.board).empties > 0]

        if symbol is None:
            player_squares = self.board._get_player_squares()
            symbol = 'x'
            if len(player_squares['x']) > len(player_squares['o']):
                symbol = 'o'

        for i in best[0]:
            if self.board[i] is '':
                return {
                    'square': i,
                    'symbol': symbol
                }


    def _rank_by_squares(self, seq1, seq2):

        """ Create a utility object for each sequence """
        seq1 = BoardSequence(seq1, self.board)
        seq2 = BoardSequence(seq2, self.board)

        """ Apply a numerical weight to each based on
            the numer of exes in each sequence and the
            number of occupied squares """

        rank1 = seq1.exes + seq1.occupied + (1 if seq1.diagonal else 0)
        rank2 = seq2.exes + seq2.occupied + (1 if seq2.diagonal else 0)

        return rank1 - rank2






