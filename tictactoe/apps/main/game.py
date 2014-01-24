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
    """ A sequence is a winnable trio of squares """

    def __init__(self, lst, board):
        super(BoardSequence, self).__init__(lst)
        self.board = board
        self.update()

    def update(self):
        self.squares = [v for k, v in self.board.iteritems() if k in self]
        self.ohs = len(filter(lambda o: o == 'o', self.squares))
        self.exes = len(filter(lambda x: x == 'x', self.squares))
        self.empties = len(filter(lambda y: y == '', self.squares))
        self.diagonal = (self == [0,4,8] or self == [2,4,6])

        if self.exes is 2:
            self.winnable = 'x'
        elif self.ohs is 2:
            self.winnable = 'o'
        else:
            self.winnable = False


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

        result = self.validate_move(square, symbol)

        if result:
            self[square] = symbol
            return True

        self._update_sequences()

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
            sequence.update()

    def _get_winnable_sequences(self, symbol=None):

        if symbol:
            return [s for s in self.sequences if s.winnable is symbol]
        else:
            return [s for s in self.sequences if s.winnable]

    def _get_player_squares(self):
        """ Returns lists of squares that each symbol has occupied """

        return {
            'x': self._get_occupied_squares(symbol='x'),
            'o': self._get_occupied_squares(symbol='o'),
        }





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
            exes and whether it's a diagonal play.

            Moves are ranked in order of:

            1. Ability to complete a winning sequence

            2. Ability to prevent the user from completing a winning sequence

            3. An empty corner

            4. The number of exes in a winnable sequence

        """

        seq = sorted(WINNING_SEQUENCES, self._rank_by_squares, reverse=True)

        best = sorted(seq, self._rank_by_diagonal, reverse=True)[0]

        if symbol is None:
            player_squares = self.board._get_player_squares()
            symbol = 'x'
            if len(player_squares['x']) > len(player_squares['o']):
                symbol = 'o'

        for i in best:
            if self.board[i] is '':
                return {
                    'square': i,
                    'symbol': symbol
                }


    def _rank_by_squares(self, seq1, seq2):

        seq1 = BoardSequence(seq1, self.board)
        seq2 = BoardSequence(seq2, self.board)

        return seq1.exes - seq2.ohs

    def _rank_by_diagonal(self, seq1, seq2):

        seq1 = BoardSequence(seq1, self.board)
        seq2 = BoardSequence(seq2, self.board)

        if seq1.diagonal and not seq2.diagonal:
            return 1
        elif seq1.diagonal and seq2.diagonal:
            return 0

        return -1






