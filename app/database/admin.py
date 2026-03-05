from app.database.connection import user_coll
from app.database.user import is_user_admin
from bson import ObjectId


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
