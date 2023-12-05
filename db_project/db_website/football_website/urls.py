from django.urls import path
from . import views
app_name = 'football_website'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('Players/',views.player_page,name='player_page'),
    path('Players/<int:player_id>/',views.player_info_page,name='player_info')
]