from django.core.cache import get_cache
from .utils import Sequence, WINNING_SEQUENCES
import random
import uuid
import json

game_cache = get_cache('default')



class TicTacToeGame(object):
    board = None
    game_id = None

    def __init__(self, game_id=None):

        if game_id:
            self.board = self.get_game(game_id)
        else:
            self.board = self.get_new_game()


    def get_game(self, game_id):
        game = game_cache.get(game_id)
        self.game_id = game_id
        return game


    def get_new_game(self):

        """ Create an empty dictionary with 9 places to
            represent our board """
        board = dict((v, '') for v in range(9))

        """ Pick a corner for the computer's first move """
        start = random.choice([0,2,6,8])

        """ Then mark the corner as played """
        board[start] = 'x'

        """ Generate a random id to assign to our game """
        self.game_id = uuid.uuid1().hex

        """ Place it in memory and return it """
        game_cache.set(self.game_id, board)

        #print board.get_available_sequences()

        return board

    def save_move(self, new_board):
        """ save the user's move """

        if not self.validate_move(new_board): return False
        game_cache.set(self.game_id, new_board)
        self.board = new_board

        return True


    def validate_move(self, new_board):

        old = set(self.board.items())
        new = set(new_board.items())

        result = old.difference(new)

        """ Ensure there is exactly one new move,
            and it is an 'o' """

        if len(result) is not 1: return False

        """ Ensure we're not changing a square that has
            an 'x' or an 'o' """

        changed_square = iter(result).next()[0]

        if self.board[changed_square] is 'x' or self.board[changed_square is 'o']: return False

        return True


    def generate_move(self):
        """ Generate the computer's move by searching
            the winning sequences for the best way to win """

        print self.board

        seq = sorted(WINNING_SEQUENCES, self._rank_by_squares, reverse=True)
        seq = sorted(seq, self._rank_by_diagonal, reverse=True)[0]


    def _rank_by_squares(self, seq1, seq2):

        seq1 = Sequence(seq1, self.board)
        seq2 = Sequence(seq2, self.board)

        return seq1.exes - seq2.ohs

    def _rank_by_diagonal(self, seq1, seq2):

        seq1 = Sequence(seq1, self.board)
        seq2 = Sequence(seq2, self.board)

        if seq1.diagonal and not seq2.diagonal:
            return 1
        elif seq1.diagonal and seq2.diagonal:
            return 0

        return -1






