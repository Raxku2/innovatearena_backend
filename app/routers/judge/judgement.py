from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse, StreamingResponse
from app.database.judge import find_all_submits, find_all_judged_submits

router = APIRouter(prefix="/judgement", tags=["Judge"])


@router.get("/positions")
def get_available_positions():
    # kick a participant

    pass


@router.patch("/submit")
def elemenate_a_submit(team_id: str):
    # kick a participant
    pass


@router.patch("/submit")
def update_a_submit(team_id: str):
    # update a participants submits from db
    pass


@router.get("/submit")
def get_a_submit(team_id: str):
    # get a participants submits from db
    pass


@router.get("/submits")
def get_all_submits():
    # get all participant submits from db
    res = find_all_submits()
    if not res:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JSONResponse(res, status_code=status.HTTP_200_OK)


@router.get("/judged")
def get_all_judged_submits():
    # get all participant submits from db
    res = find_all_judged_submits()
    if not res:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(res, status_code=status.HTTP_200_OK)
