from django.urls import path
from . import views


urlpatterns = [
    path('', views.board, name='board'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('write/', views.write, name='write'),
    path('post/<int:post_id>/', views.post, name='post'), 
    path('find_password/', views.find_password, name='find_password'),
    path('new_password/', views.new_password, name='new_password'),
    path('search/', views.search_view, name='search'),
    path('filter/daily/', views.filter_daily, name='filter_daily'),
    path('filter/cook/', views.filter_cook, name='filter_cook'),
    path('filter/travel/', views.filter_travel, name='filter_travel'),
    path('filter/movie/', views.filter_movie, name='filter_movie'),
    path('filter/it/', views.filter_it, name='filter_it'),
]
