from django.urls import path
from . import views

urlpatterns = [
    path("", views.workout_form, name="workout_form"),
    path("history/", views.history, name="history"),
    path("progress/", views.progress, name="progress"),
]

