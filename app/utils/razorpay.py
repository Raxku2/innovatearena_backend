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
            "key": RAZOR_KEY_ID, # Make sure RAZOR_KEY_ID is imported/defined
        }

    except Exception as err:
        print(f"Razorpay Order Creation Error: {err}")
        raise Exception(f"{err} :Error while generating Payment Order")
# def orderCreator(notes: dict | None = None, order_amount: int = 5) -> dict | None:
#     try:
#         order_amount = order_amount * 100  # Amount in paise (50000 = ₹500)

#         order_currency = "INR"

#         order = client.order.create(
#             {
#                 "amount": order_amount,
#                 "currency": order_currency,
#                 "payment_capture": 1,
#                 "notes": notes,
#             }
#         )

#         if not order:
#             return None

#         return {
#             "order_id": order.get("id"),
#             "amount": order.get("amount"),
#             "key": RAZOR_KEY_ID,
#         }

#     except Exception as err:
#         raise Exception(f"{err} :Error while generating Payment Order")

def orderValidator(data: orderVerifyModel) -> bool:
    try:
        # 🔹 FIX: Using the official Razorpay SDK utility is much safer
        client.utility.verify_payment_signature({
            'razorpay_order_id': data.order_id,
            'razorpay_payment_id': data.payment_id,
            'razorpay_signature': data.signature 
        })
        return True

    except razorpay.errors.SignatureVerificationError:
        print("Signature verification failed!")
        return False
    except Exception as err:
        print(f"Validation Error: {err}")
        return False
# def orderValidator(data: orderVerifyModel):
#     try:
#         generated_signature = hmac.new(
#             RAZOR_SECRATE.encode(),
#             f"{data.order_id}|{data.payment_id}".encode(),
#             hashlib.sha256,
#         ).hexdigest()

#         if data.signeture != generated_signature:
#             return False

#         return True

#     except Exception as err:
#         raise Exception(f"{err} :Error while generating Payment Order")
