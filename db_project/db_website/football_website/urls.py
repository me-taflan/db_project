from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'football_website'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login/', views.LoginView, name='login'),
    path('Players/',views.player_page,name='player_page'),
    path('Players/<int:player_id>/',views.player_info_page,name='player_info'),
    #path('Leagues/<int:league_id>/',views.league_page,name='leagues'),
    #path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('signup/',views.signup,name='signup')
]