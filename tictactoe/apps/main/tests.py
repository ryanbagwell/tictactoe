from django.test import TestCase
from .game import TicTacToeGame
import random




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

    def test_user_can_save_valid_move(self):
        game = TicTacToeGame()

        new_board = game.board.copy()

        squares = range(9)
        random.shuffle(squares)

        for i in squares:

            if new_board[i] is '':
                new_board[i] = 'o'
                break

        result = game.save_move(new_board)

        self.assertEqual(result, True)

    def test_user_cannot_save_invalid_move(self):
        game = TicTacToeGame()

        new_board = game.board.copy()

        for k,v in game.board.iteritems():

            if v is 'x':
                new_board[k] = 'o'
                break

        result = game.save_move(new_board)

        self.assertEqual(result, False)

    def test_computer_should_generate_valid_move(self):

        game = TicTacToeGame()

        new_board = game.board.copy()

        squares = range(9)
        random.shuffle(squares)

        for i in squares:

            if new_board[i] is '':
                new_board[i] = 'o'
                break

        game.save_move(new_board)

        game.generate_move()


























