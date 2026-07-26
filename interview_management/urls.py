from django.urls import path
from . import views

urlpatterns = [
    path("", views.interview_list, name="interview_list"),
    path("add/", views.interview_create, name="interview_create"),
]