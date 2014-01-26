from tictactoe.apps.main.game import TicTacToeGame
from django.core.cache import get_cache

cache = get_cache('default')

def get_game(game_id=None):
    return cache.get(game_id)


def save_game(game=None):

    if game:
        cache.set(game.game_id, game)
        return True

    return False


def create_game():
    game = TicTacToeGame()
    save_game(game)
    return game