from django.views.generic.base import TemplateView, View, ContextMixin
from tictactoe.apps.main.game import TicTacToeGame
from django.http import HttpResponse
import json




class HomeView(TemplateView):
    template_name = 'home.html'


class APIView(ContextMixin, View):


    def get_context_data(self, *args, **kwargs):
        context = super(APIView, self).get_context_data(*args, **kwargs)
        game_params = self._get_game(kwargs.get('game_id', None)).__dict__
        context.update(game_params)
        del context['view']
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):

        params = dict(kwargs.items() + request.POST.items())

        try:
            result = getattr(self, kwargs.get('method'))(**params)
        except AttributeError:
            result = self._get_response('error', 'success')

        context = self.get_context_data(**kwargs)

        context.update(result)

        return self.render_to_response(context)


    def move(self, **kwargs):

        """ Place a symbol on a square """
        game = self._get_game(game_id=kwargs['game_id'])

        square = int(kwargs.get('square'))
        symbol = unicode(kwargs.get('symbol'))

        try:
            game.move(square=square, symbol=symbol)
            return self._get_response('success', 'moved')

        except Exception as e:
            return self._get_response('error', e.message)


    def render_to_response(self, context):
        """ Override this method to produce an a json response"""
        return HttpResponse(json.dumps(context),
                        content_type='application/json')


    def _get_game(self, game_id=None):
        """ Convenience method to get the game with the given ID """
        return TicTacToeGame(game_id=game_id)


    def _get_response(self, result, message=None):
        """ Return a dictionary for inclusion in the json response """

        return {
            'result': result,
            'message': message,
        }



