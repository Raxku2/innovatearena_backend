from app.database.connection import user_coll
from bson import ObjectId
from app.utils.mongo_id_handeler import convert_objectid_in_doc
from bson import ObjectId


def createUser(username: str, useremail: str, userdp: str, team_id: ObjectId):
    try:

        status = user_coll.insert_one(
            {
                "username": username,
                "email": useremail,
                "dp": userdp,
                "type": "user",
                "name": username,
                "team_id": team_id,
            }
        )

        if status.inserted_id:
            return str(status.inserted_id)
        else:
            return False

    except Exception as err:
        print("Error while auth, add user on db: ", err)
        raise Exception(f"Error while auth, add user on db: {err}")


def viewUser(user_id: str | None = None, useremail: str | None = None):

    try:
        filter_data = {}

        if user_id is not None:
            filter_data["_id"] = ObjectId(user_id)

        if useremail is not None:
            filter_data["email"] = useremail

        status = user_coll.find_one(filter_data)

        if not status:
            return None
        print(status, "view")
        return convert_objectid_in_doc(status)

    except Exception as err:
        raise Exception(f"Error while show user on db: {err}")
