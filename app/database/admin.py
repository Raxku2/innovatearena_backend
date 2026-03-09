from app.database.connection import user_coll
from app.database.user import is_user_admin
from bson import ObjectId
from app.utils.mongo_id_handeler import (
    convert_objectid_in_list,
    convert_objectid_in_doc,
)
from collections import defaultdict


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
            {"reg_status": True, "payment_status": True},
            {"team_id": 1, "name": 1, "dept": 1, "batch": 1, "present": 1},
        )

        # Initialize a dictionary to group by team_id
        grouped_dict = defaultdict(list)

        for user in data_cursor:
            # Use the helper to handle the ObjectId before grouping
            # print(user)
            clean_user = convert_objectid_in_doc(user)
            tid = clean_user.get("team_id")

            # Append the user details to the specific team list
            grouped_dict[tid].append(
                {
                    "name": clean_user.get("name"),
                    "dept": clean_user.get("dept"),
                    "batch": clean_user.get("batch"),
                    "present": clean_user.get("present"),
                }
            )

        # Format the final output to match the flat CSV requirement with visual grouping
        data = []
        team_counter = 1

        for tid, members in grouped_dict.items():
            for index, member in enumerate(members):
                # Apply the team index (1, 2, 3...) only to the first member (index 0)
                # For all other members in the same team, leave it blank ("")
                display_tid = team_counter if index == 0 else ""

                # Create the flat row dictionary matching your exact CSV headers
                data.append(
                    {
                        "team id": display_tid,
                        "name": member.get("name", ""),
                        "dept": member.get("dept", ""),
                        "batch": member.get("batch", ""),
                        "attendence": member.get(
                            "present", "TRUE"
                        ),  # mapping your 'present' key to 'attendence'
                    }
                )

            # Increment the counter for the next team in the grouped_dict
            team_counter += 1

        return data
    except Exception as err:
        raise Exception(f"{err} : while make admin")
    pass
