from django.urls import path
from . import views

urlpatterns = [
    path("similar_players/", views.main, name="main"),
]