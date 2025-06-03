import secrets
from .engine import CrashGameEngine
from .models import GameRound  # Ensure this model exists and is correctly migrated

def start_new_round():
    """
    Starts a new game round with generated seeds and a calculated crash point.
    Saves the new round in the database.
    """
    # Generate seeds
    server_seed = secrets.token_hex(16)
    client_seed = secrets.token_hex(8)

    # Generate crash point using the game engine
    crash_point = CrashGameEngine.generate_crash_point(server_seed, client_seed)

    # Save the round to the database
    round_obj = GameRound.objects.create(
        crash_point=crash_point,
        server_seed=server_seed,
        client_seed=client_seed
    )

    return round_obj
