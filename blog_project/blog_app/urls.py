from django.urls import path
from . import views

urlpatterns = [
    path('', views.board_client, name='board_client'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('board_admin', views.board_admin, name='board_admin'),
    path('post', views.post, name='post'),
    path('write', views.write, name='write'),
]
