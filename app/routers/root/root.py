from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from app.database.admin import showStatics

router = APIRouter(prefix="/root", tags=["Admin"])


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
