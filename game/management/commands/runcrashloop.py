# game/management/commands/runcrashloop.py
from django.core.management.base import BaseCommand
from game.tasks import game_loop
import asyncio

class Command(BaseCommand):
    help = 'Starts the crash game loop'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting crash game loop..."))
        asyncio.run(game_loop())
