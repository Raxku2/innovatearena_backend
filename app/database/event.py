from app.database.connection import event_coll
from app.database.user import is_user_admin
from app.utils.mongo_id_handeler import convert_objectid_in_doc
from app.models.event import scheduleDataType, rulesDataType, eventOrganizers
from bson import ObjectId


def show_event_data():
    try:
        status = event_coll.find_one({"_id": "event"})

        if not status:
            return None

        return convert_objectid_in_doc(status)

    except Exception as err:
        raise Exception(f"{err} : showing event data  ")


def create_event_schadule(data: scheduleDataType):
    schedule_data = data.dict()
    try:
        schedule_data["id"] = ObjectId()
        status = event_coll.update_one(
            {"_id": "event"}, {"$push": {"schedule": schedule_data}}, upsert=True
        )

        return str(schedule_data["id"])

    except Exception as err:
        raise Exception(f"{err} : adding schedule  ")


def update_event_schedule(sch_id: str, data: scheduleDataType):
    schedule_data = data.dict(exclude_none=True, exclude_unset=True)
    try:
        set_query = {f"schedule.$.{key}": value for key, value in schedule_data.items()}

        status = event_coll.update_one(
            {"_id": "event", "schedule.id": ObjectId(sch_id)},
            {"$set": set_query},
        )

        if status.matched_count == 0:
            return None

        return True

    except Exception as err:
        raise Exception(f"{err} : updating schedule  ")


def delete_event_schedule(sch_id: str):
    try:
        status = event_coll.update_one(
            {
                "_id": "event",
            },
            {"$pull": {"schedule": {"id": ObjectId(sch_id)}}},
        )

        if status.modified_count == 0:
            return None

        return True

    except Exception as err:
        raise Exception(f"{err} : deleting schedule  ")


def create_event_rule(data: rulesDataType):
    rule_data = data.dict()
    try:
        rule_data["id"] = ObjectId()
        status = event_coll.update_one({"_id": "event"}, {"$push": {"rule": rule_data}})

        return str(rule_data["id"])

    except Exception as err:
        raise Exception(f"{err} : adding rule  ")


def update_event_rule(rule_id: str, data: rulesDataType):
    rule_data = data.dict(exclude_none=True, exclude_unset=True)
    try:
        set_query = {f"rule.$.{key}": value for key, value in rule_data.items()}

        status = event_coll.update_one(
            {"_id": "event", "rule.id": ObjectId(rule_id)},
            {"$set": set_query},
        )

        if status.matched_count == 0:
            return None

        return True

    except Exception as err:
        raise Exception(f"{err} : updating rule  ")


def delete_event_rule(rule_id: str):
    try:
        status = event_coll.update_one(
            {
                "_id": "event",
            },
            {"$pull": {"rule": {"id": ObjectId(rule_id)}}},
        )

        if status.modified_count == 0:
            return None

        return True

    except Exception as err:
        raise Exception(f"{err} : deleting rule  ")


def create_event_orga(data: eventOrganizers):
    orga_data = data.dict()
    try:
        orga_data["id"] = ObjectId()
        status = event_coll.update_one(
            {"_id": "event"}, {"$push": {"organizer": orga_data}}
        )

        return str(orga_data["id"])

    except Exception as err:
        raise Exception(f"{err} : adding organizer  ")


def update_event_orga(orga_id: str, data: eventOrganizers):
    orga_data = data.dict(exclude_none=True, exclude_unset=True)
    try:
        set_query = {f"organizer.$.{key}": value for key, value in orga_data.items()}

        status = event_coll.update_one(
            {"_id": "event", "organizer.id": ObjectId(orga_id)},
            {"$set": set_query},
        )

        if status.matched_count == 0:
            return None

        return True

    except Exception as err:
        raise Exception(f"{err} : updating organizer ")


def delete_event_orga(orga_id: str):
    try:
        status = event_coll.update_one(
            {
                "_id": "event",
            },
            {"$pull": {"organizer": {"id": ObjectId(orga_id)}}},
        )

        if status.modified_count == 0:
            return None

        return True

    except Exception as err:
        raise Exception(f"{err} : deleting organizer ")
