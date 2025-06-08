# Chindege Backend

This project requires several environment variables for interacting with the Paynow service:

- `PAYNOW_ID` – Paynow integration ID
- `PAYNOW_KEY` – Paynow integration key
- `PAYNOW_RETURN_URL` – URL users are redirected to after payment
- `PAYNOW_RESULT_URL` – URL that receives Paynow payment status notifications

Set these variables in your deployment environment so that `game/services/payment_service.py` can access them at runtime.
