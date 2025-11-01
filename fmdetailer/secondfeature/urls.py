from django.urls import path
from . import views

urlpatterns = [
    path("similar_players/", views.main, name="main"),
    path('analyze/', views.run_similarity_analysis, name='run_analysis')
]