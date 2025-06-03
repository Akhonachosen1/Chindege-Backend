from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path("paynow/initiate/", views.initiate_payment, name="initiate_payment"),
    path("paynow/webhook/", views.paynow_webhook, name="paynow_webhook"),
]
