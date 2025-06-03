import time
import random
from django.utils.timezone import now
from game.models import GameRound
from game.engine import generate_crash_point

def start_new_round():
    server_seed = str(random.getrandbits(256))
    client_seed = str(random.getrandbits(256))
    crash_point = generate_crash_point(server_seed, client_seed)

    round = GameRound.objects.create(
        server_seed=server_seed,
        client_seed=client_seed,
        crash_point=crash_point,
        created_at=now()
    )
    return round

def game_loop():
    while True:
        round = start_new_round()
        print(f"[GAME STARTED] Crash Point: {round.crash_point}")
        multiplier = 1.00
        interval = 0.2

        while multiplier < round.crash_point:
            print(f"[MULTIPLIER] x{multiplier:.2f}")
            time.sleep(interval)
            multiplier += 0.01

        print("[GAME ENDED]")
        print("[TASKS] Round ended. Waiting for next round...\n")
        time.sleep(5)