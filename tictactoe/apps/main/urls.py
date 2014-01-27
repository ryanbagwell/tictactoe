from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
                       url(r'^game/$', NewGameView.as_view(), name="new-game"),
                       url(r'^game/(?P<game_id>[^/]*)/$',
                           ExistingGameView.as_view(), name="existing-game"),
                       url(r'^game/(?P<game_id>[^/]*)/move/$',
                           MakeMoveView.as_view(), name="make-move"),
                       url(r'^', HomeView.as_view(), name="home"),
                       )
