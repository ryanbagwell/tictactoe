from django.core.cache import get_cache
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

        return board



















