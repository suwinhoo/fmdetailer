from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("player_analysis/", views.index, name = "player_analysis")
]