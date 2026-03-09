from razorpay import Client
from razorpay.errors import BadRequestError, ServerError
import hashlib
import hmac
from dotenv import load_dotenv
from os import getenv
from app.models.payments import orderVerifyModel
from app.database.connection import payments_coll, user_coll
from bson import ObjectId
from app.utils.mongo_id_handeler import (
    convert_objectid_in_doc,
    convert_objectid_in_list,
)

load_dotenv()

RAZOR_KEY_ID = getenv("FA_RAZOR_KEY")
RAZOR_SECRATE = getenv("FA_RAZZOR_SEC")
client = Client(auth=(RAZOR_KEY_ID, RAZOR_SECRATE))


def orderCreator(notes: dict | None = None, order_amount: int = 50) -> dict | None:
    try:
        order_amount = order_amount * 100  # Amount in paise (500 = ₹5)
        order_currency = "INR"

        order = client.order.create(
            {
                "amount": order_amount,
                "currency": order_currency,
                "notes": notes or {},
                # "payment_capture": 1 # Note: Usually handled in Razorpay Dashboard now
            }
        )

        if not order:
            return None

        return {
            "order_id": order.get("id"),
            "amount": order.get("amount"),
            "key": RAZOR_KEY_ID,  # Make sure RAZOR_KEY_ID is imported/defined
        }

    except Exception as err:
        print(f"Razorpay Order Creation Error: {err}")
        raise Exception(f"{err} :Error while generating Payment Order")


def orderValidator(data: orderVerifyModel) -> bool:
    try:
        # 🔹 FIX: Using the official Razorpay SDK utility is much safer
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": data.order_id,
                "razorpay_payment_id": data.payment_id,
                "razorpay_signature": data.signature,
            }
        )
        return True

    except razorpay.errors.SignatureVerificationError:
        print("Signature verification failed!")
        return False
    except Exception as err:
        print(f"Validation Error: {err}")
        return False


def load_order_info(payment_id: str, team_id: str):
    try:
        payment_data = convert_objectid_in_doc(
            payments_coll.find_one(
                {"team_id": team_id, "payment_id": payment_id},
                {"payment_created_at": 1, "username": 1, "_id": 0},
            )
        )

        if not payment_data:
            return None

        team_data = convert_objectid_in_list(
            user_coll.find(
                {"team_id": ObjectId(team_id)}, {"name": 1, "phone": 1, "_id": 0}
            )
        )

        if not team_data:
            return None

        # # The fetch method returns a dictionary containing the payment details
        payment_details = client.payment.fetch(payment_id)
        # print(payment_details)
        # data = {}
        payment_details["pay_data"] = payment_data
        payment_details["team_data"] = team_data

        return payment_details

    except BadRequestError as e:
        # Handles errors like an invalid payment ID
        print(f"Bad Request Error: {e}")
        return None
    except ServerError as e:
        # Handles Razorpay server-side issues
        print(f"Razorpay Server Error: {e}")
        return None
    except Exception as e:
        # Catch-all for network issues or other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None
