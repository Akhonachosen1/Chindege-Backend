from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class GameRound(models.Model):
    server_seed = models.CharField(max_length=64)
    client_seed = models.CharField(max_length=64)
    crash_point = models.FloatField()
    created_at = models.DateTimeField(default=now)

class Bet(models.Model):
    user_id = models.IntegerField()  # Use ForeignKey in production
    round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cash_out_multiplier = models.FloatField(null=True, blank=True)
    cashed_out_at = models.DateTimeField(null=True, blank=True)

class User(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class PaymentTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    poll_url = models.URLField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    poll_url = models.URLField(unique=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, default='Pending')  # e.g. Pending, Paid, Cancelled
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.amount} ({self.status})"
