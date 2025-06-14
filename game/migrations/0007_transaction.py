# Generated by Django 5.2.1 on 2025-05-27 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_paymenttransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('poll_url', models.URLField(unique=True)),
                ('reference', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
