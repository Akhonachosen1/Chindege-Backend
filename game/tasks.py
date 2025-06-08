import asyncio
import random
from django.utils.timezone import now
from channels.layers import get_channel_layer
from game.models import GameRound
from game.engine import generate_crash_point


def start_new_round() -> GameRound:
    server_seed = str(random.getrandbits(256))
    client_seed = str(random.getrandbits(256))
    crash_point = generate_crash_point(server_seed, client_seed)
    return GameRound.objects.create(
        server_seed=server_seed,
        client_seed=client_seed,
        crash_point=crash_point,
        created_at=now(),
    )


async def game_loop() -> None:
    channel_layer = get_channel_layer()
    while True:
        round_obj = start_new_round()
        multiplier = 1.0
        interval = 0.2
        # broadcast multiplier updates until crash
        while multiplier < round_obj.crash_point:
            if channel_layer:
                await channel_layer.group_send(
                    "game_updates",
                    {"type": "send_multiplier", "multiplier": round(multiplier, 2)},
                )
            await asyncio.sleep(interval)
            multiplier += 0.01
        # final crash notification
        if channel_layer:
            await channel_layer.group_send(
                "game_updates",
                {"type": "send_multiplier", "multiplier": "crash"},
            )
        await asyncio.sleep(5)

