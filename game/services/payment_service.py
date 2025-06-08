from paynow import Paynow
from game.models import User, Transaction
import requests
from urllib.parse import parse_qs
import os

# Credentials now pulled from environment variables
PAYNOW_INTEGRATION_ID = os.getenv("PAYNOW_ID")
PAYNOW_INTEGRATION_KEY = os.getenv("PAYNOW_KEY")
PAYNOW_RETURN_URL = os.getenv("PAYNOW_RETURN_URL")
PAYNOW_RESULT_URL = os.getenv("PAYNOW_RESULT_URL")

paynow = Paynow(
    PAYNOW_INTEGRATION_ID,
    PAYNOW_INTEGRATION_KEY,
    PAYNOW_RETURN_URL,
    PAYNOW_RESULT_URL
)
paynow.testing = True  # sandbox mode


def create_payment(email: str, amount: float) -> dict:
    try:
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0], "password": "temporary"}
        )

        print(f"User used for payment: {user.username} (created={created})")

        payment = paynow.create_payment(email, 'Deposit')
        payment.add('Account Top-up', amount)

        response = paynow.send(payment)

        if response.success:
            Transaction.objects.create(
                email=email,
                amount=amount,
                poll_url=response.poll_url,
                reference=payment.reference,
                status="Pending"
            )
            return {
                "status": "success",
                "redirect_url": response.redirect_url,
                "poll_url": response.poll_url
            }
        else:
            return {
                "status": "error",
                "message": "Payment initiation failed"
            }

    except Exception as e:
        print("🔥 Exception in create_payment:", str(e))
        return {
            "status": "error",
            "message": str(e)
        }


def check_payment_status(poll_url: str) -> dict:
    print(">>> ENTERED check_payment_status")
    print(">>> poll_url type:", type(poll_url))
    print(">>> poll_url value:", poll_url)

    try:
        if not isinstance(poll_url, str):
            raise ValueError(f"poll_url must be a string, got {type(poll_url)}")

        response = requests.get(poll_url)

        if response.status_code == 200:
            parsed = parse_qs(response.text)
            return {
                "status": parsed.get("status", ["Unknown"])[0],
                "email": parsed.get("reference", [""])[0],
                "amount": parsed.get("amount", [""])[0],
                "paynow_reference": parsed.get("paynowreference", [""])[0],
                "raw": parsed
            }

        return {"status": "error", "message": f"HTTP error {response.status_code}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
