from app.database.connection import event_coll
from app.database.user import is_user_admin
from app.utils.mongo_id_handeler import convert_objectid_in_doc
from app.models.event import scheduleDataType, rulesDataType, eventOrganizers
from bson import ObjectId
from fastapi import Request
from app.utils.tracker import get_client_ip


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


def update_registration(root_id: str, event_status: bool):
    try:
        admin_status = is_user_admin(root_id)
        if not admin_status:
            return None

        status = event_coll.update_one(
            {"_id": "event"},
            {"$set": {"registration_process": event_status}},
        )

        if status.matched_count == 0:
            return None

        return True

    except Exception as err:
        raise Exception(f"{err} : updating registration state ")


def update_attendence(root_id: id, attendence_state: bool, request: Request):
    try:
        admin_status = is_user_admin(root_id)
        if not admin_status:
            return None

        ip_of_venue = get_client_ip(request=request)
        if not ip_of_venue:
            return False

        status = event_coll.update_one(
            {"_id": "event"},
            {"$set": {"attendence_process": attendence_state, "ip_addr": ip_of_venue}},
        )

        if status.matched_count == 0:
            return None

        return True

    except Exception as err:
        raise Exception(f"{err} : updating attendence state ")


def update_submits(root_id: str, submit_status: bool, request: Request):
    try:
        admin_status = is_user_admin(root_id)
        if not admin_status:
            return None

        ip_of_venue = get_client_ip(request=request)
        if not ip_of_venue:
            return False

        status = event_coll.update_one(
            {"_id": "event"},
            {"$set": {"submit_process": submit_status, "ip_addr": ip_of_venue}},
        )

        if status.matched_count == 0:
            return None

        return True

    except Exception as err:
        raise Exception(f"{err} : updating submit state ")
