from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse, StreamingResponse
from app.database.judge import (
    find_all_submits,
    find_all_judged_submits,
    find_a_submit,
    update_a_submit,
    dismiss_a_submit,
)
from app.models.judgement import judgementType

router = APIRouter(prefix="/judgement", tags=["Judge"])


# @router.get("/positions")
# def get_available_positions():
#     # kick a participant

#     pass


@router.post("/submit")
def elemenate_a_submit(team_id: str):
    """kick a participant"""
    res = dismiss_a_submit(team_id)
    if not res:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    if res:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/submit")
def update_a_judgement(team_id: str, payload: judgementType):
    # update a participants submits from db
    res = update_a_submit(team_id, payload)
    if not res:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    if res:
        return Response(status_code=status.HTTP_200_OK)

    return Response(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/submit")
def get_a_submit(team_id: str):
    res = find_a_submit(team_id)
    if not res:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(res, status_code=status.HTTP_200_OK)


@router.get("/submits")
def get_all_submits():
    # get all participant submits from db
    res = find_all_submits()
    if not res:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(res, status_code=status.HTTP_200_OK)


@router.get("/judged")
def get_all_judged_submits():
    # get all participant submits from db
    res = find_all_judged_submits()
    if not res:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(res, status_code=status.HTTP_200_OK)
