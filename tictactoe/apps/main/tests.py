from django.test import TestCase
from .game import TicTacToeGame




class GameTestCase(TestCase):

    def test_user_can_create_game(self):
        game = TicTacToeGame()
        self.assertIsNotNone(game.game_id, 'A new game should have a game ID')

    def test_user_can_retrieve_game(self):
        game = TicTacToeGame()
        retrieved_game = TicTacToeGame(game_id=game.game_id)
        self.assertIsNotNone(retrieved_game.game_id, 'A retrieved game should have a game ID')
        self.assertIsNotNone(retrieved_game.board, 'A retrieved game should have a board')
        self.assertIsInstance(retrieved_game.board, dict, 'A retrieved game should have a board that is a dictionary')









