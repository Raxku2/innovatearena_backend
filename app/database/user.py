from app.database.connection import user_coll, event_coll
from app.models.user import userInfo, projectSubmit
from bson import ObjectId
from app.utils.mongo_id_handeler import convert_objectid_in_doc
from fastapi import Request
from app.utils.tracker import get_client_ip
from app.database.venue_ip import get_venue_ip


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


def is_user_admin(user_id: str):
    try:
        status = user_coll.find_one({"_id": ObjectId(user_id), "type": "root"})

        if not status:
            return False

        return True

    except Exception as err:
        raise Exception(f"error verify user_admin: {err} ")


def mark_attendence(team_id: str, request: Request):
    try:
        client_IP = get_client_ip(request=request)
        if client_IP != get_venue_ip():
            return None

        event_attend_status = event_coll.find_one(
            {"_id": "event"}, {"_id": 0, "attendence_process": 1}
        )
        if event_attend_status["attendence_process"] == False:
            return None

        status = user_coll.update_many(
            {"team_id": ObjectId(team_id)}, {"$set": {"present": True}}
        )

        if status.modified_count == 0:
            return False

        return True

    except Exception as err:
        raise Exception(f"error verify user_admin: {err} ")


def add_submits(team_id: str, data: projectSubmit, request: Request):
    try:
        client_IP = get_client_ip(request=request)
        if client_IP != get_venue_ip():
            return None

        project_data = data.dict()
        project_data["project_id"] = ObjectId()

        status = user_coll.update_many(
            {"team_id": ObjectId(team_id)}, {"$set": project_data}
        )

        if status.modified_count == 0:
            return False

        return True

    except Exception as err:
        raise Exception(f"error verify user_admin: {err} ")
