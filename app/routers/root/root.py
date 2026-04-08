from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse, StreamingResponse
from app.database.admin import (
    showStatics,
    showAdmin,
    setAdmin,
    getRegInfo,
    readAttendance,
    setJudge,
    removeJudge,
)
from app.models.user import adminSetter
from app.utils.csv_handeler import iter_csv
from datetime import datetime


router = APIRouter(prefix="/root", tags=["Admin"])


@router.delete("/admins/judge")
def delete_judge(judge_email: str):
    try:
        res = removeJudge(judge_email)

        if res:
            return Response(status_code=status.HTTP_200_OK)
        else:
            return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    except Exception as err:
        print(err)
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.post("/admins/judge")
def make_judge(judge_email: str):
    try:
        res = setJudge(judge_email)

        if res:
            return Response(status_code=status.HTTP_200_OK)
        else:
            return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    except Exception as err:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.get("/admins/attendance/{root_id}")
def get_attendance(root_id: str):
    try:
        data = readAttendance(root_id)
        return JSONResponse(data)
    except Exception as err:
        if err == "Unauth":
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        print(f"{err} : while get attendance route")

        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.get("/admins/{root_id}")
def get_admins(root_id: str):
    try:
        data = showAdmin(root_id)
        return JSONResponse(data)
    except Exception as err:
        if err == "Unauth":
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        print(f"{err} : while get admins route")

        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.post("/admins/{root_id}")
def get_admins(root_id: str, payload: adminSetter):
    try:
        data = setAdmin(root_id, payload.target, payload.param)
        # return JSONResponse(data)
        if not data:
            return Response(status_code=status.HTTP_304_NOT_MODIFIED)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        if err == "Unauth":
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        print(f"{err} : while set admins route")

        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.get("/reg/{root_id}")
def get_reg_data(root_id: str):
    try:
        # 1. Get the formatted data from your existing function
        data = getRegInfo(root_id=root_id)

        now = datetime.now().strftime("%d_%m_%y_%H_%M_%S")

        # 2. Return it as a streaming CSV file
        return StreamingResponse(
            iter_csv(data),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=innovatearena_registrations_{now}.csv"
            },
        )

    except Exception as err:
        # Keeping your exact error handling logic
        if str(err) == "Unauth":
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)

        print(f"{err} : while get reg csv route")
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.get("/{root_id}")
def get_tatistic(root_id: str):
    try:
        data = showStatics(root_id)
        return JSONResponse(data)
    except Exception as err:
        if err == "Unauth":
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        print(f"{err} : while statistic route")

        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
