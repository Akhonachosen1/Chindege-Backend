import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chindege_backend.settings')

import django
django.setup()

import asyncio
import threading
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import game.routing
from game.tasks import game_loop  # your async game loop

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            game.routing.websocket_urlpatterns
        )
    ),
})

def start_game():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(game_loop())

# Start the game loop in a separate thread
threading.Thread(target=start_game, daemon=True).start()
