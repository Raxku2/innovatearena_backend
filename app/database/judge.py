from app.database.connection import user_coll, event_coll
from bson import ObjectId
from app.utils.mongo_id_handeler import (
    convert_objectid_in_list,
    convert_objectid_in_doc,
)


# work here with get submits


def get_all_positions():
    pass


def dismiss_a_submit():
    pass


def update_a_submit():
    pass


def find_a_submit():
    pass


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
        raise Exception(f"{err} : while remove judge")


def find_all_judged_submits():
    pipeline = [
        {
            "$match": {
                "present": True,
                "judgement": True,
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
        raise Exception(f"{err} : while remove judge")
