import time
from django.core.management.base import BaseCommand
from game.tasks import start_new_round

class Command(BaseCommand):
    help = "Starts the crash game loop, creating new rounds continuously."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Crash game loop started. Press Ctrl+C to stop."))

        while True:
            round_obj = start_new_round()
            self.stdout.write(
                self.style.NOTICE(f"New round started: ID={round_obj.id}, Crash Point={round_obj.crash_point}")
            )
            time.sleep(10)  # Wait 10 seconds before starting the next round
