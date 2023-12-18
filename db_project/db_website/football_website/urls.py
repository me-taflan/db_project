from django.urls import path
from . import views
app_name = 'football_website'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('match/<int:match_id>/', views.match_page, name='match_page'),
    path('league/<int:league_id>/', views.league_page, name='league_page'),
    path('team/<int:team_id>/', views.team_page, name='team_page'),
    path('Players/',views.player_page,name='player_page'),
    path('Players/<int:player_id>/',views.player_info_page,name='player_info')
]