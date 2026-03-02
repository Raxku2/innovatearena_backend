from app.database.connection import user_coll, payments_coll
from app.models.payments import orderVerifyModel
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
