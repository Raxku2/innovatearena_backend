from fastapi import APIRouter, Response, status, Request
from fastapi.responses import JSONResponse
from app.models.event import scheduleDataType, rulesDataType, eventOrganizers
from app.database.event import (
    show_event_data,
    create_event_schadule,
    update_event_schedule,
    delete_event_schedule,
    create_event_orga,
    create_event_rule,
    update_event_orga,
    update_event_rule,
    delete_event_orga,
    delete_event_rule,
    update_registration,
    update_attendence,
    update_submits,
)

router = APIRouter(prefix="/event", tags=["Event"])


@router.get("/")
def get_event_data():
    try:
        res = show_event_data()

        if not res:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return JSONResponse(res)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.post("/schedule")
def post_schedule(payload: scheduleDataType):
    try:
        res = create_event_schadule(payload)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(res, status_code=status.HTTP_201_CREATED)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.put("/schedule/{sch_id}")
def put_schedule(payload: scheduleDataType, sch_id: str):
    try:
        res = update_event_schedule(sch_id=sch_id, data=payload)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.delete("/schedule/{sch_id}")
def delete_schedule(sch_id: str):
    try:
        res = delete_event_schedule(sch_id=sch_id)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.post("/rule")
def post_rule(payload: rulesDataType):
    try:
        res = create_event_rule(payload)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(res, status_code=status.HTTP_201_CREATED)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.put("/rule/{rule_id}")
def put_rule(payload: rulesDataType, rule_id: str):
    try:
        res = update_event_rule(rule_id=rule_id, data=payload)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.delete("/rule/{rule_id}")
def delete_rule(rule_id: str):
    try:
        res = delete_event_rule(rule_id)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.post("/organizer")
def post_organizer(payload: eventOrganizers):
    try:
        res = create_event_orga(payload)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(res, status_code=status.HTTP_201_CREATED)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.put("/organizer/{orga_id}")
def put_organizer(orga_id: str, payload: eventOrganizers):
    try:
        res = update_event_orga(orga_id=orga_id, data=payload)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.delete("/organizer/{orga_id}")
def delete_organizer(orga_id: str):
    try:
        res = delete_event_orga(orga_id)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.put("/reg/{root_id}")
def put_registration_process(root_id: str, reg_state: bool):
    try:
        res = update_registration(root_id=root_id, event_status=reg_state)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.put("/attendence/{root_id}")
def put_attendence_process(root_id: str, attendence_state: bool, request: Request):
    try:
        res = update_attendence(
            root_id=root_id, attendence_state=attendence_state, request=request
        )

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        # print(err)
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.put("/submits/{root_id}")
def put_submit_process(root_id: str, submit_state: bool, request: Request):
    try:
        res = update_submits(
            root_id=root_id, submit_status=submit_state, request=request
        )

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
