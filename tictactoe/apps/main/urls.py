from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^game/(?P<game_id>[^/]*)/?(?P<method>[^/]*)/?$', APIView.as_view(), name="api"),
    url(r'^', HomeView.as_view(), name="home"),
)
