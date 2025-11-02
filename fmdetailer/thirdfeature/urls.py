from django.urls import path
from . import views

urlpatterns = [

    path("", views.main_paige, name="main_paige"),
    
    path('analyze/', views.analyze_file, name='analyze_file'),
]