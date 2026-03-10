from app.database.connection import event_coll


def get_venue_ip():
    try:
        status = event_coll.find_one({"_id": "event"}, {"ip_addr": 1, "_id": 0})

        if status == 0:
            return None

        return status.get("ip_addr")

    except Exception as err:
        raise Exception(f"{err} : updating submit state ")
