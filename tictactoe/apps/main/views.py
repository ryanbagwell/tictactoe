from django.views.generic.base import TemplateView, View, ContextMixin
from tictactoe.apps.main.game import TicTacToeGame
from django.http import HttpResponse
import json




class HomeView(TemplateView):
    template_name = 'home.html'


class APIView(ContextMixin, View):


    def get_context_data(self, **kwargs):
        return self._get_game(kwargs.get('game_id', None)).__dict__

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context):
        return HttpResponse(json.dumps(context),
                        content_type='application/json')

    def _get_game(self, game_id=None):
        return TicTacToeGame(game_id=game_id)