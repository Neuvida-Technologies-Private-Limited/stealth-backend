from django.urls import path
from django.conf.urls import url
from . import views
from . import api

urlpatterns = [
    url(r'^api/v1/access/login/$', views.login_view, name='login-view'),
    url(r'^api/v1/access/refresh/$', views.custom_token_refresh_view, name='custom-token-refresh'),
    url(r'^api/v1/access/current-user/$', api.CurrentUserAPIView.as_view(), name='current-user'),
]
