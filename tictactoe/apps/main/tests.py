from django.test import TestCase
from .game import TicTacToeGame
from django.test import Client
from .exceptions import *
from .utils import *
import random
import json





class GameTestCase(TestCase):

    """ Tests for computer-generated situations """

    def test_can_create_game(self):
        game = create_game()

        self.assertIsNotNone(game.game_id, 'A new game should have a game ID')

    def test_can_retrieve_game(self):
        game = create_game()
        retrieved_game = get_game(game.game_id)
        self.assertIsNotNone(retrieved_game.game_id, 'A retrieved game should have a game ID')
        self.assertIsNotNone(retrieved_game.board, 'A retrieved game should have a board')
        self.assertIsInstance(retrieved_game.board, dict, 'A retrieved game should have a board that is a dictionary')

    def test_can_make_valid_move(self):

        """ Create a new game """

        game = create_game()

        """ Find the empty squares """
        empty = game.board._get_empty_squares()

        """ Make a move """
        result = game.move(random.choice(empty), 'o')

        """ Test the result """
        self.assertEqual(result, True)


    def test_cannot_add_invalid_symbol(self):
        game = create_game()

        """ Find the empty squares """
        empty = game.board._get_empty_squares()

        """ Make the move and watch for the correct exception """
        self.assertRaises(InvalidSymbol, game.move, random.choice(empty), 'z')


    def test_cannot_overrwrite_occupied_square(self):
        game = create_game()

        """ Find the occupied squares """
        occupied = game.board._get_occupied_squares()

        """ Make the move """
        self.assertRaises(NonEmptySquare, game.move, random.choice(occupied), 'o')


    def test_computer_should_generate_valid_move(self):

        """ Create a new game """

        game = create_game()

        """ Make a new move for the user """
        move = game.generate_move(symbol='o')

        result = game.board.validate_move(**move)

        """ Test the result """
        self.assertEqual(result, True)


    def test_invalid_move_should_not_be_valid(self):

        """ Create a new game """
        game = create_game()

        """ Get the occupied squares """
        occupied = game.board._get_occupied_squares()

        """ Choose a random square """
        square = random.choice(occupied)

        """ Try to fill the occupied square
            with the opposite symbol """
        symbol = 'x' if game.board[square] is 'o' else 'o'

        self.assertRaises(NonEmptySquare, game.board.validate_move, symbol=symbol, square=square)


    def test_computer_should_win_game(self):

        game = create_game()

        i = 0
        while i < 8:

            move = game.generate_move()

            game.board.move(**move)

            game.board.visualize()

            winner = game.board._get_winner()

            self.assertNotEqual(winner, 'o')

            if winner is 'x': break

            i = i +1


    """ Tests for HTTP Requests """

    def test_user_can_create_new_game(self):

        data = self._create_game()
        self.assertEqual(data['result'], 'success')


    def test_user_can_retrieve_existing_game(self):

        data = self._create_game()

        second_response_data = self._get_game(data['game_id'])

        self.assertEqual(second_response_data['result'], 'success')
        self.assertEqual(second_response_data['game_id'], data['game_id'])


    def test_user_can_make_valid_move_over_http(self):

        """ First, create a new game """
        game_data = self._create_game()

        """ Next, retrieve our game object from the cache
            and use it to generate a new move """
        game_obj = get_game(game_data['game_id'])
        move = game_obj.generate_move()

        """ Make the POST request to make the move """
        response = self._make_move(game_data['game_id'], move['symbol'], move['square'])

        """ JSON response should be 'success' """

        self.assertEqual(response['result'], 'success', response['message'])


    def test_computer_will_never_lose_over_http(self):
        """ To Do: also run this test by placing a sybol in a
            random empty square instead of generating the move
            based on our forced ranking """

        """ First, create a new game """
        response = self._create_game()

        while response.get('status', None) != 'game over':

            """ Get a copy of the game object
                to generate a move with """

            game_obj = get_game(response['game_id'])

            move = game_obj.generate_move()

            response = self._make_move(response['game_id'], move['symbol'], move['square'])

        self.assertNotEqual(response['winner'], 'o', 'Player "o" won.')


    """ Convenience methods """

    def _create_game(self):
        """ Makes a request to create a new game """

        c = Client()
        response = c.get('/game/')
        return json.loads(response.content)


    def _get_game(self, game_id):
        """ Makes a request to get an existing game information """

        c = Client()
        response = c.get('/game/%s/' % game_id)
        return json.loads(response.content)

    def _make_move(self, game_id, symbol, square):
        """ Makes a request to place a tile on a square """

        c = Client()
        response = c.post('/game/%s/move/' % game_id,
            dict(symbol=symbol, square=square))
        return json.loads(response.content)











































