import os
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
paynow.testing = True  # sandbox mode for development


def create_payment(email: str, amount: float) -> dict:
    """Initiate a payment with Paynow and store a pending transaction."""
    try:
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0], "password": "temporary"}
        )
        payment = paynow.create_payment(email, "Deposit")
        payment.add("Account Top-up", amount)
        response = paynow.send(payment)
        if response.success:
            Transaction.objects.create(
                email=email,
                amount=amount,
                poll_url=response.poll_url,
                reference=payment.reference,
                status="Pending",
            )
            return {
                "status": "success",
                "redirect_url": response.redirect_url,
                "poll_url": response.poll_url,
            }
        return {"status": "error", "message": "Payment initiation failed"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def check_payment_status(poll_url: str) -> dict:
    """Poll Paynow and update the transaction and user balance if paid."""
    if not isinstance(poll_url, str):
        return {"status": "error", "message": "poll_url must be a string"}

    try:
        response = requests.get(poll_url)
        if response.status_code != 200:
            return {"status": "error", "message": f"HTTP {response.status_code}"}

        parsed = parse_qs(response.text)
        status = parsed.get("status", ["Unknown"])[0]
        email = parsed.get("reference", [""])[0]
        amount = parsed.get("amount", ["0"])[0]
        paynow_ref = parsed.get("paynowreference", [""])[0]

        # Update transaction record if it exists
        txn = Transaction.objects.filter(poll_url=poll_url).first()
        if txn:
            txn.status = status
            txn.reference = paynow_ref or txn.reference
            txn.save(update_fields=["status", "reference", "updated_at"])

            if status == "Paid":
                user = User.objects.filter(email=email).first()
                if user:
                    user.balance = (user.balance or 0) + float(amount)
                    user.save(update_fields=["balance"])

        return {
            "status": status,
            "email": email,
            "amount": amount,
            "paynow_reference": paynow_re11111111111111111111111111111113.
          
          f
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
















































































































































































































































































































