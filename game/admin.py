from django.contrib import admin
from .models import User, GameRound, Bet

admin.site.register(User)
admin.site.register(GameRound)
admin.site.register(Bet)
