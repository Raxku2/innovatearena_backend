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


def check_positions():
    try:

        results = user_coll.find_one({"pos": 1}, {"team_id": 1})
        print("running")

        if results:
            results = convert_objectid_in_doc(results)
            event_coll.update_one(
                {"_id": "event"}, {"$set": {"pos_A": results.get("team_id")}}
            )
        else:
            event_coll.update_one({"_id": "event"}, {"$set": {"pos_A": None}})

        del results

        results = user_coll.find_one({"pos": 2}, {"team_id": 1})

        if results:
            results = convert_objectid_in_doc(results)
            event_coll.update_one(
                {"_id": "event"}, {"$set": {"pos_B": results.get("team_id")}}
            )
        else:
            event_coll.update_one({"_id": "event"}, {"$set": {"pos_B": None}})

        del results

        results = user_coll.find_one({"pos": 3}, {"team_id": 1})

        if results:
            results = convert_objectid_in_doc(results)
            event_coll.update_one(
                {"_id": "event"}, {"$set": {"pos_C": results.get("team_id")}}
            )
        else:
            event_coll.update_one({"_id": "event"}, {"$set": {"pos_C": None}})

        del results

    except Exception as err:
        print(f"{err} : while update submit positions")


def dismiss_a_submit(project_id: str):  # rejected
    try:

        results = user_coll.update_many(
            {"project_id": ObjectId(project_id)},
            {"$set": {"rejected": True, "pos": 0}},
        )

        if results.matched_count == 0:
            return False

        return True

    except Exception as err:
        raise Exception(f"{err} : while reject a submit")


def update_a_submit(project_id: str, data: judgementType):
    # print("running 2")
    try:
        judgement_data = data.dict(exclude_unset=True, exclude_none=True)
        results = user_coll.update_many(
            {"project_id": ObjectId(project_id), "present": True},
            {"$set": judgement_data},
        )
        # print("running 3")

        check_positions()

        # print(results.acknowledged)

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
                "rejected": 1,
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
                "$and": [
                    {
                        "$or": [
                            {"judgement": False},
                            {"judgement": None},
                            {"judgement": {"$exists": False}},
                        ]
                    },
                    {
                        "$or": [
                            {"rejected": False},
                            {"rejected": None},
                            {"rejected": {"$exists": False}},
                        ]
                    },
                ],
            }
        },
        {
            "$group": {
                "_id": "$team_id",
                "team_docs": {
                    "$push": {
                        # "team_id": "$team_id",
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
        list_of_lists = convert_objectid_in_list(item["team_docs"] for item in results)
        check_positions()
        return list_of_lists

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
                        "marks": "$marks",
                        "pos": "$pos",
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
