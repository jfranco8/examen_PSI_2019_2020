"""ratonGato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='landing'),
    path('index/', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_register, name='signup'),
    path('counter/', views.counter_service, name='counter'),
    path('create_game/', views.create_game_service, name='create_game'),
    path('join_game/', views.join_game_service, name='join_game'),
    path('select_game/', views.select_game_service, name='select_game'),
    path("select_game/<int:game_id>/", views.select_game_service,
         name="select_game"),
    path('select_game_mouse/', views.select_game_service_mouse,
         name='select_game_mouse'),
    path('select_game_cat/', views.select_game_service_cat,
         name='select_game_cat'),
    path("select_game_mouse/<int:game_id>/", views.select_game_service_mouse,
         name="select_game_mouse"),
    path("select_game_cat/<int:game_id>/", views.select_game_service_cat,
         name="select_game_cat"),
    path('show_game/', views.show_game_service, name='show_game'),
    path("move/", views.move_service, name="move"),
    path("instructions/", views.instructions, name="instructions"),
    path('replay_game/', views.replay_game, name='replay_game'),
    path('replay_game/<int:game_id>/', views.replay_game, name='replay_game'),
    path('replay_game/<int:game_id>/<int:move_id>', views.replay_game,
         name='replay_game'),
    path("get_move/", views.get_move, name="get_move"),
    path('select_replay_game/', views.replay_game_service,
         name='select_replay_game'),
    path("select_replay_game/<int:game_id>/", views.replay_game_service,
         name="select_replay_game"),
    path('select_replay_game_mouse/', views.replay_game_service_mouse,
         name='select_replay_game_mouse'),
    path('select_replay_game_cat/', views.replay_game_service_cat,
         name='select_replay_game_cat'),
    path("select_replay_game_mouse/<int:game_id>/",
         views.replay_game_service_mouse,
         name="select_replay_game_mouse"),
    path("select_replay_game_cat/<int:game_id>/",
         views.replay_game_service_cat,
         name="select_replay_game_cat"),
]
