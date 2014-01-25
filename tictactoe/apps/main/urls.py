from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
     url(r'^api/', APIView.as_view(), name="api"),
     url(r'^', HomeView.as_view(), name="home"),
)
