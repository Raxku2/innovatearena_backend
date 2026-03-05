from app.database.connection import user_coll, payments_coll, token_coll
from app.models.payments import orderVerifyModel, orderCreateNotes
from app.utils.mongo_id_handeler import convert_objectid_in_doc
from bson import ObjectId
from datetime import datetime


def mark_sucessful_payment(data: orderVerifyModel):
    try:
        status = user_coll.update_many(
            {"team_id": ObjectId(data.team_id)},
            {
                "$set": {
                    "payment_status": True,
                    "txn": data.payment_id,
                    "order_id": data.order_id,
                    "pay_by": data.username,
                    "payment_created_at": str(datetime.utcnow()),
                }
            },
        )
        payment_data = data.dict(exclude_unset=True, exclude_none=True)
        payment_data["payment_created_at"] = str(datetime.utcnow())
        payments_coll.insert_one(payment_data)

        if status.matched_count == 0:
            raise Exception("User Not Found")

        if status.modified_count == 0:
            print("No Changes made")
            return False

        return True

    except Exception as err:
        raise Exception(f"error while update user_info: {err} ")


def create_payment_token(user_id: str):
    try:
        user_data = user_coll.find_one(
            {"_id": ObjectId(user_id)},
            {"email": 1, "username": 1, "team_id": 1, "phone": 1},
        )
        if user_data:
            token_data = convert_objectid_in_doc(user_data)

        token_data["created_at"] = str(datetime.utcnow())

        status = token_coll.insert_one(token_data)

        if not status.inserted_id:
            return None

        return str(status.inserted_id)

    except Exception as err:
        raise Exception(f"error while update user_info: {err} ")


def read_payment_token(token: str):
    # token_data = data.dict()
    try:
        status = token_coll.find_one({"_id": ObjectId(token)}, {"_id": 0})

        if not status:
            return None

        return convert_objectid_in_doc(status)

    except Exception as err:
        raise Exception(f"error while update user_info: {err} ")
