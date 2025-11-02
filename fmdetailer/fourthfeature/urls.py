from django.urls import path
from . import views

urlpatterns = [
    path("", views.position_picker_view, name="position_picker_view"),
    path("process/", views.process_position_file, name="process_position_file"),
]