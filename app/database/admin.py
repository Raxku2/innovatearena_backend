from app.database.connection import user_coll
from app.database.user import is_user_admin
from bson import ObjectId
from app.utils.mongo_id_handeler import (
    convert_objectid_in_list,
    convert_objectid_in_doc,
)
from collections import defaultdict


def read_all_judges():
    try:
        result = user_coll.find({"judge": True}, {"email": 1, "_id": 0})

        if not result:
            return False

        return convert_objectid_in_list(result)

    except Exception as err:
        raise Exception(f"{err} : while get judges")


def removeJudge(judge_email: str):
    try:
        result = user_coll.update_one(
            {"email": judge_email}, {"$set": {"judge": False}}
        )

        if result.matched_count == 0:
            return False

        return True

    except Exception as err:
        raise Exception(f"{err} : while remove judge")


def setJudge(judge_email: str):
    try:
        result = user_coll.update_one({"email": judge_email}, {"$set": {"judge": True}})

        if result.matched_count == 0:
            return False

        return True

    except Exception as err:
        raise Exception(f"{err} : while make judge")


def readAttendance(root_id: str):
    try:
        if not is_user_admin(root_id):
            raise Exception("Unauth")
        data = {}

        data["2026"] = len(
            convert_objectid_in_list(
                user_coll.find({"batch": "2026", "present": True}, {"_id": 1})
            )
        )

        data["2027"] = len(
            convert_objectid_in_list(
                user_coll.find({"batch": "2027", "present": True}, {"_id": 1})
            )
        )

        data["2028"] = len(
            convert_objectid_in_list(
                user_coll.find({"batch": "2028", "present": True}, {"_id": 1})
            )
        )

        data["2029"] = len(
            convert_objectid_in_list(
                user_coll.find({"batch": "2029", "present": True}, {"_id": 1})
            )
        )

        data["2030"] = len(
            convert_objectid_in_list(
                user_coll.find({"batch": "2030", "present": True}, {"_id": 1})
            )
        )

        # if not result:
        #     return None

        return data

    except Exception as err:
        raise Exception(f"{err} : while read admins")


def showStatics(root_id: str):
    try:
        if not is_user_admin(root_id):
            raise Exception("Unauth")

        data = {}

        data["users_email"] = [
            doc["email"] for doc in user_coll.find({}, {"email": 1, "_id": 0})
        ]

        years = ["2026", "2027", "2028", "2029", "2030"]
        departments = ["ECE", "CSE", "BSHU", "EE", "ME", "CIVIL"]

        pipeline = [
            {
                "$match": {
                    "reg_status": True,
                    "payment_status": True,
                    "batch": {"$in": years},
                    "dept": {"$in": departments},
                }
            },
            {
                "$group": {
                    "_id": {"dept": "$dept", "batch": "$batch"},
                    "count": {"$sum": 1},
                }
            },
        ]

        result = list(user_coll.aggregate(pipeline))

        # Initialize output with 0 counts (guaranteed structure)
        output = {dept: {year: 0 for year in years} for dept in departments}

        # Fill actual counts
        for doc in result:
            dept = doc["_id"]["dept"]
            batch = doc["_id"]["batch"]
            output[dept][batch] = doc["count"]

        data.update(output)

        pipeline = [
            {
                "$match": {
                    "reg_status": True,
                    "payment_status": True,
                    "team_id": {
                        "$exists": True,
                        "$ne": None,
                    },  # ensure team_id exists and is not null
                }
            },
            {"$group": {"_id": "$team_id"}},  # group by team_id to remove duplicates
            {"$count": "total_unique_teams"},  # count total unique team_id
        ]

        result = list(user_coll.aggregate(pipeline))

        if result:
            data["team_count"] = result[0]["total_unique_teams"]
        else:
            data["team_count"] = 0

        return data

    except Exception as err:
        raise Exception(f"{err} : while make staticties")


def showAdmin(root_id: str) -> list | None:
    try:
        if not is_user_admin(root_id):
            raise Exception("Unauth")

        result = user_coll.find({"type": "root"}, {"email": 1, "_id": 0})

        if not result:
            return None

        return convert_objectid_in_list(result)

    except Exception as err:
        raise Exception(f"{err} : while read admins")


def setAdmin(root_id: str, target_id: str, param: str):
    try:
        if not is_user_admin(root_id):
            raise Exception("Unauth")

        result = user_coll.update_one({"email": target_id}, {"$set": {"type": param}})

        if result.matched_count == 0:
            return False

        return True

    except Exception as err:
        raise Exception(f"{err} : while make admin")


def getRegInfo(root_id: str):
    try:
        if not is_user_admin(root_id):
            raise Exception("Unauth")

        data_cursor = user_coll.find(
            {"payment_status": True},
            {
                "team_id": 1,
                "name": 1,
                "dept": 1,
                "batch": 1,
                "phone": 1,
                "present": 1,
                "reg_status": 1,
            },
        )

        # Initialize a dictionary to group by team_id
        grouped_dict = defaultdict(list)

        for user in data_cursor:
            # Clean the ObjectId
            clean_user = convert_objectid_in_doc(user)
            tid = clean_user.get("team_id")

            # Optimization: Just append the whole dictionary directly
            # instead of recreating it key-by-key
            grouped_dict[tid].append(clean_user)

        # Format the final output to match the flat CSV requirement with visual grouping
        data = []
        team_counter = 1
        for tid, members in grouped_dict.items():
            for index, member in enumerate(members):
                display_tid = team_counter if index == 0 else ""

                # Safely extract values so we don't overwrite actual False booleans
                reg_status = member.get("reg_status")
                present_status = member.get("present")

                data.append(
                    {
                        "team id": display_tid,
                        "Name": member.get("name") or "",
                        # If None or empty string, default to False. Otherwise, keep original value.
                        "Profile": (False if reg_status in [None, ""] else reg_status),
                        "DEPT": member.get("dept") or "",
                        "Batch": member.get("batch") or "",
                        "Phone": member.get("phone") or "",
                        # If None or empty string, default to True. Otherwise, keep original value.
                        "Attendence": (
                            False if present_status in [None, ""] else present_status
                        ),
                    }
                )

            team_counter += 1

        return data

    except Exception as err:
        raise Exception(f"{err} : while make reg data")
