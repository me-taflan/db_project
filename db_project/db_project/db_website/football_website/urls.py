from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'football_website'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('match/<int:match_id>/', views.match_page, name='match_page'),
    path('league/<int:league_id>/', views.league_page, name='league_page'),
    path('team/<int:team_id>/', views.team_page, name='team_page'),
    path('Players/',views.player_page,name='player_page'),
    path('Players/<int:player_id>/',views.player_info_page,name='player_info'),
    path('signup/',views.signup,name='signup'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add_favorite_match/<int:match_id>/<str:username>/', views.add_favorite_match, name='add_favorite_match'),
    path('add_favorite_team/<int:team_id>/<str:username>/', views.add_favorite_team, name='add_favorite_team'),
    path('fav_page/<str:username>/', views.fav_page, name='fav_page'),
    path('remove_favorite_match/<str:username>/<int:match_id>/', views.remove_favorite_match, name='remove_favorite_match'),
    path('remove_favorite_team/<str:username>/<int:team_id>/', views.remove_favorite_team, name='remove_favorite_team'),
]