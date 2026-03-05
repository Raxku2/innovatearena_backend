from razorpay import Client
import hashlib
import hmac
from dotenv import load_dotenv
from os import getenv
from app.models.payments import orderVerifyModel

load_dotenv()

RAZOR_KEY_ID = getenv("FA_RAZOR_KEY")
RAZOR_SECRATE = getenv("FA_RAZZOR_SEC")
client = Client(auth=(RAZOR_KEY_ID, RAZOR_SECRATE))


def orderCreator(notes: dict | None = None, order_amount: int = 5) -> dict | None:
    try:
        order_amount = order_amount * 100  # Amount in paise (50000 = ₹500)

        order_currency = "INR"

        order = client.order.create(
            {
                "amount": order_amount,
                "currency": order_currency,
                "payment_capture": 1,
                "notes": notes,
            }
        )

        if not order:
            return None

        return {
            "order_id": order.get("id"),
            "amount": order.get("amount"),
            "key": RAZOR_KEY_ID,
        }

    except Exception as err:
        raise Exception(f"{err} :Error while generating Payment Order")


def orderValidator(data: orderVerifyModel):
    try:
        generated_signature = hmac.new(
            RAZOR_SECRATE.encode(),
            f"{data.order_id}|{data.payment_id}".encode(),
            hashlib.sha256,
        ).hexdigest()

        if data.signeture != generated_signature:
            return False

        return True

    except Exception as err:
        raise Exception(f"{err} :Error while generating Payment Order")
