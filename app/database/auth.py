from app.database.connection import user_coll
from bson import ObjectId
from app.utils.mongo_id_handeler import convert_objectid_in_doc
from bson import ObjectId


def createUser(username: str, useremail: str, userdp: str, team_id: ObjectId):
    try:
        # update if exists, create if not
        status = user_coll.update_one(
            {"email": useremail},  # filter by email
            {
                "$set": {  # must use $set in update_one
                    "username": username,
                    "email": useremail,
                    "dp": userdp,
                    "type": "user",
                    "name": username,
                    "team_id": team_id,
                    "account": True,  # Python boolean
                }
            },
            upsert=True,
        )

        # if a new document was inserted
        if status.upserted_id:
            return str(status.upserted_id)

        # if the document already existed, fetch its _id
        existing_doc = user_coll.find_one({"email": useremail}, {"_id": 1})
        return str(existing_doc["_id"]) if existing_doc else False

    except Exception as err:
        print("Error while auth, add user on db:", err)
        raise Exception(f"Error while auth, add user on db: {err}")


def viewUser(user_id: str | None = None, useremail: str | None = None):

    try:
        filter_data = {"account": True}

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
