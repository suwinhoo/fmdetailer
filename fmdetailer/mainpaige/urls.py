from django.urls import path
from . import views
from . import file_change

urlpatterns = [
    path("", views.index, name="index"),
    path("player_analysis/", views.player_analysis, name="player_analysis"),
    path("add_player/", views.add_player, name="add_player"),
    path("import_player/", views.import_player, name="import_player"),  
    path("player/<str:player_name>/", views.player_detail, name="player_detail"),
    path("file_change/", file_change.render_file_change, name = "render_file_change"),
    path('analyze_file/', file_change.analyze_file_view, name='analyze_file_view')
]