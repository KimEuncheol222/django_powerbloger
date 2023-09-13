from django.urls import path
from . import views


urlpatterns = [
    path('', views.board, name='board'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('post/', views.post, name='post'),
    path('write/', views.write, name='write'),
    path('find_password/', views.find_password, name='find_password'),
    path('new_password/', views.new_password, name='new_password'),
    path('search/', views.search_view, name='search'),
]
