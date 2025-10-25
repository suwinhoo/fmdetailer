from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("player_analysis/", views.player_analysis, name="player_analysis"),
    path("add_player/", views.add_player, name="add_player"),
    path("import_player/", views.import_player, name="import_player"),  
    path("player/<str:player_name>/", views.player_detail, name="player_detail")
]