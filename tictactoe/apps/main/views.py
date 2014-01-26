from django.views.generic.base import TemplateView, View, ContextMixin
from tictactoe.apps.main.game import TicTacToeGame
from django.http import HttpResponse
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

    def render_to_response(self, context):
        """ Produces a JSON HTTP response"""
        return HttpResponse(json.dumps(context),
                        content_type='application/json')

    def get_game(self, game_id=None):
        """ Convenience method to get the game with the given ID """
        return TicTacToeGame(game_id=game_id)




class NewGameView(BaseAPIView):
    """ Creates a new game and returns information
        about that game """

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        game = TicTacToeGame()
        context.update(game.__dict__)
        return self.render_to_response(context)


class ExistingGameView(BaseAPIView):
    """ Returns information about an existing game """

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        game = TicTacToeGame(game_id=kwargs['game_id'])
        context.update(game.__dict__)
        return self.render_to_response(context)



class GameOperationView(BaseAPIView):
    """ Perform the variius operations on a game.

        Ex: move

    """

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





    def _get_game(self, game_id=None):
        """ Convenience method to get the game with the given ID """
        return TicTacToeGame(game_id=game_id)


    def _get_response(self, result, message=None):
        """ Return a dictionary for inclusion in the json response """

        return {
            'result': result,
            'message': message,
        }



