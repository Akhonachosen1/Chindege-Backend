from django.http import JsonResponse
from game.tasks import start_new_round

def latest_crash_point(request):
    """
    Returns the latest crash multiplier.
    """
    new_round = start_new_round()
    return JsonResponse({
        "crash_point": new_round.crash_point
    })
