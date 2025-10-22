from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("player_analysis/", views.player_analysis, name = "player_analysis")
]