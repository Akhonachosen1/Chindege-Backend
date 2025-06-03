from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from game.services.payment_service import create_payment, check_payment_status


def index(request):
    return HttpResponse("Welcome to Chindege Backend!")


def initiate_payment(request):
    email = request.GET.get("email")
    amount = request.GET.get("amount")

    if not email or not amount:
        return JsonResponse({"status": "error", "message": "Email and amount are required"}, status=400)

    try:
        amount = float(amount)
        result = create_payment(email, amount)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def paynow_status(request):
    # ✅ FIX: Extract poll_url cleanly as a string before doing anything else
    poll_url = request.GET.get("poll_url", "").strip()

    if not poll_url:
        return JsonResponse({"status": "error", "message": "Missing poll_url"}, status=400)

    if not isinstance(poll_url, str) or not poll_url.startswith("http"):
        return JsonResponse({"status": "error", "message": "Invalid poll_url"}, status=400)

    try:
        # ✅ Only now call the status checker
        result = check_payment_status(poll_url)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
def paynow_webhook(request):
    return JsonResponse({"status": "received"})
