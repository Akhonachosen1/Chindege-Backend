from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from game.services.payment_service import create_payment, check_payment_status
from game.serializers import UserSerializer, GameRoundSerializer
from game.tasks import start_new_round
from game.models import Bet, GameRound
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)


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


def check_payment_status(request):
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

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "id": user.id,
            "username": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
    return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
    return Response({"detail": "Invalid credentials"}, status=400)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_game(request):
    round_obj = start_new_round()
    serializer = GameRoundSerializer(round_obj)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_score(request):
    round_id = request.data.get('round_id')
    amount = request.data.get('amount')
    cash_out_multiplier = request.data.get('cash_out_multiplier')
    try:
        round_obj = GameRound.objects.get(id=round_id)
    except GameRound.DoesNotExist:
        return Response({'detail': 'Round not found'}, status=404)
    bet = Bet.objects.create(
        user_id=request.user.id,
        round=round_obj,
        amount=amount,
        cash_out_multiplier=cash_out_multiplier,
        cashed_out_at=now()
    )
    return Response({'id': bet.id})

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_leaderboard(request):
    bets = Bet.objects.exclude(cash_out_multiplier__isnull=True).order_by('-cash_out_multiplier')[:10]
    data = [
        {
            'user_id': b.user_id,
            'multiplier': b.cash_out_multiplier,
            'amount': str(b.amount)
        }
        for b in bets
    ]
    return Response({'leaderboard': data})

