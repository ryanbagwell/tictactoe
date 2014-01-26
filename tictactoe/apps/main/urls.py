from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^game/$', NewGameView.as_view(), name="new-game"),
    url(r'^game/(?P<game_id>[^/]*)/$', ExistingGameView.as_view(), name="existing-game"),
    url(r'^game/(?P<game_id>[^/]*)/?(?P<method>[^/]*)/?$', GameOperationView.as_view(), name="game-operation"),
    url(r'^', HomeView.as_view(), name="home"),
)
