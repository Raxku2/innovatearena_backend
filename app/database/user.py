from app.database.connection import user_coll
from app.models.user import userInfo
from bson import ObjectId
from app.utils.mongo_id_handeler import convert_objectid_in_doc


def showUserInfo(user_id: str):
    try:
        status = user_coll.find_one({"_id": ObjectId(user_id)})

        if not status:
            return None

        return convert_objectid_in_doc(status)

    except Exception as err:
        raise Exception(f"Error while getting user_info: {err}")


def updateUserInfo(data: userInfo, user_id: str):

    info_data = data.dict(exclude_unset=True, exclude_none=True)

    if not info_data:
        raise ValueError("No data provided for update")

    try:
        status = user_coll.update_one({"_id": ObjectId(user_id)}, {"$set": info_data})

        if status.matched_count == 0:
            raise Exception("User Not Found")

        if status.modified_count == 0:
            print("No Changes made")
            return False

        return True

    except Exception as err:
        raise Exception(f"error while update user_info: {err} ")
