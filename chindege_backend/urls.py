from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # General
    path("", views.index, name="index"),

    # Payment APIs
    path("paynow/initiate/", views.initiate_payment, name="initiate_payment"),
    path("paynow/status/", views.check_payment_status, name="check_payment_status"),
    path("paynow/webhook/", views.paynow_webhook, name="paynow_webhook"),

    # User APIs
    path("api/register/", views.register_user, name="register_user"),
    path("api/login/", views.login_user, name="login_user"),
    path("api/profile/", views.get_user_profile, name="get_user_profile"),

    # Game APIs
    path("api/game/start/", views.start_game, name="start_game"),
    path("api/game/submit-score/", views.submit_score, name="submit_score"),
    path("api/game/leaderboard/", views.get_leaderboard, name="get_leaderboard"),
]
