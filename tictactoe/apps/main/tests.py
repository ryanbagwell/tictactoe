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


    def test_new_game_should_have_no_winnable_sequences(self):

        game = TicTacToeGame()

        winnable_sequences = game.board._get_winnable_sequences()

        self.assertEqual(winnable_sequences, [])



    # def test_computer_should_generate_valid_move(self):

    #     game = TicTacToeGame()

    #     new_board = game.board.copy()

    #     squares = range(9)
    #     random.shuffle(squares)

    #     for i in squares:

    #         if new_board[i] is '':
    #             new_board[i] = 'o'
    #             break

    #     game.save_move(new_board)

    #     move = game.generate_move()

    #     game.save_move(move)


    # def test_computer_should_win_game(self):

    #     game = TicTacToeGame()

    #     while True:

    #         """ make the user move """
    #         new_board = game.board.copy()

    #         squares = range(9)
    #         random.shuffle(squares)

    #         for i in squares:

    #             if new_board[i] is '':
    #                 new_board[i] = 'o'
    #                 break

    #         print "saving user's move ..."
    #         if not game.save_move(new_board): break

    #         """ now make the computer move """
    #         move = game.generate_move()

    #         print "saving computer's move ..."
    #         if not game.save_move(move): break





























