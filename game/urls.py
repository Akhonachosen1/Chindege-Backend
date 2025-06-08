from django.urls import path
from . import views

urlpatterns = [
    path("latest-crash-point/", views.latest_crash_point, name="latest_crash_point"),
]
