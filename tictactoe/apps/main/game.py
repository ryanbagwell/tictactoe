from django.core.cache import get_cache
import random
import uuid
import json

game_cache = get_cache('default')

class TicTacToe(object):

    def __init__(self, game_id=None):

        if game_id:
            self.game = self.get_game(game_id)
        else:
            self.game = self.get_new_game()


    def get_game(self, game_id):
        game = game_cache.get(game_id)
        return json.loads(game)


    def get_new_game(self):

        """ Create an empty dictionary with 9 places for
            our moves """
        game = dict((v, '') for v in range(9))

        """ Pick a corner for the computer's first move """
        start = random.choice('0,2,6,8')

        """ Then mark the corner as played """
        self.game[start] = 'x'

        """ Generate a random id to assign to our game """
        game_id = uuid.uuid1().hex

        """ Place it in memory and return it """
        game_cache.set(game_id, self.game)

        return game



















