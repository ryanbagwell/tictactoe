from django.test import TestCase
from .game import TicTacToeGame
from django.test import Client
from .exceptions import *
import random
import json




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

        """ Make the move and watch for the correct exception """
        self.assertRaises(InvalidSymbol, game.move, random.choice(empty), 'z')


    def test_cannot_overrwrite_occupied_square(self):
        game = TicTacToeGame()

        """ Find the occupied squares """
        occupied = game.board._get_occupied_squares()

        """ Make the move """
        self.assertRaises(NonEmptySquare, game.move, random.choice(occupied), 'o')


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

        self.assertRaises(NonEmptySquare, game.board.validate_move, symbol=symbol, square=square)


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


    def test_user_can_create_and_retrieve_saved_game_over_http(self):

        c = Client()

        response = c.get('/game/')

        data = json.loads(response.content)

        game_id = data['game_id']

        second_response = c.get('/game/%s/' % game_id)

        second_response_data = json.loads(second_response.content)

        self.assertEqual(game_id, second_response_data['game_id'])


    def test_user_can_make_valid_move_over_http(self):

        c = Client()

        """ start a new game """

        response = c.get('/game/')
        game_data = json.loads(response.content)


        """ load up our game object to generate a new move """
        game = TicTacToeGame(game_id=game_data['game_id'])

        """ generate the move """
        move = game.generate_move()

        response = c.post('/game/%s/move/' % game_data['game_id'], move)

    def test_computer_should_win_game_over_http(self):

        game = TicTacToeGame()

        c = Client()

        """ start a new game """

        response = c.get('/game/')
        game_data = json.loads(response.content)

        """ load up our game object to generate a new move """
        game = TicTacToeGame(game_id=game_data['game_id'])

        i = 0
        while i < 8:

            """ Generate the next move """
            move = game.generate_move()

            """ Make the request """
            response = c.post('/game/%s/move/' % game_data['game_id'], move)

            i = i +1

        print response











































