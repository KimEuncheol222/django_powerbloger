from django.urls import path
from . import views


urlpatterns = [
    path('', views.board_client, name='board_client'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup_view, name='signup'),
    path('board_admin', views.board_admin, name='board_admin'),
    path('post', views.post, name='post'),
    path('write', views.write, name='write'),
    path('find_password/', views.find_password, name='find_password'),
    path('new_password/<str:username>/', views.new_password, name='new_password'),
]
