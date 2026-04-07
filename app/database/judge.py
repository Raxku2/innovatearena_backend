from app.database.connection import user_coll, event_coll
from bson import ObjectId
from app.utils.mongo_id_handeler import (
    convert_objectid_in_list,
    convert_objectid_in_doc,
)
from bson import ObjectId
from app.models.judgement import judgementType

# work here with get submits


def get_all_positions():
    pass


def dismiss_a_submit(team_id: str):  # rejected
    try:

        results = user_coll.update_many(
            {"team_id": ObjectId(team_id)},
            {"$set": {"rejected": True}},
        )

        if results.matched_count == 0:
            return False

        return True

    except Exception as err:
        raise Exception(f"{err} : while reject a submit")


def update_a_submit(team_id: str, data: judgementType):
    try:
        judgement_data = data.dict(exclude_unset=True, exclude_none=True)
        results = user_coll.update_many(
            {"team_id": ObjectId(team_id), "present": True},
            {"$set": judgement_data},
        )

        if results.matched_count == 0:
            return False

        return True

    except Exception as err:
        raise Exception(f"{err} : while update a judgement")


def find_a_submit(team_id: str):
    try:
        results = user_coll.find_one(
            {"team_id": ObjectId(team_id), "present": True},
            {
                "project_title": 1,
                "deployment": 1,
                "repo": 1,
                "marks": 1,
                "pos": 1,
                "project_id": 1,
            },
        )

        return convert_objectid_in_doc(results)

    except Exception as err:
        raise Exception(f"{err} : while find a submit")


def find_all_submits():
    pipeline = [
        {
            "$match": {
                # Filter 1: 'present' must be true
                "present": True,
                # Filter 2: 'judgement' is false, None, or doesn't exist
                "$or": [
                    {"judgement": False},
                    {"judgement": None},
                    {"judgement": {"$exists": False}},
                ],
                "$or": [
                    {"rejected": False},
                    {"rejected": None},
                    {"rejected": {"$exists": False}},
                ],
            }
        },
        {
            "$group": {
                "_id": "$team_id",
                "team_docs": {
                    "$push": {
                        "project_id": "$project_id",
                        "project_title": "$project_title",
                        "deployment": "$deployment",
                        "repo": "$repo",
                    }
                },
            }
        },
        {"$project": {"_id": 0, "team_docs": 1}},
    ]

    try:
        results = list(user_coll.aggregate(pipeline))
        list_of_lists = [item["team_docs"] for item in results]

        return convert_objectid_in_list(list_of_lists)

    except Exception as err:
        raise Exception(f"{err} : while get submits")


def find_all_judged_submits():
    pipeline = [
        {
            "$match": {
                "present": True,
                "judgement": True,
                "$or": [
                    {"rejected": False},
                    {"rejected": None},
                    {"rejected": {"$exists": False}},
                ],
            }
        },
        {
            "$group": {
                "_id": "$team_id",
                "team_docs": {
                    "$push": {
                        "project_id": "$project_id",
                        "project_title": "$project_title",
                        "deployment": "$deployment",
                        "repo": "$repo",
                    }
                },
            }
        },
        {"$project": {"_id": 0, "team_docs": 1}},
    ]

    try:
        results = list(user_coll.aggregate(pipeline))
        list_of_lists = [item["team_docs"] for item in results]

        return convert_objectid_in_list(list_of_lists)

    except Exception as err:
        raise Exception(f"{err} : while find judged submits")
