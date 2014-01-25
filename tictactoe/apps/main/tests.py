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

    def test_can_make_valid_move(self):

        """ Create a new game """

        game = TicTacToeGame()

        """ Find the empty squares """
        empty = game.board._get_empty_squares()

        """ Make a move """
        result = game.move(random.choice(empty), 'o')

        """ Test the result """
        self.assertEqual(result, True)


    def test_cannot_add_invalid_symbol(self):
        game = TicTacToeGame()

        """ Find the empty squares """
        empty = game.board._get_empty_squares()

        """ Make the move """
        result = game.move(random.choice(empty), 'z')

        """ Test the result """
        self.assertEqual(result, False)


    def test_cannot_overrwrite_occupied_square(self):
        game = TicTacToeGame()

        """ Find the occupied squares """
        occupied = game.board._get_occupied_squares()

        """ Make the move """
        result = game.move(random.choice(occupied), 'o')

        """ Test the result """
        self.assertEqual(result, False)


    def test_computer_should_generate_valid_move(self):

        """ Create a new game """

        game = TicTacToeGame()

        """ Make a new move for the user """
        move = game.generate_move(symbol='o')

        result = game.board.validate_move(**move)

        """ Test the result """
        self.assertEqual(result, True)


    def test_invalid_move_should_not_be_valid(self):

        """ Create a new game """
        game = TicTacToeGame()

        """ Get the occupied squares """
        occupied = game.board._get_occupied_squares()

        """ Choose a random square """
        square = random.choice(occupied)

        """ Try to fill the occupied square
            with the opposite symbol """
        symbol = 'x' if game.board[square] is 'o' else 'o'

        result = game.board.validate_move(symbol=symbol, square=square)

        """ Test the validation result """
        self.assertEqual(result, False)



    def test_computer_should_win_game(self):

        game = TicTacToeGame()

        i = 0
        while i < 8:

            move = game.generate_move()

            game.board.move(**move)

            game.board.visualize()

            winner = game.board._get_winner()

            self.assertNotEqual(winner, 'o')

            if winner is 'x':
                print "Computer won"
                return

            i = i +1






























