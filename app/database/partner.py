from app.database.connection import user_coll
from app.models.user import partnerInfo, partnerInfoUpdate
from app.utils.mongo_id_handeler import convert_objectid_in_doc
from bson import ObjectId


def showPartner(data: str) -> dict | None:

    try:
        status = user_coll.find_one({"email": data})

        if not status:
            return None

        return convert_objectid_in_doc(status)

    except Exception as err:
        raise Exception(f"error while get partner_info: {err} ")


def createPartner(data: partnerInfo, user_id: str):
    info_data = data.dict(exclude_unset=True, exclude_none=True)

    if not info_data.get("email"):
        raise ValueError("No data provided for update")

    try:
        partner_data = showPartner(info_data.get("email"))

        # FIX 1: Check if partner_data exists before checking payment status
        if partner_data and partner_data.get("payment_status") is True:
            return False

        user_data = user_coll.find_one(
            {"_id": ObjectId(user_id)}, {"name": 1, "email": 1, "team_id": 1}
        )

        # FIX 2: Check if user_data exists before proceeding
        if not user_data:
            raise Exception(f"User with ID {user_id} not found")

        partner_id = None

        if partner_data:
            # Now safe to use user_data.get()
            user_coll.update_one(
                {"_id": ObjectId(partner_data.get("_id")), "pay_status": {"$ne": True}},
                {
                    "$set": {
                        "partnerName": user_data.get("name"),
                        "partnerEmail": user_data.get("email"),
                        "partnerId": user_data.get("_id"),
                        "team_id": user_data.get("team_id"),
                    }
                },
            )
            partner_id = partner_data.get("_id")

        else:  # if not partner_data:
            partner_user_create_status = user_coll.insert_one(
                {
                    "username": info_data.get("name"),
                    "email": info_data.get("email"),
                    "type": "user",
                    "name": info_data.get("name"),
                    "partnerName": user_data.get("name"),
                    "partnerEmail": user_data.get("email"),
                    "partnerId": user_data.get("_id"),
                    "team_id": user_data.get("team_id"),
                }
            )
            partner_id = partner_user_create_status.inserted_id

        if not partner_id:
            return False

        # ... rest of your code

        user_update_status = user_coll.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "partnerName": info_data.get("name"),
                    "partnerEmail": info_data.get("email"),
                    "partnerId": ObjectId(partner_id),
                }
            },
        )

        if not user_update_status:
            return False

        return True

    except Exception as err:
        raise Exception(f"error while create partner: {err} ")


def updatePartner(user_id: str):
    try:
        partner_id = user_coll.find_one({"_id": ObjectId(user_id)}, {"partnerId": 1})

        if not partner_id:
            return False

        partner_data = user_coll.find_one(
            {"_id": ObjectId(partner_id.get("partnerId"))}, {"name": 1}
        )

        if not partner_data:
            return False

        user_update_status = user_coll.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"partnerName": partner_data.get("name")}},
        )

        if not user_update_status:
            return False

        return True

    except Exception as err:
        raise Exception(f"error while sync partner_info: {err} ")


def removePartner(user_id: str):
    try:
        partner_id = user_coll.find_one({"_id": ObjectId(user_id)}, {"partnerId": 1})

        if not partner_id:
            return False

        partner_update_status = user_coll.update_one(
            {"_id": ObjectId(partner_id.get("partnerId"))},
            {
                "$set": {"team_id": ObjectId()},
                "$unset": {"partnerName": 1, "partnerEmail": 1, "partnerId": 1},
            },
        )

        if not partner_update_status:
            return False

        user_update_status = user_coll.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {"team_id": ObjectId()},
                "$unset": {"partnerName": 1, "partnerEmail": 1, "partnerId": 1},
            },
        )

        if not user_update_status:
            return False

        return True

    except Exception as err:
        raise Exception(f"error while delete partner_info: {err} ")
