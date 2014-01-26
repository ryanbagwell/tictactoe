from django.views.generic.base import TemplateView, View, ContextMixin
from tictactoe.apps.main.game import TicTacToeGame
from django.http import HttpResponse
from .utils import *
import json







class HomeView(TemplateView):
    template_name = 'home.html'



class BaseAPIView(ContextMixin, View):

    """ A base view that contains common
        utilities to render a JSON response """

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

        try:
            game.move(symbol=symbol, square=square)
            info = self.get_json_response_params('error',
                e.get('message', None))
        except Exception as e:
            info = self.get_json_response_params('error',
                getattr(e, 'message', None))

        context = self.get_context_data(**kwargs)
        context.update(dict(info.items() + game.__dict__.items()))

        return self.render_to_response(context)

