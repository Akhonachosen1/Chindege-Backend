from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)



class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey('GameRound', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cashout_multiplier = models.FloatField(null=True, blank=True)
    placed_at = models.DateTimeField(auto_now_add=True)
    cashed_out = models.BooleanField(default=False)
    from django.utils import timezone
    cashed_out_at = models.DateTimeField(null=True, blank=True)


class GameRound(models.Model):
    crash_point = models.FloatField()
    server_seed = models.CharField(max_length=64)
    client_seed = models.CharField(max_length=64)
    created_at = models.DateTimeField(default=now)
