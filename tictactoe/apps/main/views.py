from django.views.generic.base import TemplateView, View, ContextMixin
from tictactoe.apps.main.game import TicTacToeGame
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import *
import json







class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        game = create_game()
        context.update(game=game)
        return context



class BaseAPIView(ContextMixin, View):

    """ A base view that contains common
        utilities to render a JSON response """

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        super(BaseAPIView, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        """ Remove the view item because it's not JSON serializable """

        context = super(BaseAPIView, self).get_context_data(**kwargs)
        if 'view' in context:
            del context['view']
        return context

    def get_json_response_params(self, result, message=None):
        """ Returns a basic status message that contains
            common information about all requests """

        return {
            'result': result,
            'message': message
        }

    def render_to_response(self, context):
        """ Produces a JSON HTTP response"""
        return HttpResponse(json.dumps(context),
                        content_type='application/json')






class NewGameView(BaseAPIView):
    """ Creates a new game and returns information
        about that game """

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        game = create_game()

        if game:
            info = self.get_json_response_params('success',
                'created new game with id %s' % game.game_id)
        else:
            info = self.get_json_response_params('error',
                'could not create new game')

        context.update(dict(info.items() + game.__dict__.items()))

        return self.render_to_response(context)


class ExistingGameView(BaseAPIView):
    """ Returns information about an existing game """

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        game = get_game(game_id=kwargs['game_id'])

        if game:
            info = self.get_json_response_params('success',
                'found game with id %s' % kwargs['game_id'])
        else:
            info = self.get_json_response_params('error',
                'could not get game with id %s' % kwargs['game_id'])

        context.update(dict(info.items() + game.__dict__.items()))

        return self.render_to_response(context)


class MakeMoveView(BaseAPIView):


    def post(self, request, *args, **kwargs):

        game_id = kwargs.get('game_id', None)
        symbol = request.POST.get('symbol', None)
        square = request.POST.get('square', -1)

        game = get_game(game_id)

        """ Play the user's move """

        try:
            game.move(symbol=symbol, square=int(square))
            info = self.get_json_response_params('success', 'placed "%s" in square %s' % (symbol, square))
        except Exception as e:
            info = self.get_json_response_params('error',
                getattr(e, 'message', None))

        """ Now generate a corresponding move for the computer if
            the game isn't over """

        try:
            computer_move = game.generate_move()
            game.move(symbol=computer_move['symbol'], square=computer_move['square'])

        except:
            print game

        context = self.get_context_data(**kwargs)

        context.update(dict(info.items() + game.__dict__.items()))

        save_game(game)

        return self.render_to_response(context)

